# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add at least five advanced song attributes to the CSV and update the
recommender so user preferences can score those attributes.

**Prompts used:**

> Add five new song attributes that are not in the baseline CSV: popularity
> from 0-100, release decade, semicolon-separated detailed mood tags,
> lyrical complexity from 0-1, and instrumentalness from 0-1. Update
> `load_songs` to convert numeric values and update `score_song` to add
> bounded, explainable points for matching user preferences for these fields.
> Keep the existing genre, mood, energy, and acoustic scoring behavior.

**What did the agent generate or change?**

The workflow added five columns and values for all 10 songs in
`data/songs.csv`. It updated `load_songs` to parse popularity, release
decade, lyrical complexity, and instrumentalness. It updated `score_song` to
score popularity similarity, decade matches, detailed mood tags, lyrical
complexity similarity, and instrumental preference. It added advanced
preferences to the profiles in `src/main.py`.

**What did you verify or fix manually?**

I checked that every CSV row has all five new fields and that semicolon
separators keep mood tags inside one CSV cell. I ran the CLI and confirmed
that scores and explanations include the new features. I also checked that
the popularity and lyrical-complexity similarities are clamped to valid
0-to-1 ranges before their 0.5-point weights are applied.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
