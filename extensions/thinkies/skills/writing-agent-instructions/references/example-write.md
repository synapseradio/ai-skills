# Example: an instruction written from incidents

The ask, in conversation: "the agent keeps running long test suites in the foreground and the session hangs. add something to CLAUDE.md so it stops doing that."

## Step 1, the reader and the cost

A mid-tier coding agent reads this, acting on every shell command it runs. A wrong act costs the session a hung turn, and the person waiting on it the time until they notice.

## Step 2, the cases

| condition | act |
| --- | --- |
| running the full test suite | start it in the background and go on |
| starting a dev server | start it in the background and go on |
| running a single fast test | run it in the foreground |
| waiting on a CI run to finish | run the command that blocks on it in the background |
| watching a log with `tail -f` | do not; read the log once with a command that exits |
| polling with `sleep` in a loop | do not; let the harness resume the session when the command exits |

The first row is the incident. The others came from asking what else hangs a session and what does not.

## Step 3, the axis

Axis 1, the feature the acts vary with: whether the command's end is in sight when it starts. The full suite, the server, the CI wait, the `tail -f`, and the `sleep` loop all run until something outside the command stops them or for longer than a turn should wait. The single fast test ends on its own within the turn.

Axis 1 is visible on the command, so it is the axis. Its values are "ends on its own within the turn" and "runs past the turn or until stopped".

## Step 4, the four parts

Domain: every shell command the agent starts.

Mapping, in prose since there are two arms: Where the command ends on its own within the turn, run it in the foreground. Otherwise, start it in the background, do the work that does not depend on its result, and end the turn, letting the harness resume the session when the command exits.

Expansion rule: implicit in "Where ... Otherwise".

Anchor: none, since the two values leave no second reading.

## Step 5, wording

The two "do not" rows become omissions: "Keep `sleep` and every command that runs until stopped, `tail -f` for one, out of every wait." The polling fact becomes a stance: "Count a check run again to see whether the state changed as polling."

## Step 6, the checks

Closure: member, `bun test`; non-member, a file read through a tool that is not the shell; borderline, `gh run watch`, which the domain sentence takes in since it is a shell command. Closed.

Visibility: "ends on its own within the turn" is a judgment on commands the agent has not run before. Gloss added: "Count a command as running past the turn where it watches, serves, polls, or runs a whole suite."

Trace, on the six cases: every row holds. The `tail -f` row holds through the omission, which is residue of the attached-duty form, since the generator alone would background `tail -f` rather than forbid it.

Edge: `npm install` on a large tree, which ends on its own but slowly; the generator says foreground, and the tool's own timeout bounds it. `docker compose up` without `-d`: runs until stopped, so background. A database migration: ends on its own, foreground. All three go to the approval list, since nobody wrote them.

Two readings: "within the turn" read literally means before the next message; read charitably means before the tool's timeout. The edge row for `npm install` lands differently under each. Repair: "within the tool's timeout" replaces "within the turn".

Terms: the file uses "wait" nowhere else. No capture.

## Step 7, the output

Generator:

> For every shell command you start, run it in the foreground where it ends on its own within the tool's timeout, and otherwise start it in the background, do the work that does not depend on its result, and end the turn, letting the harness resume the session when the command exits. Count a command as running past the timeout where it watches, serves, polls, or runs a whole suite.

Residue: "Keep `sleep` and every command that runs until stopped, `tail -f` for one, out of every wait." as an attached duty. "Count a check run again to see whether the state changed as polling." as a stance.

Accounting: six rows, all holds.

For approval: the three edge rows.

Dropped: none.

The contrast to notice is that the ask named one incident, the full test suite, and an instruction written from that incident alone would have said "run the test suite in the background". The case table turned one incident into a domain, and the generator now decides the dev server and the CI wait, which the ask never mentioned.
