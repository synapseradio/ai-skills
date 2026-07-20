Good spec to start from, but it leaves a fair number of decisions open that will each shape the data model, scheduler, and UI. Here's what I'd get from the product owner before writing code:

**Scope of "dashboard data"**

- If a user has more than one dashboard, do they pick which one to schedule, or is there a single fixed dashboard being exported?
- What time window does each export cover — a live snapshot at generation time, a fixed period like "last 7 days," or "everything since the last export"?

**Frequency & timing**

- What exact frequency options do we support — daily, weekly, monthly, a custom day-of-week/day-of-month?
- Whose timezone defines "overnight" and "next morning" — the user's account/profile timezone, or a fixed server time?

**Format**

- Does the PDF need to visually mirror the dashboard (charts, layout, branding), or is it a formatted table like the CSV, just rendered as a PDF? This one materially changes scope.

**Delivery & failure handling**

- Is the export sent as an email attachment, or as a link to download it? (Matters for attachment size limits and whether sensitive data should even go over email as a file.)
- If generation or sending fails on a given night, do we retry, skip and notify the user, or fail silently and just try again next cycle?

**Lifecycle**

- Can a user have more than one schedule at a time, and can they edit or pause one after creating it, or is it create/delete only?

That's the set I'd want answered before touching the scheduler or data model — the timezone, data-window, and PDF-fidelity questions in particular are the ones most likely to bite you late if assumed wrong.
