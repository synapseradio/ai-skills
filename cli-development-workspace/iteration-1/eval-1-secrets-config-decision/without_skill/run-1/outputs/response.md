Short answer: support all three, but with a strict precedence order and one of them as the "happy path" for each audience. The idiomatic shape is **`--token` flag > `FLOWCTL_TOKEN` env var > credentials file**, with the credentials file being what humans actually use day-to-day and the env var being what CI uses. The `--token` flag exists mostly as an escape hatch and for debugging.

Let me walk through the reasoning, then the gotchas, because the gotchas are where most internal CLIs go wrong.

## The three sources, ranked by audience

**Credentials file (`~/.config/flowctl/credentials` or similar) — the default for humans.**

This is what `gh`, `aws`, `gcloud`, `kubectl`, `doctl`, `flyctl`, and basically every well-loved CLI does. The user runs `flowctl auth login` (or `flowctl login`, or `flowctl configure`), pastes the token once, and never thinks about it again until rotation. The token lives in a file with `0600` permissions in their config directory. No shell history exposure, no copy-paste into terminals, no accidental commit to dotfiles.

For a quarterly-rotated token this is especially important, because the human cost of "where did I put that token" compounds. A login subcommand that writes the file means rotation is a 30-second ritual, not a hunt through Bitwarden and `.zshrc`.

**Env var (`FLOWCTL_TOKEN`) — the default for CI and scripts.**

CI systems already have first-class secret stores (GitHub Actions secrets, GitLab CI variables, Vault-injected env, etc.) and the standard interface to those stores is "set an env var on the job." Asking CI to write a credentials file before invoking the CLI is friction nobody needs. The env var is also what people will reach for in ad-hoc shell scripts and in a `direnv` `.envrc`.

**`--token` flag — escape hatch only.**

Useful for: debugging ("does this token actually work?"), one-off invocations against a non-default token, and scripts where someone really does want to be explicit. But it's the worst option for daily use because it ends up in shell history, in `ps` output (visible to other users on shared boxes), and in CI logs if anyone forgets to mask it.

Some CLIs deliberately omit the flag for this reason. I'd include it because SREs will ask for it, but I would not advertise it in the README's "getting started" section.

## Precedence

When more than one source is set, resolve in this order, highest wins:

1. `--token` flag
2. `FLOWCTL_TOKEN` env var
3. Credentials file
4. (fail with a clear error pointing at `flowctl auth login`)

This is the order every major CLI uses, and it matches user expectation: the most explicit, most local source wins. Document this order plainly. When a token is loaded, a `--verbose` or `flowctl auth status` should say *which source it came from* — this saves an enormous amount of debugging time when someone has a stale token in a file overriding what they thought their env var was doing.

Actually, that's wrong — re-read the order. The env var should *not* override a `--token` passed on the same invocation, but it *should* override the file. The point is: explicit beats ambient, and ambient-per-shell beats ambient-per-machine.

## Gotchas

**Don't accept the token on stdin by default.** Some CLIs read from stdin if no other source is set, which seems clever but causes confusing hangs in CI when someone forgets to set the env var. If you want stdin support, gate it behind an explicit `--token-stdin` flag (this is what `gh auth login --with-token` does, and it's the right pattern — stdin is opt-in, never implicit).

**File permissions matter and you should enforce them.** When `flowctl auth login` writes the credentials file, `chmod 0600` it and `chmod 0700` the parent directory. On read, check the mode and warn (or refuse) if it's group/world readable. `aws` warns; `ssh` refuses. For an SRE tool I'd warn loudly and continue, because refusing breaks people in unexpected ways and SREs will hate you for it.

**Respect `XDG_CONFIG_HOME`.** `~/.config/flowctl/credentials` is the *fallback* when `XDG_CONFIG_HOME` is unset. The actual path is `${XDG_CONFIG_HOME:-$HOME/.config}/flowctl/credentials`. Some users (especially ones with carefully curated dotfiles) set `XDG_CONFIG_HOME` to something else and will be annoyed if you ignore it. Also: don't put it in `~/.flowctl/` — that's the old-school pre-XDG convention and it clutters `$HOME`.

**Separate config from credentials.** `~/.config/flowctl/config.toml` (or yaml, or whatever) holds non-secret things like the API endpoint, default workflow, output format. `~/.config/flowctl/credentials` holds only the token. This way users can commit their config to a dotfiles repo without leaking secrets, and you can document "safe to share" vs "never share" cleanly. `aws` does this with `~/.aws/config` vs `~/.aws/credentials`; `gh` keeps them together in `hosts.yml` and it's caused real incidents.

**Don't put the token in process arguments if you can help it.** If `--token` is passed, scrub it from any logs, telemetry, or error messages your CLI emits. Be especially careful with debug/verbose modes that dump the resolved config — a common bug is `--verbose` printing the loaded config including the token. Mask it (`ghp_***...***abcd`, showing only a prefix and last four chars) anywhere it's displayed.

**CI-specific: don't echo the token even on auth failure.** A 401 response handler that prints "tried token <full token>" has shipped in real CLIs. The token in a 401 message ends up in CI logs that may be world-readable for public repos. Print a fingerprint (last 4 chars, or a hash prefix) at most.

**Profiles, eventually.** You don't need this on day one, but plan for it. SREs often hit staging and prod with the same CLI, and the day someone runs a destructive command in prod thinking they were in staging is the day you'll wish you had `flowctl --profile staging ...` and a `[default]` section in the credentials file. Build the credentials file format with profile sections from the start (`[default]`, `[staging]`, `[prod]`), even if you only support one profile initially. Migrating a flat file to a sectioned one later is annoying.

**Token rotation UX.** Quarterly rotation means this happens. Make `flowctl auth login` idempotent (overwrites the existing token without complaint), and consider `flowctl auth status` that shows the token's source, a fingerprint, and — if your API exposes it — the expiry. A `--check` mode that hits a `/whoami` endpoint and confirms the token is live is worth its weight in support tickets.

**Keychain integration is nice but not required.** macOS Keychain, `secret-tool` on Linux, Windows Credential Manager. `gh` and `doctl` support these. For an internal SRE tool I would not bother on v1 — file with `0600` is fine, and adding keychain support later is non-breaking. If you do add it, make it opt-in via config, because keychain prompts in the middle of a script are infuriating.

## What I'd actually ship on day one

A `flowctl auth login` subcommand that prompts for the token (with `--with-token` reading from stdin for scripted setup), writes `${XDG_CONFIG_HOME:-$HOME/.config}/flowctl/credentials` at mode `0600` with a `[default]` profile section. Resolution order `--token > FLOWCTL_TOKEN > file`. A `flowctl auth status` that shows source and fingerprint. Token never logged in full, ever. Document the precedence in `flowctl auth --help` and in the README.

That covers the CI path (set `FLOWCTL_TOKEN` in the secret store, done), the daily human path (login once a quarter, forget about it), and the debugging path (`--token` when you need to be explicit), without any of them stepping on each other.
