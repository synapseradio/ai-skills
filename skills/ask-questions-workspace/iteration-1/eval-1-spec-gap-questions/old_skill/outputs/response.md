Here's a set of questions organized by where guessing wrong would cost you the most rework:

**What actually gets exported**

1. When an export runs, does it capture the exact filters/date range the user had set on the dashboard, or a fixed default view?
2. Is this tied to one specific dashboard, or can a user choose which dashboard to export — and can they have more than one schedule active at once?

**Scheduling mechanics**
3. What frequency options need to exist — daily/weekly/monthly, or should users be able to pick a custom interval or specific day?
4. "Overnight" and "next morning" — whose timezone governs that: each user's local time, or one server time for everyone?

**Delivery & failure handling**
5. If the export fails to generate, or the email fails to send, what should happen — retry, notify the user, or just log it?
6. For the PDF format, does it need to visually replicate the dashboard's charts and layout, or is a plain data table acceptable?
7. Is the export always emailed to the account owner, or should users be able to add other recipients?

Questions 3–4 and 5–6 are the ones most likely to change your architecture (scheduler design, job retry logic, PDF rendering approach), so I'd push for answers to those before writing any code — the rest can probably be reasonable defaults you confirm along the way.
