# Prepare a rebuttal

Open the root of your submitted LaTeX project in your preferred coding agent. Copy the contents of [PROMPT.md](PROMPT.md) into the agent and give it access to the LaTeX source and a terminal. The workflow uses subagents and may ask for the review source or venue details.

## Set up the files

Copy [PROMPT.md](PROMPT.md), [import_reviews.py](import_reviews.py), and [count_rebuttal.py](count_rebuttal.py) from the `rebuttal/` directory of a checkout of [muelphil/research-skills](https://github.com/muelphil/research-skills) into a single `rebuttal/` directory under the LaTeX project root. Use a checkout containing these files. The public repository currently contains only the root README.

Run the workflow from the LaTeX project root with Python 3 available as `python`. The scripts use the standard library. Have the OpenReview forum URL or a saved HTML page with all official reviews expanded ready.

## Launch from the command line

Use the interactive launch if you want the agent to ask for the source and follow-up details. The second command in each block starts a non-interactive run. Replace the example URL with your forum URL or saved HTML path. Supply any venue details the agent cannot infer in the same message.

### Claude Code

```sh
claude "Read ./rebuttal/PROMPT.md and follow the rebuttal workflow."
claude -p "Read ./rebuttal/PROMPT.md and follow the rebuttal workflow. Review source: https://openreview.net/forum?id=EXAMPLE. Proceed without additional author context."
```

### Codex

```sh
codex "Read ./rebuttal/PROMPT.md and follow the rebuttal workflow."
codex exec --sandbox workspace-write "Read ./rebuttal/PROMPT.md and follow the rebuttal workflow. Review source: https://openreview.net/forum?id=EXAMPLE. Proceed without additional author context."
```

### OpenCode

```sh
opencode --prompt "Read ./rebuttal/PROMPT.md and follow the rebuttal workflow."
opencode run "Read ./rebuttal/PROMPT.md and follow the rebuttal workflow. Review source: https://openreview.net/forum?id=EXAMPLE. Proceed without additional author context."
```

## Review the drafts

Start with `rebuttal/summary.md` for reviewer priorities, draft readiness, and outstanding author tasks. Read `rebuttal/review-N-analysis.md` and edit `rebuttal/review-N-reviewer-answer.md`. After replacing placeholders, rerun the character counter with the applicable limit, for example:

```sh
python rebuttal/count_rebuttal.py rebuttal/review-1-reviewer-answer.md --limit 5000
```

