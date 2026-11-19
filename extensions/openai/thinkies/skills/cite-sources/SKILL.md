---
name: cite-sources
description: Use whenever a response draws on web pages, docs, or other external material fetched
  during the task. Ties each claim to the source it came from, checks that each link works before
  citing it, and keeps sourced facts distinct from analysis.
---

## Steps

### 1. Identify what needs citation

Target: recent statements that reference external information. Citations are for information retrieved this task via external tools (web search, docs, API lookup) — not training data, which is base knowledge and never cited.

When no content was passed, read "recent statements" as those in the last reply or the document in hand. A statement that came from memory and needs a source gets retrieved first, then cited. Where no statement on the page draws on outside information, say that nothing needs citing and stop.

### 2. Track sources as you work

For each source consulted, note:

- The URL actually visited
- What specific information came from it
- Which claims depend on it

### 3. Validate every URL before citing

Fetch each URL with the session's web fetch tool and confirm it loads. A reader cannot open a source that returns an error or times out, so drop it or cite it as unreachable. In a session with no fetch tool, mark each URL "not checked" beside its citation.

### 4. Match citation format to context

- **Formal work**: structured citations (APA, MLA)
- **Technical discussion**: simple references with working URLs
- **Quick response**: inline links with clear attribution

### 5. Separate source material from synthesis

Mark what came from sources ("According to…", "The documentation states…") apart from your own analysis ("This suggests…", "Based on this, I conclude…").

### 6. Present citations where readers can find them

Group citations in a dedicated section or place them inline. Make URLs clickable and obvious. Include enough context for a reader to verify the interpretation.

## Return

Return the content with its citations in place, and a source list giving each URL, whether it loaded, what came from it, and which claims depend on it. Keep what the sources state apart from what you conclude. The run is done when every claim that draws on a retrieved source carries a citation and every cited URL has been fetched or marked "not checked".
