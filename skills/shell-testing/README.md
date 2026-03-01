# shell-testing

Write idiomatic [BATS](https://github.com/bats-core/bats-core) tests for bash and zsh shell scripts. Covers test patterns, assertions, mocking, isolation, zsh-specific testing, and CI integration.

## Install

```sh
claude install-skill github:synapseradio/ai-skills/skills/shell-testing
```

## What it covers

- BATS-core patterns with bats-assert, bats-support, and bats-file
- Mandatory test isolation (temp dirs, mocked externals, safety guards)
- Zsh testing via `bats --shell zsh` and zunit
- Mocking strategies: function overrides, PATH manipulation, CLI stubs
- Targeted test execution (never runs the full suite)

## References

| File | Purpose |
|------|---------|
| `references/patterns.md` | Sourcing, multi-line output, stdin, stderr, TTY testing, fixtures, CI |
| `references/gotchas.md` | Anti-patterns: dangerous teardown, negation bugs, variable scope, portability |
| `references/zsh-testing.md` | Zunit syntax, zsh-test-runner, completions, widgets |

## Usage

```
/shell-testing write tests for lib/helpers.sh
/shell-testing add integration tests for the install command
```

## License

MIT
