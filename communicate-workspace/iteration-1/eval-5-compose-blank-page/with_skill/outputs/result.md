## Why User Input Is Untrusted by Default

Every value that originates from a user — a form field, a URL parameter, a cookie, a JSON body — enters this library as untrusted. The library does not assume the input is malformed. It assumes you have not yet decided whether to trust it.

That distinction matters. We built this default after a pattern of bug reports where developers passed raw request data directly into internal APIs that expected sanitized values. The APIs had no defenses at that layer — why would they? They were internal. A search field holding `'; DROP TABLE users; --` made it from the HTTP request to a database query in three lines of code, and none of those lines looked wrong from the outside.

Marking input as untrusted forces the trust decision to be explicit. When you pass a value to an internal API, the library needs to see either a sanitized form or a deliberate `trust()` call that signals you have checked it yourself. The call does not protect you — it documents that you accepted responsibility.

This does not make every user interaction a threat. Most inputs are benign. The default exists because the cost of a missed threat is asymmetric: one unvalidated field is enough. The library cannot know which inputs are sensitive, but you can. The default asks you to say so.
