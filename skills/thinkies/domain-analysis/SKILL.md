---
name: domain-analysis
description: Use before working inside or auditing an unfamiliar system, codebase, or multi-agent setup. Models what the system is for, what it does, what carries that out, and who touches each part, and extends an earlier model when handed one.
compatibility: >-
  Runs without file access. A save writes a record when loaded from the
  thinkies Claude Code plugin; elsewhere the record goes in the reply for the
  user to keep.
---

# Domain analysis

Model a real system as nodes on five levels, from what it is for down to what it is made of, crossed with its grains from whole system to component. Link the nodes as means to ends and as parts of wholes, and name who acts on and sees each node. The nodes, links, and actors are the run's record, so a later run can load a saved model and extend it.

## Start

1. Start a new model, unless the user asks to resume or extend an earlier one or hands over its record. To resume, load the record as Record directs, from the store by the topic that names this system or from the conversation, and take the latest line for each node, link, and actor as the current model. Answer its open lines before adding anything new.
2. Settle the scope, which becomes the record's subject: the system, its boundary, the task the model serves, and the reading, either the domain you are about to work in or an agentic system. Take each from the request and from the system itself, and hold as an open item any part of the scope you had to assume.
3. Name the system's grains, coarsest first: system, subsystem, component, or the domain's own words.

## Levels

| Level | Id word | Holds | In code | In an agentic system |
|---|---|---|---|---|
| functional purpose | purpose | what the system exists to achieve, and for whom | the outcome its users rely on | what the user wants done |
| abstract function | value | the priorities, values, and measures the purpose is judged by | budgets, service levels, invariants, policies | the user's rules, limits, and quality bars |
| generalized function | function | what must happen, whatever carries it out | validate, store, notify, schedule | plan, delegate, verify, report |
| physical function | process | what specific components can do | modules, services, jobs | named agents, tools, hooks, skills |
| physical form | form | the concrete things and where they are | files, configs, schemas, hosts | prompt files, settings, model ids, directories |

## Build

Work down from functional purpose when the purpose is known. To explain a fault, start at physical form and work up. Go as fine as the task the model serves needs and stop there, since a later run can extend the record.

1. **Nodes.** Place nodes at each level and grain. Give each a stable id, its level's id word, a hyphen, and a number, such as `function-3`, never reused. Write the level's name, as the table gives it, in the node's `level`. When the domain is code, give every physical function and physical form node the path it lives at, and mark a node with no path as unverified in its evidence.
2. **Means–ends links.** Link each node to every node one level up that it serves, with `rel` set to `means-of`. A node may serve several and be served by several. Test each link both ways: read upward it answers why, read downward it answers how.
3. **Part–whole links.** Link each node to the node on its own level, one grain coarser, that contains it, with `rel` set to `part-of`.
4. **Gaps.** A node below functional purpose that serves nothing, or a node above physical form that nothing carries out, is a gap. Hold each as an open item about that node.
5. **Actors.** Name each actor, of type person or agent, with the nodes it acts on and the nodes it sees. Give each the id `actor-` and a number. A node someone acts on without seeing, or a purpose or value no actor sees, is a finding.

In a saved record, a correction is a new line with the same id, and a removal is a line with `"retired": true`.

## Show

Show the whole model in the reply in the form of [assets/playback.md](assets/playback.md), with the Model part first and then the findings and open items, each naming its nodes. Around it, write plain declarative sentences saying what the model shows and why each finding matters for the task the model serves. Tie each claim to a node's evidence, or mark it as an assumption.

## Record

Hold the run's record in mind as you work: the subject, what was given, the notes, the results, and what stays open. Those parts organize the thinking, and the reply gives them in prose. A plain run ends there: it writes no file, shows no record lines, and says nothing about saving.

Save the record only when the user asks to save or keep the run, or resumes a saved one. The rest of this section applies only then.

Records live in the store, `${CLAUDE_PLUGIN_DATA}/records/`, with a copy in the mirror folder, `${user_config.records_mirror}`.

- When the store path is not absolute, or no tool here writes files, no store is reachable. Give the record in the reply instead, in a `jsonl` block under its file name, for the user to keep.
- When the mirror path is empty or still a placeholder, skip the mirror. Otherwise, after the run's last line, copy the record file into the mirror under the same name.
- Create either folder when it is missing.

Write each record in the form of the template at the end of this section: the file name as shown, then one JSON object per line, one line per event, in the order the events happen, with every bracketed value replaced. Write a kind as often as the run produces it, and leave out kinds it does not produce. Take times from the clock in UTC, for example `date -u +%Y%m%dT%H%M%SZ` for the file name. Where no clock can be read, take the date from the conversation and write the time of day as zeros. A topic is two to six lowercase words joined by hyphens. An answer's `q` names the question or open item it answers.

- Append lines; never change or remove one.
- Where lines share an id, the latest wins. A link's id is its from, to, and rel. `"retired": true` removes the entry.
- To resume a run, read its file, first copying it from the mirror when only the mirror holds it, or take the record the user pastes. Append a run line with `"resumed": true`, then the lines the resumed run adds.
- An agent answering a record's questions appends its answer, skip, and open lines to the same file and names itself in `by`.

After saving, play the record back in the form of [assets/playback.md](assets/playback.md): the path it was saved to, then every part the reply has not already shown. Show raw lines only in the `jsonl` block that stands in for an unreachable store.

Record the scope as the subject; each node, link, and actor as its own line as you place it; each gap as an open line about its nodes; each finding as a result; and, on resume, each answered open item as an answer line.

File: `domain-analysis_[start time, UTC, YYYYMMDDTHHMMSSZ]_[topic].jsonl`

```jsonl
{"kind": "run", "at": "[time, UTC, YYYY-MM-DDTHH:MM:SSZ]", "skill": "domain-analysis", "topic": "[topic]", "subject": "[system, boundary, task served, reading]", "project": "[repository or project name, or empty]", "resumed": false}
{"kind": "node", "at": "[time]", "id": "function-1", "level": "generalized function", "grain": "[grain name]", "name": "[what must happen]", "evidence": "[where this is shown]", "retired": false}
{"kind": "node", "at": "[time]", "id": "process-1", "level": "physical function", "grain": "[grain name]", "name": "[component]", "evidence": "[path, or unverified: why]", "retired": false}
{"kind": "link", "at": "[time]", "from": "process-1", "to": "function-1", "rel": "means-of", "retired": false}
{"kind": "link", "at": "[time]", "from": "process-1", "to": "process-2", "rel": "part-of", "retired": false}
{"kind": "actor", "at": "[time]", "id": "actor-1", "name": "[who]", "type": "[person or agent]", "acts_on": ["process-1"], "sees": ["function-1"], "retired": false}
{"kind": "open", "at": "[time]", "id": "open-1", "text": "[the gap or question]", "about": ["function-1"]}
{"kind": "answer", "at": "[time]", "q": "open-1", "text": "[the answer]", "by": "[who answered]"}
{"kind": "result", "at": "[time]", "text": "[a finding and the nodes it names]"}
```
