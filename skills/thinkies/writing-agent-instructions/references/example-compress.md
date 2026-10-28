# Example: a run of bans turned into a generator

The group, as it stood in an instruction file for an agent that edits a project's files:

> Never run `rm -rf`. Never run `git clean -f`. Never truncate a log file with `>`. Never overwrite a config file without reading it first.

## Step 1

| original line | condition | act |
| --- | --- | --- |
| Never run `rm -rf`. | about to remove a tree | forbidden |
| Never run `git clean -f`. | about to remove untracked files | forbidden |
| Never truncate a log file with `>`. | about to empty a log | forbidden |
| Never overwrite a config file without reading it first. | about to overwrite a config | read it first, then allowed |

## Step 2

The acts vary: three forbid, one gates on a read. Axis 1, the feature the acts vary with, gives nothing visible, since "forbidden" and "gated" are the acts themselves. Axis 2, what the banned items share: each discards content with no copy left anywhere. Axis 3, where the result ends up: after `rm -rf`, `git clean -f`, and `> log`, the content is nowhere; after an overwrite with a prior read, the content is in the reader's context.

Axis 3 works. Its values are "the prior content survives somewhere a later step can reach" and "the prior content is gone".

## Step 3

Domain: every command that removes or replaces content on disk. Membership test: after the command, is some content that was on disk before it no longer on disk?

Mapping: Remove or replace content on disk only where a copy of the prior content survives where a later step can reach it, in version control, in a diff, or in the message that reports the change.

Anchor: none needed yet.

Closure: clear member, `rm -rf build/`; clear non-member, `ls`; borderline, `git checkout -- src/app.ts`, which replaces the working copy with the committed one. The test decides it from what is visible, since the edits on disk before the command are gone after it, so it is in. Closed.

## Trace

| original line | axis value read off it | arm taken | act the generator yields | result | kept as |
| --- | --- | --- | --- | --- | --- |
| Never run `rm -rf`. | "removes a tree, no copy" | no copy survives | forbidden | holds | |
| Never run `git clean -f`. | "removes untracked files, no copy" | no copy survives | forbidden | holds | |
| Never truncate a log file with `>`. | "empties a log, no copy" | no copy survives | forbidden | holds | |
| Never overwrite a config file without reading it first. | "overwrites a config; a read puts the prior content in context" | copy survives in the message that reports the change | allowed after the read, and the prior content goes in the report | bends | |

The last row bends. The original asked only for a read; the generator asks that the copy survive where a later step can reach it, and a read alone puts the content in a context window that the next session loses. The expansion reached the act through a feature the original never named.

Repair, to the generator: "a copy of the prior content survives where a later step can reach it" already says it. Repair, to the residue: none, since the generator's act is stricter than the original by one duty, reporting the prior content. That stricter act is a yielded directive nobody wrote, so it goes to the approval list rather than silently in.

## Edge

| new case | axis value | act the generator yields | another line already decides it | agreement |
| --- | --- | --- | --- | --- |
| `git checkout -- src/app.ts` on a file with edits | edits gone, no copy | forbidden unless the edits are committed or reported first | none | for approval |
| `mv notes.md notes.old.md` | content survives under the new name | allowed | none | for approval |
| `sed -i 's/foo/bar/' config.yaml` | prior line gone; a diff shows it where the file is tracked | allowed where tracked, forbidden where untracked | none | for approval |

Each row is a directive the original never gave. The third row shows the generator yielding a split act on one command, which the writer of the original may or may not want; it goes up as written.

## Two readings and Terms

Literal reading of "survives where a later step can reach it": the content must be on disk or in version control. Charitable reading: the content in the agent's own message counts. The two readings differ on the config row. Repair: name the places, as the mapping now does, "in version control, in a diff, or in the message that reports the change". Rerun the trace: the config row now holds, with the report duty as the yielded act.

Term search: the file elsewhere uses "content" for the body of a pull request. Qualify the generator's term to "prior content on disk".

## Size

The original group runs to four sentences. The generator runs to one sentence plus its place list. Shorter, and it covers `checkout --`, `mv`, and `sed -i`, which the group never reached.

## The output

Generator:

> Remove or replace prior content on disk only where a copy of it survives in version control, in a diff, or in the message that reports the change.

Residue: none.

For approval: the three edge rows, and the report duty on config overwrites.

Dropped: none.

The contrast to notice is that the original four bans said nothing about `mv` or `sed -i`, and a reader of the bans would have run either without a thought. The generator decides both, and the decision is visible on the approval list before it lands.
