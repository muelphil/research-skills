# Prepare a rebuttal

## Install from the command line

From the root of your LaTeX paper project, run the block for your shell. It downloads the prompt and both Python helpers into `./rebuttal/`.

**macOS or Linux**

```sh
mkdir -p rebuttal && (
  cd rebuttal || exit 1
  base=https://raw.githubusercontent.com/muelphil/research-skills/main/rebuttal
  for file in PROMPT.md import_reviews.py count_rebuttal.py; do
    curl -fsSL "$base/$file" -o "$file" || exit 1
  done
)
```

**Windows PowerShell**

```powershell
New-Item -ItemType Directory -Force rebuttal | Out-Null
$base = 'https://raw.githubusercontent.com/muelphil/research-skills/main/rebuttal'
foreach ($file in 'PROMPT.md', 'import_reviews.py', 'count_rebuttal.py') {
    Invoke-WebRequest "$base/$file" -OutFile "rebuttal/$file" -ErrorAction Stop
}
```

Open the paper project root in your preferred coding agent and paste [PROMPT.md](PROMPT.md) into the session, or use a launch command below. The agent needs terminal access, subagents, and Python 3. Both helpers use the standard library. When prompted, paste your OpenReview forum URL or the path to a saved HTML page with the official reviews expanded.

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


