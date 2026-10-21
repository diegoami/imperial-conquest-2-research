# Optional review guidance

The session chooses whether a separate review is useful, its tools, model and isolation.
This guide is not a mandatory external-review or merge gate. Explicit owner choices
prevail. Historical briefs retain their original instructions as historical evidence.

A useful brief names the exact commit/diff, the question, acceptance criteria, evidence
paths and unavailable inputs. Ask for all material findings in one complete pass, ranked
by severity, with supporting locations and concrete impact. Distinguish blockers from
suggestions. The reviewer should state what was checked and what remains unverified;
an incomplete pass must not claim full approval. Read the full final/native record
before interpreting the run's exit code or deciding to retry.

If using OpenCode, `.opencode/agents/reviewer.md` supplies an optional read-only role.
Use a compatible CLI and check its permissions first. The legacy 1.x invocation was
`opencode run --agent reviewer -m <model> --dir <workspace>` with stdin closed and
appropriate monitoring. A worktree is optional. Keep private evidence outside Git;
stage only needed read-only inputs in a private scratch directory when isolation
requires it. Never broaden access to credential stores to resolve a refusal.

Useful wording for a review brief:

> Finish reading the full diff and acceptance criteria before reporting. Report all
> blocking findings together, including shared causes and affected locations. State
> the checks actually performed, the evidence limits and any uncovered sections.
> Do not edit, commit, push, comment or merge; return findings to the main session.
