export type Column<T> = { header: string; value: (row: T) => unknown };

// Spreadsheet apps execute cells starting with these as formulas (OWASP CSV injection).
const FORMULA_TRIGGER = /^[=+\-@\t\r]/;

function cell(value: unknown): string {
  let s = value == null ? "" : String(value);
  // Numbers pass through so negative totals stay numeric.
  if (typeof value === "string" && FORMULA_TRIGGER.test(s)) s = `'${s}`;
  return /[",\r\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

// RFC 4180 CSV with a UTF-8 BOM so Excel decodes non-ASCII names correctly.
export function toCsv<T>(rows: T[], columns: Column<T>[]): string {
  const lines = [
    columns.map((c) => cell(c.header)),
    ...rows.map((r) => columns.map((c) => cell(c.value(r)))),
  ];
  return "﻿" + lines.map((l) => l.join(",") + "\r\n").join("");
}

export function downloadCsv(filename: string, csv: string): void {
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
