Honest review. There's a fair amount wrong here, and given that this tool deletes pods and rotates secrets, several of these are blockers, not nits.

## Blocker 1: `-P` for `--password` puts the secret on the process list

```go
rootCmd.PersistentFlags().StringP("password", "P", "", "auth password")
```

A password should never be passed as a CLI flag at all — short or long. Anything on `argv` is visible to every other user on the host via `ps`, ends up in shell history, lands in CI logs, and gets captured by audit tooling. The standard fix is one of:

- Read from an environment variable (`DEPLOYCTL_PASSWORD`) and document it.
- Read from a file path (`--password-file`) so the secret stays on disk with the right mode bits.
- Read from stdin when `--password-stdin` is set (this is what `docker login` and `kubectl` style tools do).
- Prompt interactively via `golang.org/x/term`'s `ReadPassword` when stdin is a TTY.

Cite: this is the long-standing POSIX/Unix convention — `argv` is world-readable through `/proc/<pid>/cmdline` on Linux and through `ps -ef` everywhere. `git`, `curl` (`--netrc`, `-K`), `docker login --password-stdin`, `kubectl` (kubeconfig), `gh auth login`, and `aws` (env vars + credentials file) all avoid taking secrets on argv for exactly this reason. `curl`'s own man page warns that `-u user:password` is "insecure" because of this. The Cobra/spf13 ecosystem doesn't have a rule about it because it's upstream of Cobra — it's a Unix property.

Drop the `-P` short flag and the `--password` long flag entirely. Replace with `--password-stdin` and/or `DEPLOYCTL_PASSWORD`.

## Blocker 2: `-F` for `--force` is dangerous muscle memory

```go
rootCmd.PersistentFlags().BoolP("force", "F", false, "force the action")
```

Two problems here.

First, `--force` on a tool that deletes pods and rotates secrets should not have a short form at all. Short flags exist to make common, safe actions ergonomic. `--force` is the opposite of common and safe — making it one keystroke invites accidents, especially in shell history recall and in copy-pasted runbooks where someone tweaks the command and forgets `-F` is still on it. Look at how `kubectl delete --force`, `rm -rf` (notoriously regretted), and `terraform apply -auto-approve` are spelled out — the long form is intentional friction.

Second, if you keep a short flag despite the above, `-F` is the wrong letter. The de facto convention across Unix tools is lowercase `-f` for force (`rm -f`, `cp -f`, `mv -f`, `ln -f`, `kubectl delete -f`... wait, that one means `--filename`, which is exactly the kind of collision that bites people). Capital `-F` is unconventional and will surprise SREs whose fingers expect `-f`.

My recommendation: remove the short flag. `--force` only.

## Blocker 3: `-y` for `--yes` is fine in isolation but lethal in combination

```go
rootCmd.PersistentFlags().BoolP("yes", "y", false, "auto-confirm")
```

`-y` for auto-confirm is a real convention (`apt-get -y`, `dnf -y`). The blocker isn't `-y` itself; it's that `--force`, `--yes`, and a destructive `deploy` exist on the same root with persistent flags and short letters, so a careless `deployctl deploy -F -y --namespace prod` skips every guardrail in one line. For a tool that rotates secrets in prod, you want at least one of these confirmations to be unskippable, or to require a typed phrase (`--confirm "rotate-secrets-prod"`) for the truly destructive paths. `terraform`'s `-auto-approve`, `kubectl`'s lack of a global `--yes`, and `gh`'s `--yes` only on specific destructive subcommands are the references.

At minimum: don't make `--yes` and `--force` *persistent* on the root. Attach them only to the subcommands that genuinely need them. Persistent flags inherit down the tree and create surface area you didn't intend.

## Blocker 4: `-V` shadows Cobra's built-in `--version` and breaks the GNU convention

```go
rootCmd.PersistentFlags().BoolP("V", "V", false, "show version")
```

Three things wrong in one line.

