# Playback

Show each record in this form. Leave out any heading with nothing under it, the "Saved to" line for a record no one saved, and the "Copied to" sentence where no mirror copy was made. For node, link, and actor lines, show only the latest line for each id, and leave out retired entries. Leave out open items that an answer line closes.

---

### [skill] · [topic, with spaces for hyphens] · [start date and time, local]

Saved to `[record path]`. Copied to `[mirror path]`.

Project: [project]

**Subject:** [subject]

**Given**

- [text] ([source])

**Questions and answers**

1. [question text]

   [answer text] ([by])

2. [question text]

   Skipped: [reason]

**Notes**

- [note text] ([context])

**Results**

- [result text]

**Model**

| Level | [coarsest grain] | [next grain] |
| --- | --- | --- |
| Functional purpose | [id] [name] | |
| Abstract function | [id] [name] | |
| Generalized function | | [id] [name] |
| Physical function | | [id] [name] |
| Physical form | | [id] [name] |

- Node [id] [name]: [evidence]
- Link [from] → [to] ([rel])
- Actor [name] ([type]): acts on [ids]; sees [ids]

**Open**

- [id]: [text] (about [question or node ids])

**Resumed** [date and time, local]: [what the resumed run added]

---

When a save was asked for and no store is reachable, replace the "Saved to" line with "No store is reachable here. Keep the record below as `[file name]`." and put the record after the playback in a `jsonl` block.
