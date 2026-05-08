For a tool that deletes pods and rotates secrets, this flag layout has several problems that range from "annoying" to "actively dangerous." I'm grounding each one in the [Command Line Interface Guidelines](https://clig.dev), which is the closest thing this space has to a shared style guide.

Going block by block.

## Root flags

### `--force` as `-F` (uppercase)

```go
rootCmd.PersistentFlags().BoolP("force", "F", false, "force the action")
```

The convention for force is lowercase `-f`. clig.dev lists it explicitly in the standard-flag table:

> `-f`, `--force`: Force. For example, `rm -f` will force the removal of files, even if it thinks it does not have permission to do it. This is also useful for commands which are doing something destructive that usually require user confirmation, but you want to force it to do that destructive action in a script.

Source: [clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags), under *"Use standard names for flags, if there is a standard."* The whole point of that rule is so users can guess: "If another commonly used command uses a flag name, it's best to follow that existing pattern. That way, a user doesn't have to remember two different options... and users can even guess an option without having to look at the help text."

Every SRE has `rm -f`, `cp -f`, `ln -f`, `git push -f` in their fingers. `-F` will get typed as `-f` under stress, silently fail to parse as force, and then they'll add `-F` and move on without thinking about why. Worse, on a tool that rotates secrets, "force" is exactly the flag you want users to type deliberately, not muscle-memory through.

Also, the help text "force the action" tells the reader nothing. Force what, past what guard? Spell out what protections `-f` bypasses (confirmation prompts? safety checks on prod? both?).

### `--password` as `-P` taking a string

```go
rootCmd.PersistentFlags().StringP("password", "P", "", "auth password")
```

This is the worst one in the diff. clig.dev is unambiguous:

> **Do not read secrets directly from flags.** When a command accepts a secret, e.g. via a `--password` flag, the flag value will leak the secret into `ps` output and potentially shell history. And, this sort of flag encourages the use of insecure environment variables for secrets. (Environment variables are insecure because they can often be read by other users, their values end up in debug logs, etc.)

> Consider accepting sensitive data only via files, e.g. with a `--password-file` flag, or via `stdin`.

Source: [clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags), final rule of the section.

Concretely, on a shared bastion, `ps auxww` from any other SRE's session will print the password while `deployctl` is running. Shell history (`~/.bash_history`, `~/.zsh_history`) will keep it for as long as `HISTSIZE` permits. CI logs that echo the command line will leak it. Replace with `--password-file <path>` or read from stdin (`--password-stdin`, the way `docker login` does it). If a `--password` flag is needed for compatibility, at minimum it should warn loudly when used and accept `-` to mean stdin.

There's a second issue layered on top: `-P` is also being burned as the short form here, which collides with what `-p` usually means in this neighborhood — port (`ssh`, `psql`, `kubectl port-forward`). clig.dev's standard list is:

> `-p`, `--port`: Port. For example, `psql`, `ssh`.

A deploy tool that talks to a cluster is exactly where users will reach for `-p` expecting port. Even if you fix the secrets handling, do not park a password under any case of `-p`/`-P`.

### `--yes` as `-y`

```go
rootCmd.PersistentFlags().BoolP("yes", "y", false, "auto-confirm")
```

`-y` for auto-confirm is well-known (`apt -y`, `dnf -y`, `brew install -y`) so the short form is fine. The problem is what it implies for a tool of this blast radius. clig.dev's danger taxonomy:

> **Confirm before doing anything dangerous.**
>
> - **Mild:** A small, local change such as deleting a file...
> - **Moderate:** A bigger local change like deleting a directory, a remote change like deleting a resource of some kind, or a complex bulk modification that can't be easily undone. You usually want to prompt for confirmation here. Consider giving the user a way to "dry run" the operation so they can see what'll happen before they commit to it.
> - **Severe:** Deleting something complex, like an entire remote application or server. You don't just want to prompt for confirmation here — you want to make it hard to confirm by accident. Consider asking them to type something non-trivial such as the name of the thing they're deleting. Let them alternatively pass a flag such as `--confirm="name-of-thing"`, so it's still scriptable.

Source: [clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags).

"Push services to staging and prod" plus "deletes pods and rotates secrets" sits in moderate-to-severe territory for prod. A blanket persistent `-y` that auto-confirms every prompt under the tool means a forgotten alias or a `set -x` script can roll prod with no friction. Two things to consider:

1. Have `--yes` only suppress mild prompts. For severe actions (anything against prod, secret rotation, anything destructive), require `--confirm="<env-or-resource-name>"` instead. clig.dev names this pattern explicitly.
2. Restrict `--yes` to non-prod by default, or refuse to honor it when the target environment is prod unless `--confirm` is also passed.

