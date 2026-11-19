---
name: domain-analysis
description: Use before working inside or auditing an unfamiliar system, codebase, or multi-agent setup. Models what the system is for, what it does, what carries that out, and who touches each part. On request, keeps the model for a later session to extend.
compatibility: >-
  Runs without file access. A save writes a record when loaded from the
  thinkies Claude Code plugin; elsewhere the record goes in the reply for the
  user to keep.
---

# Domain analysis

Model a real system as nodes on five levels, from what it is for down to what it is made of, crossed with its grains from whole system to component. Link the nodes as means to ends and as parts of wholes, and name who acts on and sees each node.

Build the model in the conversation. Read [references/lasting-model.md](references/lasting-model.md) only when the user asks to keep or save the model, asks to reload or extend an earlier one, or hands over a model's record, and follow it alongside the steps below.

## Start

1. Settle the scope: the system, its boundary, the task the model serves, and the reading, either the domain you are about to work in or an agentic system. Take each from the request and from the system itself, and list as an open item any part of the scope you had to assume.
2. Name the system's grains, coarsest first: system, subsystem, component, or the domain's own words.

## Levels

| Level | Id word | Holds | In code | In an agentic system |
|---|---|---|---|---|
| functional purpose | purpose | what the system exists to achieve, and for whom | the outcome its users rely on | what the user wants done |
| abstract function | value | the priorities, values, and measures the purpose is judged by | budgets, service levels, invariants, policies | the user's rules, limits, and quality bars |
| generalized function | function | what must happen, whatever carries it out | validate, store, notify, schedule | plan, delegate, verify, report |
| physical function | process | what specific components can do | modules, services, jobs | named agents, tools, hooks, skills |
| physical form | form | the concrete things and where they are | files, configs, schemas, hosts | prompt files, settings, model ids, directories |

## Build

Work down from functional purpose when the purpose is known. To explain a fault, start at physical form and work up. Go as fine as the task the model serves needs and stop there.

1. **Nodes.** Place nodes at each level and grain. Give each a stable id, its level's id word, a hyphen, and a number, such as `function-3`, never reused. When the domain is code, give every physical function and physical form node the path it lives at, and mark a node with no path as unverified in its evidence.
2. **Means–ends links.** Link each node to every node one level up that it serves, as `means-of`. A node may serve several and be served by several. Test each link both ways: read upward it answers why, read downward it answers how.
3. **Part–whole links.** Link each node to the node on its own level, one grain coarser, that contains it, as `part-of`.
4. **Gaps.** A node below functional purpose that serves nothing, or a node above physical form that nothing carries out, is a gap. List each as an open item about that node.
5. **Actors.** Name each actor, of type person or agent, with the nodes it acts on and the nodes it sees. Give each the id `actor-` and a number. A node someone acts on without seeing, or a purpose or value no actor sees, is a finding.

## Show

Show the whole model in the reply in this form, then the findings and the open items, each naming its nodes. Leave a cell empty where no node sits.

```markdown
**Subject:** [system, boundary, task served, reading]

| Level | [coarsest grain] | [next grain] |
| --- | --- | --- |
| Functional purpose | [id] [name] | |
| Abstract function | [id] [name] | |
| Generalized function | | [id] [name] |
| Physical function | | [id] [name] |
| Physical form | | [id] [name] |

- Node [id] [name]: [evidence]
- Link [from] → [to] ([means-of or part-of])
- Actor [name] ([type]): acts on [ids]; sees [ids]

**Findings**

- [a finding and the nodes it names]

**Open**

- [the gap or question] (about [node ids])
```

Around it, write plain declarative sentences saying what the model shows and why each finding matters for the task the model serves. Tie each claim to a node's evidence, or mark it as an assumption.
