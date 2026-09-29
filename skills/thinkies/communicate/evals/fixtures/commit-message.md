fix(parser): reject trailing commas in strict mode

The strict parser accepted `[1, 2,]` and returned a three-element array
with a trailing null, which downstream validation then rejected with an
unrelated "unexpected null" error. Strict mode now fails at the comma
with a position, and lenient mode keeps accepting it.

Refs #412