### `--version` as `-V` with short name `"V"`

```go
rootCmd.PersistentFlags().BoolP("V", "V", false, "show version")
```

Two distinct mistakes here.

First, the long name is `"V"` not `"version"`. Cobra's `BoolP(name, shorthand, ...)` takes the long name as the first argument, so this registers a long flag literally spelled `--V`. clig.dev requires:

> **Have full-length versions of all flags.** For example, have both `-h` and `--help`. Having the full version is useful in scripts where you want to be verbose and descriptive, and you don't have to look up the meaning of flags everywhere.

Source: [clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags). The standard-flag list calls out `--version` by name. This should be `BoolP("version", "V", false, "show version")`.

Second, on the short form, clig.dev is cautious about `-v`/`-V`:

> `-v`: This can often mean either verbose or version. You might want to use `-d` for verbose and this for version, or for nothing to avoid confusion.

`-V` for version is defensible — it's what `gcc`, `ssh`, and many GNU tools use, and it leaves `-v` free for verbose, which a deploy tool will eventually want. Just be aware you've spent a single-letter slot, and document the choice. clig.dev's broader rule applies:

> **Only use one-letter flags for commonly used flags,** particularly at the top-level when using subcommands. That way you don't "pollute" your namespace of short flags, forcing you to use convoluted letters and cases for flags you add in the future.

Source: [clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags). You're putting four short flags on root (`-F`, `-P`, `-y`, `-V`), all persistent, before any subcommand has been written. Once those are out, removing them is a breaking change. I'd drop `-F` (force is dangerous enough to warrant typing the long form) and `-P` (which is going away with the secrets fix anyway), and keep only `-y` and `-V` on root.

## Deploy subcommand flags

### `--dry` as `-n`

```go
deployCmd.Flags().BoolP("dry", "n", false, "dry run mode")
```

Short form is right, long form is wrong. clig.dev specifies:

> `-n`, `--dry-run`: Dry run. Do not run the command, but describe the changes that would occur if the command were run. For example, `rsync`, `git add`.

Source: [clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags).

The convention is `--dry-run`, not `--dry`. `rsync -n`, `git add -n`, `kubectl --dry-run=client`, `terraform plan` (which is its own dry-run idiom) — every neighbor uses `dry-run`. Rename to `--dry-run`. Also: given the danger profile, `dry-run` should be promoted in the help text and probably suggested by the tool itself when a user runs against prod for the first time on a host.

### `--output` as `-o` taking `human|table|json`

```go
deployCmd.Flags().StringP("output", "o", "human", "output format (human, table, json)")
```

This one is closest to right but has a subtle problem. clig.dev lists `-o`/`--output` as:

> `-o`, `--output`: Output file. For example, `sort`, `gcc`.

Source: [clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags).

The standard meaning of `-o` in the UNIX world is "output file path" (`gcc -o out.bin`, `sort -o out.txt`, `curl -o page.html`). Using `-o` for output *format* is a `kubectl`-ism that has spread, but it collides with the older convention. If users ever pipe `deployctl` output anywhere, they'll reach for `-o` expecting a path. Two cleaner options:

1. Rename the flag to `--format` (or `--output-format`) and drop the `-o` short form. This is what `gh` does (`gh ... --json`).
2. Keep `-o`/`--output` but accept either a format keyword or a path, the way `kubectl` mostly gets away with — and document the overload explicitly.

