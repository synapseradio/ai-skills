Short answer: ship all three input paths, but rank them carefully and treat the bearer token as a secret, not as ordinary configuration. The credentials file is the primary, durable home for the token. The environment variable is a reluctant accommodation for CI. A `--token` flag is useful as an idea but should not actually accept the secret value on the command line — accept a file path or `-` for stdin instead.

Here is the reasoning, grounded in clig.dev.

## Why the bearer token is special

clig.dev separates "configuration" from "secrets." For ordinary configuration — endpoint URL, default workspace, output format — the guidance is to support flags, env vars, and a config file together, applied in a fixed precedence order ([clig.dev: Configuration](https://clig.dev/#configuration)).

For secrets, both relevant sections are explicit and unusually firm:

- **"Do not read secrets directly from flags."** A `--token <value>` flag leaks the secret into `ps` output and into shell history, and "encourages the use of insecure environment variables for secrets" ([clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags)).
- **"Do not read secrets from environment variables."** Exported env vars are sent to every child process and tend to end up in logs; shell substitutions like `curl -H "Authorization: Bearer $TOKEN"` leak into globally-readable process state; container env vars surface through `docker inspect`; systemd unit env vars surface through `systemctl show` ([clig.dev: Environment variables](https://clig.dev/#environment-variables)).

The same section names the acceptable channels: "Secrets should only be accepted via credential files, pipes, `AF_UNIX` sockets, secret management services, or another IPC mechanism."

So clig.dev's strong preference for a quarterly bearer token is a credentials file (or stdin/pipe). Flags and env vars for the secret itself are anti-patterns it calls out by name.

## What that means for flowctl

### 1. Credentials file is the primary path

Put the token in a credentials file under XDG, exactly as you suggested:

- `${XDG_CONFIG_HOME:-$HOME/.config}/flowctl/credentials`
- File mode `0600`, parent directory `0700`, and verify both on read.

This is the right home for it under the [XDG Base Directory Spec](https://clig.dev/#configuration) — "**Follow the XDG-spec.**" Make sure you actually honor `$XDG_CONFIG_HOME` rather than hard-coding `~/.config`; users who relocate it (containers, multi-tenant boxes) expect that.

A few details worth getting right:

- Keep the credentials file separate from any other `flowctl` config. A `config.toml` for endpoint, default workspace, output preferences, etc., can live next to `credentials` but should not contain the token. Mixing them invites users to commit the whole file to dotfiles repos.
- Provide `flowctl auth login` and `flowctl auth logout` subcommands that write and remove the file with the right permissions, rather than asking SREs to hand-edit it. clig.dev's [Conversation as the norm](https://clig.dev/#conversation-as-the-norm) and [Ease of discovery](https://clig.dev/#ease-of-discovery) push you toward a guided flow here, and it dovetails with the quarterly rotation: `flowctl auth login` after the rotation reminder is one command, not "edit this file at this path with this format."
- If your platform has a system keychain (macOS Keychain, Secret Service on Linux, Windows Credential Manager) and your SREs all run on managed laptops, prefer that over a plaintext file. clig.dev names "secret management services" as a first-class option in the same sentence that allows credential files. The XDG file is the portable fallback when no keychain is available, and is the right default for headless Linux boxes.

### 2. The "flag" should accept a file path, not the value

Do not ship a literal `--token <value>` flag — that is precisely the construction the guideline refuses. Ship one or both of:

- `--token-file <path>` — read the token from a file. This is the `--password-file` pattern clig.dev recommends by name in [Arguments and flags](https://clig.dev/#arguments-and-flags).
- Reading the token from stdin when the flag value is `-`, e.g. `flowctl --token-file - run start ...`. clig.dev's "**If input or output is a file, support `-` to read from stdin or write to stdout**" applies here ([clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags)).

Together these cover the scriptable paths that actually need a per-invocation override: a one-off run with a different identity, an SRE testing a freshly rotated token before saving it, a script that pulls a token from Vault and pipes it in.

### 3. The environment variable is a deliberate concession for CI

clig.dev's "do not read secrets from environment variables" is a hard line, but the working reality of GitHub Actions, GitLab CI, Buildkite, and friends is that the supported way to inject a secret into a job is an environment variable bound from the platform's secret store. Refusing to read `FLOWCTL_TOKEN` does not make CI safer; it just pushes your users into shelling out an `echo "$SECRET" > /tmp/token && flowctl --token-file /tmp/token` dance that is no better and arguably worse.

So: support `FLOWCTL_TOKEN` for CI, and in your help and docs flag it as the CI escape hatch, not the recommended day-to-day path. Things to actually do here:

- Name it `FLOWCTL_TOKEN` — uppercase, underscore, prefixed by your binary name, single-line value. That follows the naming rules in [clig.dev: Environment variables](https://clig.dev/#environment-variables).
- Also accept `FLOWCTL_TOKEN_FILE` pointing at a file path. Several modern tools do this (`DOCKER_CONFIG`, the `_FILE` suffix convention from Docker secrets, `GIT_ASKPASS`) and it gives CI systems that mount secrets as files — Kubernetes projected volumes, Vault Agent, GitHub Actions with a file-typed secret — a path that does not stage the value through `env`.
- Do not read the token from a generic `.env` file by default. The same env-vars section warns against `.env` for "sensitive credentials & key material that would be better stored more securely." If you support `.env` for non-secret config, exclude the token key from that loader, or at least do not advertise it.

### 4. Precedence order

clig.dev specifies a single precedence order, highest to lowest ([clig.dev: Configuration](https://clig.dev/#configuration)):

1. Flags
2. Shell environment variables
3. Project-level configuration (e.g. `.env`)
4. User-level configuration
5. System-wide configuration

Apply that to flowctl's token sources:

1. `--token-file <path>` (or `--token-file -` from stdin) — highest. An explicit per-invocation override always wins.
2. `FLOWCTL_TOKEN_FILE` — read the file at that path.
3. `FLOWCTL_TOKEN` — the raw value, with a debug-log warning that this path is discouraged outside CI.
4. The XDG credentials file at `${XDG_CONFIG_HOME:-$HOME/.config}/flowctl/credentials`.
5. (Optional) System-wide `/etc/flowctl/credentials` for shared bastion hosts, same `0600`/owned-by-the-user model.

The first source that resolves to a usable token wins; do not silently merge them. When more than one is set, log at debug level which one was selected — SREs debugging "why am I authenticating as the wrong identity" will thank you.

### 5. Concrete flag and behavior surface

Putting it all together, the surface I would ship for v1:

- `flowctl auth login` — interactive prompt, writes `~/.config/flowctl/credentials` at mode `0600`. Honors `--no-input` ([clig.dev: Interactivity](https://clig.dev/#interactivity)) by failing fast with a useful error in non-TTY contexts instead of hanging.
- `flowctl auth logout` — removes the credentials file.
- `flowctl auth status` — prints which source the token is being read from and a fingerprint (last four chars or a hash), never the full token. Same rule applies to any debug logging.
- `--token-file <path>` global flag, with `-` meaning stdin.
- `FLOWCTL_TOKEN_FILE` env var, identical semantics.
- `FLOWCTL_TOKEN` env var, documented as "for CI environments where mounting a file is not practical."
- No `--token <value>` flag at all. If you must have something for the help text to say, document the absence: "flowctl does not accept the token as a flag value to keep it out of `ps` and shell history; use `--token-file` or `flowctl auth login`."

### 6. Gotchas worth flagging up front

- **Logging.** Whatever you do, scrub the token from request logs, debug output, and crash reports. The leakage paths in the env-vars section ("their values end up in debug logs") apply equally to a value you read from a file once it is in memory. Wrap it in a type that redacts on `Display`/`Debug`/`String()`.
- **Error messages on missing token.** "401 Unauthorized" from the API is hostile. Rewrite it ([clig.dev: Errors](https://clig.dev/#errors)) into something like "flowctl could not authenticate. Run `flowctl auth login`, or set FLOWCTL_TOKEN_FILE. The token is read from <source it tried>." This also covers the rotation case — when the quarterly token expires, the message should name the renewal step.
- **File-permission checks.** If `credentials` is group- or world-readable, refuse to read it and tell the user to `chmod 0600`. SSH does this for `~/.ssh/id_rsa`; users recognize the pattern.
- **Rotation flow.** Quarterly rotation is frequent enough that you should make `flowctl auth login` idempotent and atomic — write to a temp file in the same directory, `fsync`, then `rename` over the existing file. A half-written credentials file at the moment of rotation is a bad day.
- **`.env` and dev workflow.** SREs may try to put `FLOWCTL_TOKEN=...` in a project `.env`. clig.dev allows `.env` for ordinary config but specifically discourages it for credentials. Decide explicitly whether your loader reads `.env` for the token or skips that key, and document the choice. I would skip it.
- **Help text honesty.** When you list env vars in `flowctl --help` or `flowctl help auth`, mark `FLOWCTL_TOKEN` as the lower-preference option and explain why ([clig.dev: Help](https://clig.dev/#help) — "Saying just enough" applies).
- **Shell completion and history.** If you ever add a `--token` value flag later "just for convenience," it will end up in shell history and screen-share recordings. The reason to refuse it now is that the refusal is much harder to walk back once people depend on it.

### TL;DR

- **Primary:** XDG credentials file at `${XDG_CONFIG_HOME:-$HOME/.config}/flowctl/credentials`, mode `0600`, written and rotated through `flowctl auth login`. ([clig.dev: Configuration](https://clig.dev/#configuration))
- **Per-invocation override:** `--token-file <path>` (and `-` for stdin). No `--token <value>`. ([clig.dev: Arguments and flags](https://clig.dev/#arguments-and-flags))
- **CI:** `FLOWCTL_TOKEN_FILE` preferred, `FLOWCTL_TOKEN` accepted as the explicit CI escape hatch, both documented as such. ([clig.dev: Environment variables](https://clig.dev/#environment-variables))
- **Precedence:** flag-file > env-var-file > env-var-value > user credentials file > system credentials file. ([clig.dev: Configuration](https://clig.dev/#configuration))
- **Always:** redact in logs, check file permissions, write a useful error on auth failure that names the source it tried.
