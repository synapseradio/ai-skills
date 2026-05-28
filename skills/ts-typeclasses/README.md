# ts-typeclasses

Implement typeclasses and their instances in TypeScript — `Functor`, `Applicative`, `Monad`, `Traversable`, `Foldable` — and the higher-kinded type encoding they require. The skill uses Effect's HKT encoding (`TypeLambda`, `Kind`) as the substrate, but the subject is typeclasses in TypeScript generally; it works in repos that already depend on Effect and in repos that do not. It first checks whether a typeclass is the right abstraction at all, then walks the brand and instance encoding with copy-ready templates and a catalog of standard typeclasses.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/ts-typeclasses/` into `~/.claude/skills/ts-typeclasses/`.

## Usage

The skill triggers on natural language about typeclasses, HKTs, or the related Effect APIs — no explicit invocation required. When you want to invoke it directly:

```
/ts-typeclasses set up Functor and Traversable instances for my Tree type
```

```
/ts-typeclasses I have a Validated<E, A> and want to accumulate every error, not short-circuit
```

```
/ts-typeclasses why does "interface Functor<F> { map: <A,B>(fa: F<A>, f: (a:A)=>B) => F<B> }" not compile?
```

```
/ts-typeclasses we have six OrNull patterns scattered across this Node API — would a typeclass help, given the team's imperative style?
```

## How it works

The skill body in `SKILL.md` runs a five-step workflow: a judgment gate (is the encoding warranted at all?), situation routing (consuming Effect's built-ins, branding a custom type, or defining a missing typeclass), the `TypeLambda` brand, the instance, and verification. References load only when needed:

- `references/hkt-encoding.md` — why TypeScript has no native HKTs, how defunctionalization and brands recover them, and how `Kind` works mechanically.
- `references/typeclass-catalog.md` — every `@effect/typeclass` typeclass: what it abstracts, its core operation, its laws, and its derivation graph.
- `references/troubleshooting.md` — inference failures, variance-slot mistakes, decoding `Kind` error messages.
- `references/templates.md` — copy-and-adapt templates for brands, instances, and custom typeclasses.
- `references/non-effect-repos.md` — getting typeclasses into a repo that does not depend on Effect: the choice between adding `effect` / `@effect/typeclass` and vendoring a minimal encoding, with the vendorable code.

The judgment gate matters. Most requests for HKTs do not need them, and the encoding has a standing cost — inference-annotation tax, dense error messages. The skill states the gate's outcome explicitly before doing any encoding work.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`ts-typeclasses.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/ts-typeclasses.skill)
