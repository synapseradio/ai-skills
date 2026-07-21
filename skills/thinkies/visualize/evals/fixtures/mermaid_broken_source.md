---
name: Mermaid (Markdown) — broken: unrecognized diagram type and unbalanced brackets
description: First keyword is not a known mermaid diagram type, and a node bracket is left open
chart-type: mermaid-flowchart
engine: markdown
---

# Broken diagram

```mermaid
flowchory TD
    A[Visit signup page --> B[Enter email]
    B --> C{Email valid?
```

This block declares an unknown diagram keyword and leaves brackets unbalanced.
