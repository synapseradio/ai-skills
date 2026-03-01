# flix

Context engineering runbook for writing [Flix](https://flix.dev) code. Flix has sparse LLM training data — Scala/Haskell/Java instincts produce code that doesn't compile. This skill loads the constraints, stdlib guidance, and anti-hallucination rules needed for correct generation.

## Install

```sh
claude install-skill github:synapseradio/ai-skills/skills/flix
```

## What it does

- Loads Flix design principles and compiler constraints before generating code
- Enforces stdlib-first discipline via `api.flix.dev` (check before importing Java)
- Provides translation references from TypeScript, Python, and Rust
- Covers the effect system, Java interop, and common compiler errors

## References

| File | Purpose |
|------|---------|
| `references/design-principles.md` | 6 values + 41 compiler-enforced principles |
| `references/effect-system.md` | Purity tracking, `eff`/handler syntax, direct-style patterns |
| `references/interop-patterns.md` | Java interop: imports, null handling, `unsafe` blocks |
| `references/stdlib-map.md` | Task-to-module lookup for stdlib functions |
| `references/translate-typescript.md` | TypeScript/Effect-TS to Flix patterns |
| `references/translate-python.md` | Python to Flix patterns |
| `references/translate-rust.md` | Rust to Flix patterns |

## Usage

```
/flix write a CLI tool that reads a JSON config file and validates its schema
/flix translate this TypeScript function to Flix
```

## License

MIT
