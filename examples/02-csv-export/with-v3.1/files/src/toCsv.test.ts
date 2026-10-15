import { test } from "node:test";
import assert from "node:assert/strict";
import { toCsv, type Column } from "./toCsv.ts";

type Row = { id: string | number; customer: string; total: number | string; status: string };

const columns: Column<Row>[] = [
  { header: "ID", value: (o) => o.id },
  { header: "Customer", value: (o) => o.customer },
  { header: "Total", value: (o) => o.total },
  { header: "Status", value: (o) => o.status },
];

const hostile: Row[] = [
  { id: 1, customer: "Acme, Inc.", total: 120.5, status: "paid" },
  { id: 2, customer: 'The "Best" Shop', total: 9.99, status: "paid" },
  { id: 3, customer: "Line\nBreak Ltd", total: 10, status: "pending" },
  { id: 4, customer: "Carriage\r\nReturn Co", total: 11, status: "pending" },
  { id: 5, customer: "=HYPERLINK(\"http://x\",\"y\")", total: 1, status: "paid" },
  { id: 6, customer: "+SUM(A1:A9)", total: 2, status: "paid" },
  { id: 7, customer: "-2+3", total: 3, status: "refunded" },
  { id: 8, customer: "@cmd", total: 4, status: "paid" },
  { id: 9, customer: "\tTabbed", total: 5, status: "paid" },
  { id: 10, customer: "Zoë Müller 東京", total: -12.5, status: "refunded" },
  { id: 11, customer: "", total: 0, status: "" },
  { id: 12, customer: "  padded , \"mixed\"\n=all ", total: 1e21, status: "paid" },
];

// Minimal RFC 4180 parser, independent of the implementation under test.
function parse(csv: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let i = 0;
  let quoted = false;
  while (i < csv.length) {
    const c = csv[i];
    if (quoted) {
      if (c === '"' && csv[i + 1] === '"') { cell += '"'; i += 2; continue; }
      if (c === '"') { quoted = false; i++; continue; }
      cell += c; i++; continue;
    }
    if (c === '"' && cell === "") { quoted = true; i++; continue; }
    if (c === ",") { row.push(cell); cell = ""; i++; continue; }
    if (c === "\r" && csv[i + 1] === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; i += 2; continue; }
    if (c === "\n" || c === "\r") throw new Error(`bare line break outside quotes at ${i}`);
    cell += c; i++;
  }
  if (cell !== "" || row.length) { row.push(cell); rows.push(row); }
  return rows;
}

const FORMULA = /^[=+\-@\t\r]/;
const expected = (v: unknown) =>
  typeof v === "string" && FORMULA.test(v) ? `'${v}` : String(v);

test("starts with a UTF-8 BOM and uses CRLF", () => {
  const csv = toCsv(hostile, columns);
  assert.equal(csv.charCodeAt(0), 0xfeff);
  assert.ok(csv.endsWith("\r\n"));
});

test("12 hostile rows round-trip with 0 altered cells", () => {
  const parsed = parse(toCsv(hostile, columns).replace(/^﻿/, ""));
  assert.deepEqual(parsed[0], ["ID", "Customer", "Total", "Status"]);
  assert.equal(parsed.length, hostile.length + 1);
  const altered: string[] = [];
  hostile.forEach((r, i) => {
    columns.forEach((col, j) => {
      const want = expected(col.value(r));
      const got = parsed[i + 1]?.[j];
      if (got !== want) altered.push(`row ${r.id} ${col.header}: ${JSON.stringify(got)} != ${JSON.stringify(want)}`);
    });
  });
  assert.deepEqual(altered, [], `${altered.length} altered cells`);
});

test("no string cell starts with a formula trigger; numbers stay numeric", () => {
  const parsed = parse(toCsv(hostile, columns).replace(/^﻿/, ""));
  for (const row of parsed.slice(1)) assert.ok(!FORMULA.test(row[1]), row[1]);
  assert.equal(parsed[10][2], "-12.5");
});
