# domain-analysis: a garage tool library

- skill: domain-analysis, from commit 0c9258f
- subject: A neighbourhood tool library run out of a garage: members borrow drills, ladders, and a single much-loved pressure washer; volunteers keep a paper ledger and a group chat.
- kind: single run

## Prompt

/domain-analysis A neighbourhood tool library run out of a garage: members borrow drills, ladders, and a single much-loved pressure washer; volunteers keep a paper ledger and a group chat.

## Run

No store exists here, so there was no earlier record of this system to resume. The scope for this run: the system is the tool library, its boundary is the garage, the volunteers, the members, and the two record-keeping channels named in the subject (paper ledger, group chat). The task the model serves is deciding where to improve how loans and the washer queue are tracked without adding volunteer hours. The reading is a domain, not an agentic system. The grains, coarsest first, are library, workstream, and item. The subject names only the garage, the three kinds of tool, the ledger, the chat, and the volunteers. Every node that goes beyond those carries "assumed" in its evidence, and each should be confirmed with the volunteers.

### domain-analysis · garage-tool-library · 2026-09-30 01:11

Not saved: no store here. Keep the record below as `domain-analysis_20260929T231022Z_garage-tool-library.jsonl`.

Project: none

**Subject:** The tool library (boundary: the garage, its volunteers and members, the paper ledger and the group chat), modelled to decide where loan and washer-queue tracking should improve without adding volunteer hours; a domain reading.

**Model**

The grid reads down from why the library exists to what it is made of. Each column is a grain, from the whole library to its individual items. The three columns are the same system seen coarse, middle, and fine.

| Level | Library | Workstream | Item |
| --- | --- | --- | --- |
| Functional purpose | purpose-1 Neighbours use tools they need only occasionally without each buying their own<br>purpose-2 Neighbours come to know and trust each other | | |
| Abstract function | value-1 Every tool comes back and works for the next borrower<br>value-2 Fair access across households<br>value-3 Borrowers stay safe on ladders and power tools<br>value-4 Running the library costs volunteers little time and neighbours nothing | | value-5 Everyone who asks for the washer gets it within a week |
| Generalized function | function-1 Circulate the stock and keep it usable | function-2 Allocate a tool to a borrower for a period<br>function-3 Record what is out, with whom, due when<br>function-4 Take tools back and check their condition<br>function-5 Repair and maintain tools<br>function-6 Tell members what is available, due, and changed<br>function-7 Admit members and know who they are<br>function-8 Acquire and replace tools | function-9 Hand out the washer in turn |
| Physical function | process-1 Volunteer-run garage lending | process-2 Desk shift: hand-out and return in opening hours<br>process-3 Group chat coordination<br>process-4 Repair session | process-5 Ledger entry: name, tool, date out; struck on return<br>process-6 Sign-up at the desk<br>process-7 Washer queue: ask in chat, a volunteer replies with a slot<br>process-8 Look-over of ladders and drills on return |
| Physical form | form-1 The garage<br>form-2 The group chat thread | form-3 Tool wall and shelves<br>form-4 Front table<br>form-5 Repair bench and parts box | form-6 Paper ledger notebook<br>form-7 Member list pages<br>form-8 The pressure washer<br>form-9 Drills and ladders |

