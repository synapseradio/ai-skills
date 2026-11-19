# visualize: a household's coffee across one week

- skill: visualize, from commit d7e0155
- subject: Show how a household of three's coffee consumption changes across the week, as a page to open in a browser. Cups per day, Mon–Sun: 9, 7, 8, 11, 6, 3, 4. Monday's spike follows a Sunday-night "just one episode" habit.
- kind: unattended run (one agent, no user turns)

## Prompt

/visualize Show how a household of three's coffee consumption changes across the week, as a page I can open in my browser. Cups per day, Mon–Sun: 9, 7, 8, 11, 6, 3, 4. Monday's spike follows a Sunday-night "just one episode" habit.

## Run

**Skill:**

### 1. Settle the claim and the surface

This shows that Monday runs high at 9 cups, but Thursday is the week's peak at 11, and the weekend drops to 3 and 4.

What cuts against the framing in the request:

- You called Monday's count a spike, but Thursday's 11 is higher than Monday's 9. Monday is the second-highest day.
- Monday is the first row, so the Sunday before it is not in the data. The Sunday shown (4) ends the week.
- The link between the Sunday-night habit and Monday's count comes from your description. The counts carry no bedtime information, and one week cannot separate the habit from a general weekday rise.
- The counts are for the whole household: 48 cups in the week.

Surface: you asked for a page to open in a browser, so this is the HTML route.

### 2. Prepare the data

`coffee.csv`:

```text
day,cups
Mon,9
Tue,7
Wed,8
Thu,11
Fri,6
Sat,3
Sun,4
```

```bash
uv run --no-project scripts/prepare_data.py coffee.csv --x day --y cups --out rows.json
```

```text
note: summary: 7 rows; day is category; cups runs 3 to 11
wrote rows.json
```

No problem lines. The one note says the days were read as categories, which decides the next step.

### 3. Choose the chart

The question is how a value changes along an order, so the chart is a line. The days are categories with a real order, Monday to Sunday, so the spec sets `"ordered": true` on x. There is one series and one measure, so one chart carries the point.

### 4. Build the page

`spec.json`:

```json
{
  "title": "Monday runs high at 9 cups, but Thursday peaks at 11",
  "subtitle": "Household of three, cups of coffee per day, Monday to Sunday, one week",
  "summary": "Thursday is the week's high at 11 cups and Monday is second at 9. Weekdays run 6 to 11 cups; Saturday and Sunday drop to 3 and 4. The week totals 48 cups.",
  "source": "Household's own count, one week. The Sunday-night habit is reported, not measured.",
  "chart": "line",
  "x": { "label": "Day", "ordered": true },
  "y": { "label": "Coffee", "unit": "cups per day" }
}
```

```bash
uv run --no-project scripts/build_page.py spec.json --data rows.json --out coffee-week.html
```

```text
wrote coffee-week.html
```

### 5. Check the output

```bash
uv run --no-project scripts/check_output.py coffee-week.html
```

```text
coffee-week.html: ok
```

Read as its reader:

- The title states the claim, and the rows bear it out: Thursday 11, Monday 9.
- The y axis reads "Coffee (cups per day)" and the table header carries the same unit.
- The summary gives the numbers behind the claim: 11, 9, the weekday range, the weekend, the total.
- One series in one colour, so nothing rests on telling colours apart.

Opened from disk in headless Chrome, the page reports `data-viz="drawn"`.

### 6. Hand over

The page is `coffee-week.html` in the working directory. It needs network access to draw the chart; without it the page shows the table below and says why.

Claim: Monday runs high at 9 cups, but Thursday is the week's peak at 11, and the weekend drops to 3 and 4.

No row was dropped or combined.

The page, top to bottom:

```text
Monday runs high at 9 cups, but Thursday peaks at 11
Household of three, cups of coffee per day, Monday to Sunday, one week

[line chart: Day on x, Mon to Sun; Coffee (cups per day) on y, 3 to 11]

Thursday is the week's high at 11 cups and Monday is second at 9. Weekdays run
6 to 11 cups; Saturday and Sunday drop to 3 and 4. The week totals 48 cups.
Source: Household's own count, one week. The Sunday-night habit is reported, not measured.

Data table
```

| Day | Coffee (cups per day) |
| --- | --------------------: |
| Mon |                     9 |
| Tue |                     7 |
| Wed |                     8 |
| Thu |                    11 |
| Fri |                     6 |
| Sat |                     3 |
| Sun |                     4 |
