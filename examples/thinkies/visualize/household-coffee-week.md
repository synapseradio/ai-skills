# visualize: a household's coffee across one week

- skill: visualize, from commit 0c9258f
- subject: Show how a household of three's coffee consumption changes across the week. Cups per day, Mon–Sun: 9, 7, 8, 11, 6, 3, 4. Monday's spike follows a Sunday-night "just one episode" habit.
- kind: staged conversation (the user side played by a second agent)

## Prompt

/visualize Show how a household of three's coffee consumption changes across the week. Cups per day, Mon–Sun: 9, 7, 8, 11, 6, 3, 4. Monday's spike follows a Sunday-night "just one episode" habit.

## Run

**Skill:**

### Phase 1: Think

- Argument: This visualization shows that Monday runs high at 9 cups, but Thursday is the week's peak at 11, and the weekend sits at 3 and 4.
- Viewer and task: The three housemates need to judge, at their Sunday check-in, whether the Sunday-night "just one episode" habit is worth changing.
- Cognitive mode: conclusion (inference). One week of counts cannot decide anything on its own, so the viewer weighs a pattern; nobody has to act on a signal at a glance.
- Constraints: a markdown page, so no scripts or interactive marks; a non-technical audience; the data is in hand (7 whole-number counts); a quick result; a plain-text chart with the numbers beside it, which screen readers can read.
- Honesty check:
    - You called Monday's count a spike, but Thursday's 11 is higher than Monday's 9. Monday is the second-highest day, not the peak.
    - Monday is the first row of the week, so the Sunday before it is not in the data. The Sunday shown (4) comes at the end of the week. Comparing Monday's 9 with Sunday's 4 assumes the Sunday before was also about 4.
    - The link between the Sunday-night habit and Monday's count comes from your description. The counts carry no bedtime or episode information, and one week cannot separate the habit from a general weekday rise (Monday to Friday range 6 to 11 against 3 and 4 on the weekend).
    - The counts are for the whole household (48 cups in the week, about 2.3 cups per person per day), not per person.
- Editorial integrity: I set no thresholds or bins. I show all seven days, none left out. The finding that cuts against your framing, Thursday's 11, gets an on-chart marker equal to Monday's, not a footnote.

### Phase 2: Research

Data classification:

| Attribute | Type | Unit | Notes |
|---|---|---|---|
| Day | Temporal (ordered names) | day of week, Mon to Sun | keep chronological order |
| Cups per day | Quantitative | cups per day, whole household | 9, 7, 8, 11, 6, 3, 4; none missing |
| Change from previous day (derived) | Quantitative | cups | Tue -2, Wed +1, Thu +3, Fri -5, Sat -3, Sun +1; Monday has none |

Encoding plan: cups per day as bar length from zero (one block = 1 cup), with the exact number printed at the end of each bar; days as row order, Monday first. Position on a common scale would be more accurate, but a text chart has only row position and length, so the printed number covers the precision length loses. Color is not used, so nothing depends on color.

Engine: Markdown, decided by criterion 2 (the destination is a markdown page). Template: unicode-bar-chart, rows kept in Monday-to-Sunday order, not sorted by value, because the days are a time sequence and sorting would erase the week.

Transforms, in order: (1) keep days in chronological order; (2) derive change from previous day; (3) derive weekday mean (Mon to Fri: 41 cups, 8.2 per day) and weekend mean (Sat and Sun: 7 cups, 3.5 per day); (4) scale bars at one block per cup.

Accessibility: no color; numbers printed beside every bar; a values table under the chart.

Decision for you: I will build around "Monday runs high, but Thursday peaks" because that is what the seven counts support. If you want the chart built around Monday alone, say so. Approve this plan, or redirect?

**User (played):** Approved, go ahead with "Monday runs high, but Thursday peaks." I hadn't noticed Thursday was higher. We only count the whole household, not per person, so that's fine. Please keep the days in Monday-to-Sunday order and keep it simple so it pastes into our page.

**Skill:**

### Phase 3: Build

Encode. Encoding table with channel rank (from the channel-effectiveness ranking):

| Variable | Type | Unit | Channel | Rank | Typical error |
|---|---|---|---|---|---|
| Cups per day | Quantitative | cups per day | Length from a zero baseline (one block per cup) | 3 | about 5-10% |
| Cups per day, exact | Quantitative | cups per day | Printed number after each bar | not a channel; restores exactness | none |
| Day | Temporal | day of week | Row order, Monday first | spatial region (identity and order) | none |
| Highlight (Monday, Thursday) | Nominal | none | Marker glyph and note at the row end | redundant, not color | none |

Position on a common scale (rank 1) is out of reach in monospace text, so length (rank 3) carries the quantity and the printed count carries the precision. The bars start at zero, so each block is one cup.

Compose. Three-level weight assignment:

- Primary: the Thursday and Monday rows with their end-of-row markers. Weight move: isolation, because the marker and note sit to the right of the bar, where no other row has text.
- Secondary: the other five bars and the printed counts. Weight move: plain rows with no marker.
- Tertiary: the source line and the values table. Weight move: position, since both sit below the chart, set off by a blank line, in smaller table form.

Narrate.

- Title (takeaway): "Monday runs high at 9 cups, but Thursday peaks at 11"
- Subtitle (context): "Household of three, cups of coffee per day, Monday to Sunday, one week"
- Annotations:
    - Monday, 9 cups: "Monday, after the Sunday-night episode habit (reported, not measured here)"
    - Thursday, 11 cups: "week's peak"