- Node purpose-1 Neighbours use tools they need only occasionally without each buying their own: given in the subject (members borrow tools)
- Node purpose-2 Neighbours come to know and trust each other: assumed; the subject does not state it, and it is what a neighbourhood library usually also does
- Node value-1 Every tool comes back and works for the next borrower: assumed; a ledger exists to make return checkable; measures would be tools lost or broken per year and days out past due
- Node value-2 Fair access across households: assumed; measure would be loans per household
- Node value-3 Borrowers stay safe on ladders and power tools: assumed; measure would be incidents per year
- Node value-4 Running the library costs volunteers little time and neighbours nothing: assumed; measure would be volunteer hours per week
- Node value-5 Everyone who asks for the washer gets it within a week: assumed from "single much-loved"; measure would be days from request to slot
- Node function-1 Circulate the stock and keep it usable: assumed grouping of functions 2 to 9
- Node function-2 Allocate a tool to a borrower for a period: given (members borrow tools)
- Node function-3 Record what is out, with whom, due when: given (paper ledger)
- Node function-4 Take tools back and check their condition: assumed
- Node function-5 Repair and maintain tools: assumed
- Node function-6 Tell members what is available, due, and changed: given (group chat)
- Node function-7 Admit members and know who they are: given (the subject says "members")
- Node function-8 Acquire and replace tools: assumed; no carrier is named anywhere (see open-1)
- Node function-9 Hand out the washer in turn: assumed from "single much-loved"
- Node process-1 Volunteer-run garage lending: given (volunteers, garage)
- Node process-2 Desk shift: hand-out and return in opening hours: assumed; the subject does not say hand-out is staffed (open-4)
- Node process-3 Group chat coordination: given (group chat)
- Node process-4 Repair session: assumed (open-4)
- Node process-5 Ledger entry: name, tool, date out; struck on return: given that a paper ledger exists; the entry format is assumed
- Node process-6 Sign-up at the desk: assumed
- Node process-7 Washer queue: ask in chat, a volunteer replies with a slot: assumed from the chat and the single washer
- Node process-8 Look-over of ladders and drills on return: assumed
- Node form-1 The garage: given
- Node form-2 The group chat thread: given
- Node form-3 Tool wall and shelves: assumed
- Node form-4 Front table: assumed
- Node form-5 Repair bench and parts box: assumed
- Node form-6 Paper ledger notebook: given
- Node form-7 Member list pages: assumed; where the member list lives is open (open-3)
- Node form-8 The pressure washer: given
- Node form-9 Drills and ladders: given
- Link value-1 → purpose-1 (means-of)
- Link value-2 → purpose-1 (means-of)
- Link value-2 → purpose-2 (means-of)
- Link value-3 → purpose-1 (means-of)
- Link value-4 → purpose-1 (means-of)
- Link value-5 → purpose-1 (means-of)
- Link value-5 → purpose-2 (means-of)
- Link function-1 → value-1 (means-of)
- Link function-1 → value-2 (means-of)
- Link function-1 → value-3 (means-of)
- Link function-1 → value-4 (means-of)
- Link function-2 → value-1 (means-of)
- Link function-2 → value-2 (means-of)
- Link function-3 → value-1 (means-of)
- Link function-3 → value-2 (means-of)
- Link function-4 → value-1 (means-of)
- Link function-4 → value-3 (means-of)
- Link function-5 → value-1 (means-of)
- Link function-5 → value-3 (means-of)
- Link function-5 → value-4 (means-of)
- Link function-6 → value-1 (means-of)
- Link function-6 → value-2 (means-of)
- Link function-7 → value-1 (means-of)
- Link function-7 → value-2 (means-of)
- Link function-8 → value-1 (means-of)
- Link function-9 → value-2 (means-of)
- Link function-9 → value-5 (means-of)
- Link process-1 → function-1 (means-of)
- Link process-2 → function-2 (means-of)
- Link process-2 → function-4 (means-of)
- Link process-2 → function-7 (means-of)
- Link process-3 → function-2 (means-of)
- Link process-3 → function-6 (means-of)
- Link process-4 → function-5 (means-of)
- Link process-5 → function-3 (means-of)
- Link process-6 → function-7 (means-of)
- Link process-7 → function-2 (means-of)
- Link process-7 → function-9 (means-of)
- Link process-8 → function-4 (means-of)
- Link form-1 → process-1 (means-of)
- Link form-1 → process-2 (means-of)
- Link form-2 → process-3 (means-of)
- Link form-2 → process-7 (means-of)
- Link form-3 → process-2 (means-of)
- Link form-3 → process-8 (means-of)
- Link form-4 → process-2 (means-of)
- Link form-5 → process-4 (means-of)
- Link form-6 → process-5 (means-of)
- Link form-7 → process-6 (means-of)
- Link form-8 → process-7 (means-of)
- Link form-9 → process-2 (means-of)
- Link form-9 → process-8 (means-of)
- Link value-5 → value-2 (part-of)
- Link function-2 → function-1 (part-of)
- Link function-3 → function-1 (part-of)
- Link function-4 → function-1 (part-of)
- Link function-5 → function-1 (part-of)
- Link function-6 → function-1 (part-of)
- Link function-7 → function-1 (part-of)
- Link function-8 → function-1 (part-of)
- Link function-9 → function-2 (part-of)
- Link process-2 → process-1 (part-of)
- Link process-3 → process-1 (part-of)
- Link process-4 → process-1 (part-of)
- Link process-5 → process-2 (part-of)
- Link process-6 → process-2 (part-of)
- Link process-8 → process-2 (part-of)
- Link process-7 → process-3 (part-of)
- Link form-3 → form-1 (part-of)
- Link form-4 → form-1 (part-of)
- Link form-5 → form-1 (part-of)
- Link form-6 → form-4 (part-of)
- Link form-7 → form-4 (part-of)
- Link form-8 → form-3 (part-of)
- Link form-9 → form-3 (part-of)
- Actor Borrower (person): acts on process-7, form-2, form-8, form-9; sees purpose-1, value-5, function-6, process-7, form-1, form-2, form-8, form-9
- Actor Desk volunteer (person): acts on process-2, process-5, process-6, process-8, form-4, form-6, form-7; sees function-3, function-4, function-7, form-1, form-3, form-6, form-8, form-9
- Actor Chat volunteer (person): acts on process-3, process-7, form-2; sees function-2, function-6, form-2
- Actor Repair volunteer (person): acts on process-4, form-5, form-8, form-9; sees function-5, form-5, form-9