1. The long flag is `"V"` — a single uppercase letter as a long flag is non-conformant. GNU long options are words: `--version`, not `--V`. POSIX/GNU getopt convention (which Cobra and pflag follow) treats `--V` as a long option named `V`, which works but reads as a typo to every user.
2. The short flag should be lowercase `-v` for version per long-standing convention (`git --version`/`-v` on many tools). Capital `-V` is also used (notably by `curl -V`, `ssh -V`, GNU tools), so `-V` for version isn't *wrong*, but...
3. ...lowercase `-v` is universally `--verbose`. If you ever add verbose logging — and an SRE tool will — you've already painted yourself into a corner with the casing. Pick now: `-v/--verbose` and `-V/--version`, OR no short flag for version.
4. Cobra already gives you `--version` for free if you set `rootCmd.Version = "..."`. Re-implementing it as a custom bool flag means you also have to write the print-and-exit logic, and you'll get it subtly wrong (exit code, output stream, format). Cite: Cobra docs, "Version Flag" — `cmd.Version` automatically registers `--version` and `-v` (configurable). See <https://github.com/spf13/cobra/blob/main/site/content/user_guide.md#version-flag>.

Fix: delete this line. Set `rootCmd.Version = version` and let Cobra register the flag. If you want `-V` instead of `-v`, set `rootCmd.Flags().BoolP("version", "V", false, "")` after construction or use `SetVersionTemplate` and override the shorthand.

## Issue 5: `-N` for `--namespace` collides with kubectl muscle memory

```go
deployCmd.Flags().StringP("namespace", "N", "default", "target namespace")
```

Every SRE on the planet types `kubectl -n <ns>` a hundred times a day. `kubectl` uses lowercase `-n` for `--namespace`. Your `deployctl` uses uppercase `-N`. They will type `-n` in your tool and hit `--dry`:

```go
deployCmd.Flags().BoolP("dry", "n", false, "dry run mode")
```

So `deployctl deploy -n prod` — which an SRE will type from muscle memory expecting "deploy to prod namespace" — is parsed as "dry run, with `prod` as a positional arg." That's a foot-gun. In the *other* direction (`-n` meant as dry-run), they'll get a deploy to the `default` namespace because `--namespace` defaulted to `default`. Either way, the parse and the intent diverge silently.

Cite: kubectl flag reference — <https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands>. Convention isn't a rule, but when your users live in `kubectl` all day, breaking its conventions is a usability bug.

Fix:

- `--namespace` gets `-n` (match kubectl).
- `--dry` becomes `--dry-run` (match kubectl, terraform `-plan`-style; nobody calls it `--dry`) and either drops its short flag or takes something unambiguous. `kubectl` uses `--dry-run=client|server` with no short flag. Follow that.

## Issue 6: `--dry` is the wrong name

```go
deployCmd.Flags().BoolP("dry", "n", false, "dry run mode")
```

The conventional spelling is `--dry-run`. `ansible`, `kubectl`, `rsync -n/--dry-run`, `helm --dry-run`, `git push --dry-run`, `make -n` (which prints commands without running them — same idea) all use `--dry-run` or `-n` as the short. Calling it `--dry` is idiosyncratic; SREs will tab-complete `--dry-run` and be told it doesn't exist.

Also: the description "dry run mode" is redundant ("mode"). Say what it does: "print actions without executing them."

## Issue 7: `-o human` default for `--output` is a footgun for scripts

```go
deployCmd.Flags().StringP("output", "o", "human", "output format (human, table, json)")
```

The flag itself is fine (`-o` for output is the universal convention — `kubectl -o json`, `gh -o`, `aws --output`). Two smaller issues:

- "human" as a format name is unusual. `kubectl` calls it `wide` or has no flag (default). `gh` uses no `--output` and a separate `--json`. The conventional names are `text`/`plain`/`table`/`json`/`yaml`. "human" is readable but non-standard; pick `text` or document explicitly that "human" is your name for it.
- The default being `human` means scripts that forget `-o json` will parse free-form text and break on every release. Common pattern: detect whether stdout is a TTY (`isatty`) and default to `human` only when interactive, `json` otherwise. `gh` and `docker` do this. If you don't want the auto-switch, at least document the contract: "human output is not stable; scripts must pass `-o json`."