Interact. Skip condition: the destination is a markdown page, a static medium with no scripts, so there are no tooltips, filters, or brushing. Tooltip fields do not apply; the printed counts do their job. Sizing: fixed-width text, 11 blocks at most, which fits a column of about 100 characters.

Access audit:

- [x] Palette: no color used, so no palette or red-green pair to check
- [x] Contrast: default text color on the page background
- [x] SVG title and desc: not applicable, the chart is text; the title line and the values table carry the same content
- [x] Data table fallback: the values table under the chart
- [x] Units on every value: "cups" after each count; "cups" in the table header
- [x] Redundant encoding: bar length plus the printed number; markers plus words, not color

### Phase 4: Verify (first draft, then second draft)

Pass A, structural read-back of the first draft:

- [x] Frontmatter has name, description, chart-type, engine, project, created
- [x] Title states the takeaway, not the topic
- [x] Units on every count and on the table header
- [x] Sort order: chronological, matching the time sequence being shown, so the value-sort rule does not apply
- [x] Source line present
- [ ] The Monday note read "after the Sunday-night episode habit", which states the habit as fact and reads as the cause. The counts do not show it.

Pass B, render inference from the source:

- One block is one cup: Thursday's 11 blocks are the widest bar and Saturday's 3 the narrowest, which matches the counts.
- Alignment: every bar is padded to 11 cells, then two spaces, then the count right-aligned in two cells, so the counts end in the same column (Thursday's "11" fills both cells; single digits start one cell later).
- The block glyph and the marker glyph are one cell wide in the usual monospace fonts. In a font that draws them wider, the columns shift together and the counts stay readable.
- The longest row is the Monday note, about 100 characters, at the edge of a README column; it wraps at the note, after the counts, so the bars and counts stay intact.
- Zero baseline: bars begin at the same left edge; no bar is truncated.

The passes disagreed on one point: Pass A flagged the Monday wording, and Pass B, which reads only geometry, saw nothing wrong with it. The disagreement is a defect in the wording, since a reader takes the note as a cause. Fix: the Monday note now ends "(reported, not measured here)".

Second draft, re-verified on both passes: both passes agree. Style pass against the core principles: composition (one chart, one claim, two marked rows), color (none, so nothing to conflict), spacing (blank lines between chart, source, and table), simplicity (no non-data elements). Regression check: units still present, both annotations still match the counts (Monday 9, Thursday 11), nothing reordered.

Editorial integrity check (mode-refine): thresholds, none used; metric selection, cups per day is the only metric available and would be shown whether Monday stood out or not; epistemic commitment, Thursday's contradicting 11 has a marker equal to Monday's.

**Skill:**

### Phase 5: Present

This visualization shows that Monday runs high at 9 cups, but Thursday is the week's peak at 11, and the weekend sits at 3 and 4.

Encoding: bar length from zero (one block per cup) with the exact count printed after every bar; days in Monday-to-Sunday order. Accessibility: no color, counts printed, a values table below. Limits: the chart cannot show that the Sunday-night habit causes Monday's count; the Sunday before Monday is not in the data; the counts are household totals and one week is a small sample; bar blocks render slightly differently across fonts, so the printed numbers are the reference.

Final artifact:

````markdown
---
name: Household Coffee Week
description: Cups of coffee per day for a household of three, Monday to Sunday, as a unicode bar chart
chart-type: unicode-bar-chart
engine: markdown
project: household-notes
created: 2026-09-30T12:00:00Z
---

# Monday Runs High at 9 Cups, but Thursday Peaks at 11

Household of three, cups of coffee per day, Monday to Sunday, one week.

```
Mon  █████████     9 cups  ◀ Monday, after the Sunday-night episode habit (reported, not measured here)
Tue  ███████       7 cups
Wed  ████████      8 cups
Thu  ███████████  11 cups  ◀ week's peak
Fri  ██████        6 cups
Sat  ███           3 cups
Sun  ████          4 cups
```

Source: one week of the household coffee tally, Monday to Sunday, whole household, 48 cups in total. Bar width proportional to value; one block = 1 cup. Weekdays (Mon to Fri) average 8.2 cups a day; Saturday and Sunday average 3.5.

## Underlying values

| Day | Cups per day | Change from previous day (cups) |
| --- | -----------: | ------------------------------: |
| Mon |            9 |          none (Sunday before is not in the data) |
| Tue |            7 |                              -2 |
| Wed |            8 |                              +1 |
| Thu |           11 |                              +3 |
| Fri |            6 |                              -5 |
| Sat |            3 |                              -3 |
| Sun |            4 |                              +1 |
````

**User (played):** This looks good to me. The bars match my numbers, and I like that Thursday's peak is marked too. The note on Monday about the Sunday-night episode habit is fine, and "reported, not measured" is fair, since that's just what we told you. Please finish it so I can paste it into our page.

**Skill:**

### Phase 6: Save

Output kind: markdown (`.md`), so no HTML file was produced and no browser open applies. The harness fallback for a run outside a project store is to print the artifact, which is done above; the artifact is the final record. Registering it with the visualizer CLI is optional and was not run.

Record: name "Household Coffee Week"; engine markdown; template unicode-bar-chart; source line and values table included.
