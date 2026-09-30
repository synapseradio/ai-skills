# surface-intent: dark mode for a grandmother's recipe website

- skill: surface-intent, from commit 0c9258f
- subject: "Add a dark mode to our grandmother's recipe website."
- kind: single run

## Prompt

/surface-intent Add a dark mode to our grandmother's recipe website.

## Run

### Beat 1: before acting, surface what is already there

**1. Name it in one line.**

Add a dark color scheme to the recipe website, so a reader can use it in low light, such as a kitchen at night.

That sentence carries a guess: I wrote "so a reader can use it in low light" without being told why dark mode is wanted. The purpose is what step 2 searches by, so I hold it as assumed until the survey or the requester says otherwise.

**2. Read what already serves that purpose.**

Survey, three angles, per the method in the skill's incoming reference.

- By name: I searched the projects directory on this machine for paths containing "recipe", "grandma", or "grandmother". Nothing came back. The site's source is not reachable from here.
- By purpose: the words the existing thing would use for this job are "dark", "theme", "color scheme", "prefers-color-scheme", "night", "contrast", "print", "reader mode". I could not search a codebase for them, because I have none. So I list where they would be found, for whoever opens the site next:
    - the stylesheet: any `@media (prefers-color-scheme: dark)` block, or a `.dark` or `[data-theme]` selector;
    - the color definitions: hard-coded hex values scattered through rules, or a small set of named variables (`--bg`, `--text`) reused everywhere;
    - the page head: a `color-scheme` meta tag, or a theme toggle script;
    - the host or site builder: many website builders and blog templates ship a dark theme as a setting, so "add" may mean "switch on";
    - the browser: readers who already use a dark operating-system setting or a browser extension that darkens pages may already see a dark site, so the missing piece may be smaller than it looks.
- By place: a recipe site's dark mode would live in the shared stylesheet or template, and in the printable recipe view, which is a second surface with opposite needs (dark ink on white paper).

**3. Diff against what exists.**

I cannot run the diff, because the "what exists" side is empty. Two things I can say without the site:

- The comparison is by what each thing makes true, not by wording. "Dark mode" is satisfied when text stays readable against a dark background on every page, and when the reader's choice, or their system's setting, decides which they see. If the site already has a theme setting that a hosting service provides, that condition may already hold under another name.
- My verdict is not covered by evidence, and not covered by assumption either. It is unknown.

Verdict: **unknown**. I am not entitled to write "not covered", so I do not proceed to build. The next step is one read of the site, not a design.

**4. State what you found.**

Searched: the local projects directory by three name patterns. Found: nothing. Concluded: no evidence about coverage in either direction.

Sorted, per the known, assumed, unknown split:

- Known: nothing about the site. No file or line I can point to.
- Assumed, each to confirm or mark open:
  1. The site has a stylesheet I can edit, and is not a hosted builder page with a theme menu.
  2. The purpose is comfortable low-light reading, not a visual preference or an accessibility need such as light sensitivity.
  3. The colors are not yet centralized.
  4. There is no dark styling already in place.
- Unknown, named so they do not shape the decision silently:
  1. Who edits the site now, and how (hand-written files, a builder, a blog engine)?
  2. Does the site have a printable recipe view?
  3. Do recipe photos have transparent backgrounds or baked-in white borders, which look wrong on a dark page?
  4. Who is the least-practiced reader who will act on the finished change: the grandmother, a family member who maintains the site, or a visitor?

The failure mode to avoid here is the middle pile passing for the first. "I assume nothing covers this" is not "I read the site and nothing covers this."

Decision path once the site is read:

- Already covered (a theme option or dark stylesheet exists): sharpen it. Fix low-contrast spots. Do not add a second theme beside it.
- Partly covered (some variables or a media query exist): extend the smallest missing piece, such as the untouched pages or the photo borders.
- Not covered: add it, and say so with the search terms and files you read.

### Beat 2: as you produce, surface your own intent

Nothing is built yet, since Beat 1 ended in unknown. Beat 2 applies to what I hand back now, and to the change when it is made.

**1. Name things for what they are.** If the change lands, the names say the purpose: `color-scheme: light dark` in the head; variables `--page-background`, `--body-text`, `--link`, `--recipe-card-background`. No `--c1`, no `--dm`. A comment states why, for example "photos keep a light mat so white-edged images do not glow on the dark page", never what the variable is.

**2. Prefer one named root over indirection.** Every color the site uses becomes a variable defined once, with a light value and a dark value. Rules refer to the variable. The alternative, a second stylesheet that overrides the first rule by rule, hides the shared intent (one palette, two settings) behind a trail of overrides that drift apart when a recipe page is restyled later. One named root beats many links.

**3. Make it clear enough to act on.**

The note for whoever maintains the site, top terse, depth waiting below:

> **Dark mode: what to do first.** Open the site's stylesheet and look for two things: colors written directly into many rules, and any existing dark or theme setting. Reply with what you find. If a theme setting exists, use it. If not, the change is to name the colors once and give each a dark value.
>
> **Depth, open when needed.** Which readers get dark mode by default (those whose device is set to dark) versus by a switch on the page. Printing: recipes print on white paper, so the printable view keeps light colors. Photos: check the ones with white borders. Contrast: body text against the dark background should stay easy to read at a glance across a kitchen, so pick a soft off-white on a deep gray, not pure white on pure black.

The top holds the first action. The rationale sits below, which is how this skill is built.

**4. Self-check before you ship.**

Read as the second reader, holding only the subject sentence and this output. Could they follow it and reach the same place? They would reach "read the site's stylesheet first", which is the place I reached. Where the intent did not make the page: the reason for dark mode is my guess, and I said so in step 1 and again in the assumed pile. Ranked, solid to shaky:

- Solid: no reachable site was searched, and the search found nothing. That is what happened.
- Shaky: every item under "assumed". Each is a starting guess, not a finding.
- Shakiest: that low-light reading is the purpose. It steers the contrast advice and the print exception, and only the requester can confirm it.

Grounding claims in evidence, such as the contrast recommendation, belongs to the warrant discipline. Per the skill's outgoing reference, I point at that seam and stop. The soft-off-white advice above rests on my conviction and carries no source; a reader who acts on it should check it against a contrast tool, or I should cut it.

**Result of the run:** the intent behind the request is not yet surfaced, because the existing site has not been read. Handed back: one line naming the change, the survey performed and its empty result, the sorted piles, the three-way decision path, and a maintainer note whose first action is to read the stylesheet.