## Issue 8: persistent vs. local flag scoping is wrong

`--force`, `--password`, `--yes`, and `--version` are all on `rootCmd.PersistentFlags()`. That means they're inherited by every subcommand, including ones that have no business with them (a hypothetical `deployctl status`, `deployctl logs`, `deployctl whoami`).

Cite: Cobra docs on flag scoping — "PersistentFlags ... will be available to the command it's assigned to as well as every command under that command." <https://github.com/spf13/cobra/blob/main/site/content/user_guide.md#persistent-flags>. The implication: only flags that genuinely apply across the whole tree belong on `PersistentFlags`. `--password` (auth) plausibly does. `--force` and `--yes` should live on the destructive subcommands that need them, so a `status` invocation can't accidentally accept `--force`.

`--version` on `PersistentFlags` is also wrong-shaped: version is a property of the binary, not a flag every subcommand should advertise. `rootCmd.Version` puts it where it belongs.

## Issue 9: descriptions are weak

Several flag descriptions don't say what the flag does or what its values mean:

- `"force the action"` — force *what* past *what*? "skip confirmation prompts and override safety checks" tells the SRE what they're losing.
- `"auto-confirm"` — confirm what? "answer yes to all confirmation prompts."
- `"show version"` — fine, but Cobra's auto-generated one is fine.
- `"dry run mode"` — see above.
- `"output format (human, table, json)"` — this one's actually good; lists the values.

`cobra` lints don't catch this, but `golangci-lint`'s `revive` and the project's own help output will surface it. If anything is going to live in `--help` for years, write the sentence properly.

## Summary table of recommended changes

| Current | Problem | Fix |
|---|---|---|
| `-P/--password` | Secret on `argv`, visible via `ps` | Remove. Use `--password-stdin`, env var, or file. |
| `-F/--force` | Destructive action with one-keystroke trigger; wrong case | Remove short flag. `--force` long-only. Move off persistent. |
| `-y/--yes` | Persistent + combinable with `--force` | Move off persistent. Per-subcommand only. Consider `--confirm <phrase>` for the worst paths. |
| `-V/--V` for version | Single-letter long flag, conflicts with conventions, reimplements Cobra built-in | Delete. Set `rootCmd.Version`. |
| `-N/--namespace` | Collides with `kubectl -n` muscle memory | Use `-n/--namespace`. |
| `-n/--dry` | Steals `-n` from namespace; wrong spelling | Rename to `--dry-run`. Drop short flag, or use a non-conflicting one. |
| `-o human` default | Non-standard name; scripts break silently | Rename to `text`, or auto-switch to `json` when not a TTY. |

## What I'd want to see before approving

1. `--password` removed from `argv`. This is the only one I'd actively block on by itself.
2. `-n` swapped to mean `--namespace`, and `--dry` renamed to `--dry-run`. The current layout will cause a wrong-namespace deploy in production within a month.
3. `--force` and `--yes` moved off persistent root flags onto the specific subcommands that need them.
4. `-V/--V` replaced with Cobra's built-in `Version`.

The other items I'd take as follow-ups, but the four above are blocking for a tool that rotates prod secrets. Honest read: the flag layout reads like it was written without referencing `kubectl` or thinking about `ps`, and an SRE tool can't afford either gap.

### References used

- Cobra user guide, "Persistent Flags" and "Version Flag": <https://github.com/spf13/cobra/blob/main/site/content/user_guide.md>
- pflag (which Cobra uses): <https://pkg.go.dev/github.com/spf13/pflag>
- `kubectl` flag reference: <https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands>
- `docker login --password-stdin` rationale: <https://docs.docker.com/reference/cli/docker/login/>
- `curl` man page warning on `-u user:password` argv exposure: <https://curl.se/docs/manpage.html>
- POSIX `ps`, `/proc/<pid>/cmdline` argv visibility: <https://man7.org/linux/man-pages/man5/proc.5.html>
- GNU "Standards for Command Line Interfaces" (long options as words): <https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html>
