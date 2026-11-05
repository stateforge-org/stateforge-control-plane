# StateForge Control Plane agent instructions

Before planning, reviewing, or changing this repository, read:

1. `CLAUDE.md`
2. Root `STATEFORGE_DPT.md`
3. `.agents/skills/stateforge-dpt-milestone/SKILL.md`
4. Every applicable engineering skill under `.claude/skills/`

Implement only the specifically requested Issue and its mapped DPT milestone.
The Control Plane owns its catalog, renderer registry, renderer extensions,
presentation validation against installed renderers, and rendering behavior.
SFP owns only the generic presentation transport contract; Provider Python
owns Provider runtime and author-facing declarations. Do not change sibling
repositories unless explicitly asked.

Preserve unrelated files and editor state. Local implementation commits are
allowed; humans own pushing, opening the PR, formal review, and merging. Do
not edit the generated DPT plan to record implementation status. Hand back
verification evidence and a PR-description draft; DPT derives delivery from
the correctly associated merged PR.
