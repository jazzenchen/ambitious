Here's the most ambitious version I'd propose, followed by a smaller fallback. I haven't opened the repo or written anything yet, since you asked to see the proposal first.

## The ambitious version: a full launch kit

**1. The flagship post, written as a story.** It would open on the problem Tidepool exists to solve and why it matters now. It would then cover what 1.0 promises, such as stability and API guarantees, and end with one demo that makes the reader think "oh, I need this." The full feature list would go in the release notes, not the post.

**2. Every claim checked against the repo.**
- Each code snippet in the post gets run against the v1.0 code here.
- Any performance numbers come from a benchmark script I write and commit, so the figures can be reproduced.
- If a claim can't be backed up, it gets cut or softened.

**3. An interactive web page of the post.** The same post, published as a page with:
- live charts for any benchmarks
- tabbed before-and-after code examples
- a "try it in 60 seconds" section

You'd have both a Markdown version for your blog and a link you can share right away.

**4. The rest of launch day, written in the same voice:**
- release notes and a 0.x → 1.0 migration guide (I'll work out the breaking changes from the git history)
- a Show HN post and its first comment
- a thread for X or Bluesky, a LinkedIn post and a newsletter email
- a FAQ answering the objections people are likely to raise ("why not X?", "is it production-ready?", "who maintains it?")

**5. A hostile review before you ship.** A separate agent reads the post as a skeptical Hacker News commenter and as a first-time user. Then I revise it based on what they find.

**Cost and limits:** this fits within the $4 budget, but only just. If money gets tight, I'd cut parts 4 and 5 first. The weak point is facts I can't get from the repo, like who uses Tidepool, quotes, the launch date and the story of why it was started. I'd mark those as `[TK]` rather than make them up.

## The fallback: just the post

One polished launch post as Markdown in the repo. I'd still check the code snippets against the repo, but I'd skip the web page, the other launch pieces and the hostile review.

## Before I start

1. **Ambitious, fallback, or somewhere in between?** You could also pick specific numbered parts.
2. **Who is the main audience?** For example developers, data teams, or buyers at companies.
3. **Anything I can't get from the repo?** A launch date, user names, a founder story, or a tone you want, like Stripe-style polish or a hacker-blog voice.

If you'd rather I just pick, say "go" and I'll do the ambitious version. My first step will be reading the repo to learn what Tidepool actually is.