Separately, clig.dev's [Output](https://clig.dev/#output) section calls out `--json` and `--plain` as standard top-level flags. If JSON is one of three formats here, consider promoting `--json` to a flag in its own right (and likewise `--plain` for the human format). It's a small ergonomic win for scripts: `deployctl deploy --json` reads better than `deployctl deploy -o json`, and it matches the [Output](https://clig.dev/#output) guidance directly.

### `--namespace` as `-N` (uppercase) defaulting to `"default"`

```go
deployCmd.Flags().StringP("namespace", "N", "default", "target namespace")
```

The collision is with `kubectl`. Anyone deploying services to a Kubernetes-shaped target reaches for `-n` for namespace from muscle memory:

```
kubectl get pods -n production
```

Your tool already used `-n` for `--dry-run` on the same subcommand, which forced `-N` here, which violates [Consistency across programs](https://clig.dev/#consistency-across-programs):

> **Use standard names for flags, if there is a standard.** If another commonly used command uses a flag name, it's best to follow that existing pattern. That way, a user doesn't have to remember two different options (and which command it applies to), and users can even guess an option without having to look at the help text.

Source: [clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags).

This is the most dangerous interaction in the diff for a tool that deletes pods. An SRE under load types `deployctl deploy -n staging service-x` expecting "deploy to staging namespace." On this tool, `-n` means dry-run and `staging` becomes a positional argument. Best case the parser rejects it; worst case `staging` gets interpreted as something else and a deploy targets `default`. The combination of `-n=dry-run` + `-N=namespace` is the bug waiting to happen.

Two fixes, in order of preference:

1. Make `--dry-run` long-form-only on this subcommand and give `-n` to `--namespace`. clig.dev's "only use one-letter flags for commonly used flags" applies — namespace is referenced on every invocation, dry-run is occasional.
2. If you keep `-n` for dry-run for some reason, drop the short form for namespace entirely. `--namespace` only. Do not use `-N`.

The default `"default"` is also worth a second look. For a tool that pushes to staging and prod, defaulting the target namespace to anything is risky — a missing `--namespace` should probably be a hard error (or at minimum require explicit confirmation in prod). clig.dev:

> **Make the default the right thing for most users.**

Source: [clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags). For a deploy tool, "the right thing" is "force the user to name what they're touching."

## Cross-cutting things worth raising in the PR

A few patterns visible across the whole diff that aren't tied to a single line.

**Persistent vs subcommand placement.** Putting `--force`, `--yes`, `--password` on the root command means every subcommand inherits them, including ones that have no business taking a password or being forced. Push the dangerous flags down to the specific subcommands that need them. clig.dev's rationale is the same one as for short-flag namespace pollution above — each persistent flag at root is a slot you can never reclaim without a breaking change ([Future-proofing](https://clig.dev/#future-proofing)).

**Help text quality.** `"force the action"`, `"auto-confirm"`, `"dry run mode"`, `"target namespace"` are placeholder-grade. clig.dev's [Help](https://clig.dev/#help) section is worth a read; the short version is that flag descriptions should say what changes and what guards are bypassed, not restate the flag name. For a deploy tool: "Skip confirmation prompts on moderate operations. Has no effect on prod, where `--confirm=<env>` is required." That kind of specificity.

**Severe-action pattern is missing entirely.** The diff has `--force` and `--yes` but nothing matching the `--confirm="name-of-thing"` shape clig.dev recommends for severe actions. Given that this tool rotates secrets and deletes pods in prod, that's the gap that worries me most. Add a `--confirm` flag, gate prod operations behind it, and have the interactive prompt require typing the environment name.

## Suggested layout

Pulling all of the above into a concrete fix:

```go
// root flags
rootCmd.PersistentFlags().BoolP("yes", "y", false,
    "Auto-confirm mild prompts. Ignored for prod; use --confirm there.")
rootCmd.PersistentFlags().BoolP("version", "V", false, "Print version and exit.")
rootCmd.PersistentFlags().Bool("json", false, "Emit machine-readable JSON on stdout.")
rootCmd.PersistentFlags().Bool("no-input", false,
    "Disable all interactive prompts; fail instead of prompting.")

// auth — secrets via file or stdin only, never as a flag value
rootCmd.PersistentFlags().String("password-file", "",
    "Path to a file containing the auth password. Use '-' to read from stdin.")

// deploy subcommand
deployCmd.Flags().BoolP("dry-run", "n", false,
    "Describe the changes that would occur without applying them.")
deployCmd.Flags().String("format", "human",
    "Output format: human, table, json. Prefer --json at the root.")
deployCmd.Flags().StringP("namespace", "N", "",
    "Target namespace. Required; no default.")
deployCmd.Flags().String("confirm", "",
    "For prod: the namespace name, typed verbatim, to confirm the action.")

// drop --force at root entirely; if a subcommand needs it, add it locally
```

Notes on the changes:

- `--password` flag is gone; replaced with `--password-file` per the secrets rule.
- `--force` is gone from root; reintroduce only on the specific subcommand that needs it, with a long-form-only flag and an explicit warning.
- `-n` reassigned to `--dry-run` on `deploy` (matches `rsync`/`git`); namespace gets `-N` since `-n` is taken at the subcommand level. If you'd rather give `-n` to namespace (matching `kubectl`), drop the short form on `--dry-run`.
- `--namespace` has no default, so a forgotten flag fails closed.
- `--confirm` added for severe actions, per the [Arguments and flags](https://clig.dev/#arguments-and-flags) severity taxonomy.
- `--json` is promoted to a top-level flag per [Output](https://clig.dev/#output).
- `--no-input` added per the [Interactivity](https://clig.dev/#interactivity) section so CI can opt out of prompts deterministically.
- Long-form names follow standard spellings (`--dry-run`, `--version`).

Most of the PR's flag layout would be fine on a tool with smaller blast radius. On a tool that pushes to prod, deletes pods, and rotates secrets, the `--password` flag and the `-n` collision are blocking issues, and the rest are worth fixing before they calcify into compatibility commitments.