**Results**

- The values value-1, value-2, value-3, and value-4 and the purpose purpose-2 are seen by no actor. The only value anyone sees is value-5, the washer wait, and only the borrower sees it. Lost or broken tools, fairness across households, incidents, and volunteer hours have no one looking at them, so nothing in the model would tell the volunteers that any of them is going wrong. This matters for the task because any change to tracking has to decide first whose eyes it is meant to feed.
- function-3 (record what is out) is carried only by process-5 on form-6. function-9 (the washer's turn order) is carried only by process-7 on form-2. Two records of who has what therefore exist: the ledger, seen at the garage, and the chat, seen on phones. The desk volunteer sees function-3 but not function-2 or function-6, and the chat volunteer sees function-2 and function-6 but not function-3. The subject does not say whether the two are reconciled (open-5), so this is an assumption to test: a washer that the chat says is free and the ledger says is out is possible in this structure.
- form-6, the ledger notebook, is the single carrier of function-3, and form-8 is the single carrier of function-9. Losing or damaging either leaves no fallback in the model. The washer is also the one tool the model treats as a queue (process-7), because it is one physical item serving every household.
- function-8 (acquire and replace tools) is a gap: it serves value-1 and no process carries it out. Because the library's stock only shrinks through loss and wear, this gap sits under the very value (value-1) that nobody watches.
- Three of the four volunteer roles, and processes process-2, process-4, process-6, and process-8, rest on assumptions. Findings that depend on them (the split between desk and chat volunteers, the single-carrier reading of form-6) hold only as far as those assumptions do.

**Open**

- open-1: function-8 has no process that carries it out; who decides to replace a lost drill or buy another washer, and with what money? (about function-8)
- open-2: Who sees the measures for value-1, value-2, value-3, and value-4, if anyone does? (about value-1, value-2, value-3, value-4)
- open-3: Where does the member list live: in the ledger, in the chat, or elsewhere? (about form-7, process-6, function-7)
- open-4: Is there a staffed desk shift and a repair session, or does lending happen by arrangement through the chat alone? (about process-2, process-4)
- open-5: Do volunteers reconcile the ledger and the chat, and how? (about form-6, form-2, function-3)

```jsonl
{"kind": "run", "at": "2026-09-29T23:10:22Z", "skill": "domain-analysis", "topic": "garage-tool-library", "subject": "The tool library (boundary: the garage, its volunteers and members, the paper ledger and the group chat), modelled to decide where loan and washer-queue tracking should improve without adding volunteer hours; a domain reading.", "project": "", "resumed": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "purpose-1", "level": "functional purpose", "grain": "library", "name": "Neighbours use tools they need only occasionally without each buying their own", "evidence": "given in the subject (members borrow tools)", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "purpose-2", "level": "functional purpose", "grain": "library", "name": "Neighbours come to know and trust each other", "evidence": "assumed; not stated in the subject", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "value-1", "level": "abstract function", "grain": "library", "name": "Every tool comes back and works for the next borrower", "evidence": "assumed; measures: tools lost or broken per year, days out past due", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "value-2", "level": "abstract function", "grain": "library", "name": "Fair access across households", "evidence": "assumed; measure: loans per household", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "value-3", "level": "abstract function", "grain": "library", "name": "Borrowers stay safe on ladders and power tools", "evidence": "assumed; measure: incidents per year", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "value-4", "level": "abstract function", "grain": "library", "name": "Running the library costs volunteers little time and neighbours nothing", "evidence": "assumed; measure: volunteer hours per week", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "value-5", "level": "abstract function", "grain": "item", "name": "Everyone who asks for the washer gets it within a week", "evidence": "assumed from the single much-loved washer; measure: days from request to slot", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "function-1", "level": "generalized function", "grain": "library", "name": "Circulate the stock and keep it usable", "evidence": "assumed grouping of function-2 to function-9", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "function-2", "level": "generalized function", "grain": "workstream", "name": "Allocate a tool to a borrower for a period", "evidence": "given in the subject (members borrow tools)", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "function-3", "level": "generalized function", "grain": "workstream", "name": "Record what is out, with whom, due when", "evidence": "given in the subject (paper ledger)", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "function-4", "level": "generalized function", "grain": "workstream", "name": "Take tools back and check their condition", "evidence": "assumed", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "function-5", "level": "generalized function", "grain": "workstream", "name": "Repair and maintain tools", "evidence": "assumed", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "function-6", "level": "generalized function", "grain": "workstream", "name": "Tell members what is available, due, and changed", "evidence": "given in the subject (group chat)", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "function-7", "level": "generalized function", "grain": "workstream", "name": "Admit members and know who they are", "evidence": "given in the subject (members)", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "function-8", "level": "generalized function", "grain": "workstream", "name": "Acquire and replace tools", "evidence": "assumed; no carrier named", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "function-9", "level": "generalized function", "grain": "item", "name": "Hand out the washer in turn", "evidence": "assumed from the single much-loved washer", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "process-1", "level": "physical function", "grain": "library", "name": "Volunteer-run garage lending", "evidence": "given in the subject (volunteers, garage)", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "process-2", "level": "physical function", "grain": "workstream", "name": "Desk shift: hand-out and return in opening hours", "evidence": "assumed; not stated in the subject", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "process-3", "level": "physical function", "grain": "workstream", "name": "Group chat coordination", "evidence": "given in the subject (group chat)", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "process-4", "level": "physical function", "grain": "workstream", "name": "Repair session", "evidence": "assumed; not stated in the subject", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "process-5", "level": "physical function", "grain": "item", "name": "Ledger entry: name, tool, date out; struck on return", "evidence": "paper ledger given in the subject; entry format assumed", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "process-6", "level": "physical function", "grain": "item", "name": "Sign-up at the desk", "evidence": "assumed", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "process-7", "level": "physical function", "grain": "item", "name": "Washer queue: ask in chat, a volunteer replies with a slot", "evidence": "assumed from the chat and the single washer", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "process-8", "level": "physical function", "grain": "item", "name": "Look-over of ladders and drills on return", "evidence": "assumed", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "form-1", "level": "physical form", "grain": "library", "name": "The garage", "evidence": "given in the subject", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "form-2", "level": "physical form", "grain": "library", "name": "The group chat thread", "evidence": "given in the subject", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "form-3", "level": "physical form", "grain": "workstream", "name": "Tool wall and shelves", "evidence": "assumed", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "form-4", "level": "physical form", "grain": "workstream", "name": "Front table", "evidence": "assumed", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "form-5", "level": "physical form", "grain": "workstream", "name": "Repair bench and parts box", "evidence": "assumed", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "form-6", "level": "physical form", "grain": "item", "name": "Paper ledger notebook", "evidence": "given in the subject", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "form-7", "level": "physical form", "grain": "item", "name": "Member list pages", "evidence": "assumed; location of the member list is open-3", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "form-8", "level": "physical form", "grain": "item", "name": "The pressure washer", "evidence": "given in the subject", "retired": false}
{"kind": "node", "at": "2026-09-29T23:11:19Z", "id": "form-9", "level": "physical form", "grain": "item", "name": "Drills and ladders", "evidence": "given in the subject", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "value-1", "to": "purpose-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "value-2", "to": "purpose-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "value-2", "to": "purpose-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "value-3", "to": "purpose-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "value-4", "to": "purpose-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "value-5", "to": "purpose-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "value-5", "to": "purpose-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-1", "to": "value-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-1", "to": "value-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-1", "to": "value-3", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-1", "to": "value-4", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-2", "to": "value-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-2", "to": "value-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-3", "to": "value-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-3", "to": "value-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-4", "to": "value-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-4", "to": "value-3", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-5", "to": "value-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-5", "to": "value-3", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-5", "to": "value-4", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-6", "to": "value-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-6", "to": "value-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-7", "to": "value-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-7", "to": "value-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-8", "to": "value-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-9", "to": "value-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-9", "to": "value-5", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-1", "to": "function-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-2", "to": "function-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-2", "to": "function-4", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-2", "to": "function-7", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-3", "to": "function-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-3", "to": "function-6", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-4", "to": "function-5", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-5", "to": "function-3", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-6", "to": "function-7", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-7", "to": "function-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-7", "to": "function-9", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-8", "to": "function-4", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-1", "to": "process-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-1", "to": "process-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-2", "to": "process-3", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-2", "to": "process-7", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-3", "to": "process-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-3", "to": "process-8", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-4", "to": "process-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-5", "to": "process-4", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-6", "to": "process-5", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-7", "to": "process-6", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-8", "to": "process-7", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-9", "to": "process-2", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-9", "to": "process-8", "rel": "means-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "value-5", "to": "value-2", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-2", "to": "function-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-3", "to": "function-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-4", "to": "function-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-5", "to": "function-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-6", "to": "function-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-7", "to": "function-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-8", "to": "function-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "function-9", "to": "function-2", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-2", "to": "process-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-3", "to": "process-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-4", "to": "process-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-5", "to": "process-2", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-6", "to": "process-2", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-8", "to": "process-2", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "process-7", "to": "process-3", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-3", "to": "form-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-4", "to": "form-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-5", "to": "form-1", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-6", "to": "form-4", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-7", "to": "form-4", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-8", "to": "form-3", "rel": "part-of", "retired": false}
{"kind": "link", "at": "2026-09-29T23:11:19Z", "from": "form-9", "to": "form-3", "rel": "part-of", "retired": false}
{"kind": "actor", "at": "2026-09-29T23:11:19Z", "id": "actor-1", "name": "Borrower", "type": "person", "acts_on": ["process-7", "form-2", "form-8", "form-9"], "sees": ["purpose-1", "value-5", "function-6", "process-7", "form-1", "form-2", "form-8", "form-9"], "retired": false}
{"kind": "actor", "at": "2026-09-29T23:11:19Z", "id": "actor-2", "name": "Desk volunteer", "type": "person", "acts_on": ["process-2", "process-5", "process-6", "process-8", "form-4", "form-6", "form-7"], "sees": ["function-3", "function-4", "function-7", "form-1", "form-3", "form-6", "form-8", "form-9"], "retired": false}
{"kind": "actor", "at": "2026-09-29T23:11:19Z", "id": "actor-3", "name": "Chat volunteer", "type": "person", "acts_on": ["process-3", "process-7", "form-2"], "sees": ["function-2", "function-6", "form-2"], "retired": false}
{"kind": "actor", "at": "2026-09-29T23:11:19Z", "id": "actor-4", "name": "Repair volunteer", "type": "person", "acts_on": ["process-4", "form-5", "form-8", "form-9"], "sees": ["function-5", "form-5", "form-9"], "retired": false}
{"kind": "open", "at": "2026-09-29T23:11:19Z", "id": "open-1", "text": "function-8 has no process that carries it out; who decides to replace a lost drill or buy another washer, and with what money?", "about": ["function-8"]}
{"kind": "open", "at": "2026-09-29T23:11:19Z", "id": "open-2", "text": "Who sees the measures for value-1, value-2, value-3, and value-4, if anyone does?", "about": ["value-1", "value-2", "value-3", "value-4"]}
{"kind": "open", "at": "2026-09-29T23:11:19Z", "id": "open-3", "text": "Where does the member list live: in the ledger, in the chat, or elsewhere?", "about": ["form-7", "process-6", "function-7"]}
{"kind": "open", "at": "2026-09-29T23:11:19Z", "id": "open-4", "text": "Is there a staffed desk shift and a repair session, or does lending happen by arrangement through the chat alone?", "about": ["process-2", "process-4"]}
{"kind": "open", "at": "2026-09-29T23:11:19Z", "id": "open-5", "text": "Do volunteers reconcile the ledger and the chat, and how?", "about": ["form-6", "form-2", "function-3"]}
{"kind": "result", "at": "2026-09-29T23:11:19Z", "text": "value-1, value-2, value-3, value-4 and purpose-2 are seen by no actor; only value-5 is seen, and only by the borrower."}
{"kind": "result", "at": "2026-09-29T23:11:19Z", "text": "function-3 is carried only by process-5 on form-6 and function-9 only by process-7 on form-2, so two records of who has what exist (ledger and chat); whether they are reconciled is open-5."}
{"kind": "result", "at": "2026-09-29T23:11:19Z", "text": "form-6 is the single carrier of function-3 and form-8 the single carrier of function-9; neither has a fallback in the model."}
{"kind": "result", "at": "2026-09-29T23:11:19Z", "text": "function-8 is a gap: it serves value-1 and no process carries it out."}
{"kind": "result", "at": "2026-09-29T23:11:19Z", "text": "process-2, process-4, process-6, process-8, form-3, form-4, form-5 and form-7 are assumed; findings that rest on them hold only as far as those assumptions do."}
```
