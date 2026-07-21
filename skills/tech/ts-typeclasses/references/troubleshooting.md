# Troubleshooting HKT-encoded code

The encoding simulates a kind system the TypeScript compiler does not natively
have, so the compiler cannot always help the way it would for a built-in
feature. The failures below are the common ones. Each gives the symptom, the
cause, and the fix.

## `Type 'F' is not generic. ts(2315)`

**Symptom**: writing `F<A>` where `F` is a type parameter.

```typescript
interface Functor<F> {
  map: <A, B>(fa: F<A>, f: (a: A) => B) => F<B>  // ts(2315)
}
```

**Cause**: `F` has kind `*` — it cannot be applied. This is the wall the whole
encoding exists to get around.

**Fix**: constrain `F` to `TypeLambda` and apply it with `Kind`:

```typescript
import type { Kind, TypeLambda } from "effect/HKT"
interface Functor<F extends TypeLambda> {
  map: <A, B>(fa: Kind<F, never, never, never, A>, f: (a: A) => B)
    => Kind<F, never, never, never, B>
}
```

## `Generic type 'X<T>' requires N type argument(s). ts(2314)`

**Symptom**: naming a generic type or alias without its arguments — `type Bad =
Array` or passing `MyType` somewhere a type is expected.

**Cause**: a generic type is not a first-class entity in TypeScript; it cannot
be referenced unapplied. This is *why* a brand is needed — the brand is the
first-class handle for the constructor.

**Fix**: define and pass the brand (the `TypeLambda`), not the raw generic type.

## Inference does not run backward

**Symptom**: a generic function typed against `Kind<F, …>` fails to infer `F`
from a concrete argument. Passing an `Option<string>` where `Kind<F, …, A>` is
expected produces an assignability error instead of inferring
`F = OptionTypeLambda`.

**Cause**: `Kind` is a conditional type over an indexed access. The compiler
reduces it *forward* (brand plus arguments → concrete type) reliably, but cannot
reliably invert it (concrete type → which brand).

**Fix**: supply `F` explicitly at the call site rather than relying on
inference — `myFn<OptionTypeLambda>(...)`. Designing the API so the brand is an
explicit first type parameter, or so the instance value (which names its brand)
is passed in, avoids the inference dead end.

## Error messages show the encoding internals

**Symptom**: an error mentions `(F & { readonly In: In; … readonly Target: A
})["type"]` instead of the concrete type you expected.

**Cause**: that intersection-and-index expression is the literal definition of
`Kind`. When unification fails, the compiler shows `Kind` unreduced.

**Fix**: read it as a substitution. `(Brand & { Target: A })["type"]` is "the
brand's `type` body, with `this["Target"]` set to `A`". Substitute the brand's
`type` member mentally and the message becomes the concrete type. The mismatch
is usually a wrong slot or a wrong brand.

## A non-brand reached `Kind`

**Symptom**: `Kind<F, …>` resolves to an object type with `F`, `In`, `Out2`,
`Out1`, `Target` fields, and downstream code behaves as if the type is wrong.

**Cause**: `F` did not have a `type` member, so `Kind` took its error-fallback
branch. Usually the brand interface is missing `readonly type:`, has a typo in
it, or does not actually `extends TypeLambda`.

**Fix**: check the brand definition. It must `extends TypeLambda` and supply
`readonly type: YourType<this["Target"]>`.

## Variance-slot mistakes

**Symptom**: assignability errors that read backwards — a type that should be
assignable is rejected, or an unsafe assignment is allowed.

**Cause**: a type parameter placed in the wrong slot. `In` is contravariant;
`Out1`, `Out2`, `Target` are covariant. Putting a value-output type in `In`, or
a consumed-input type in `Target`, inverts the variance the compiler enforces.

**Fix**: place each parameter by role. An output the structure *produces* goes
in `Target` (or `Out1`/`Out2`); an input it *consumes* goes in `In`. For a type
like `Effect<R, E, A>`: `R` is consumed → `In`; `E` and `A` are produced →
`Out1` and `Target`.

## The `this`-resolution stall

**Symptom**: with nested or composed `TypeLambda`s, `Kind` widens to `unknown`
or fails to reduce, even though each brand looks correct alone.

**Cause**: the compiler does not always simplify `(F & { Target: … })["type"]`
when the argument is itself an unresolved `Kind`. Polymorphic `this` resolution
can stall under nesting.

**Fix**: avoid composing `TypeLambda`s on the fly. Define a dedicated brand for
the composed structure with its own explicit `type` member, rather than relying
on the compiler to compose two brands. Where a composition genuinely must stay
generic, an explicit type annotation at the boundary usually unblocks it.

## When the real problem is over-abstraction

**Symptom**: heavy annotation everywhere, unreadable errors, and the encoding
fighting back at every call site.

**Cause**: the code may not need HKTs at all. Re-apply the Step 0 gate from
`SKILL.md` — if no call site has a genuinely unknown `F`, concrete code is the
correct answer and the encoding is pure cost.

**Fix**: consider removing the encoding and writing concrete, possibly
duplicated, code. That is sound engineering when `∀f` is not load-bearing.
