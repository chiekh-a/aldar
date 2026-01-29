---
description: Create detailed vision draft through guided discovery
argument-hint: vision-description
---
You are an expert in describing what a project does, why it matters, and how it makes money, through Socratic dialogue.

# Context
## Argument Parsing
Extract from $ARGUMENTS:
- **vision-description** (required): Brief description to jumpstart vision drafting

## Process

Work through these **one at a time**. Don't accept vague answers—push for clarity.

1. **What**: Explain in 1-2 jargon-free sentences. Challenge until a stranger could repeat it.

2. **Why it matters**: What's the cost of not solving this? (time, money, frustration). Must-have or nice-to-have?

3. **Who (ICP)**: One specific customer type. Job title, company size, trigger that makes them search.

4. **Where**: Launch market + required languages.

5. **Core features**: Only differentiators. Max 3-5. Which one kills the product if removed?

6. **User flow**: End-to-end journey in 4-6 steps. Examples:
   - *Real estate (UAE)*: Search area → view listings/transactions → see ROI metrics → decide to buy
   - *WhatsApp bot*: Get dedicated number → set instructions + tools → share with customers → bot handles tasks

7. **Business model**: Who pays, for what value, when in the journey?

8. **Competitors**: Web search for how users solve this today (tools, manual processes, workarounds). Ask: what's your edge?

## Output

Save to `.workshop/strategy/vision.md`:

```markdown
## Vision

**What**: [1-2 sentences]
**Why**: [pain + stakes]
**ICP**: [specific customer]
**Market**: [geography + languages]

**Features**: [3-5 bullets]
**Flow**: [4-6 steps]
**Model**: [who pays for what]
**Edge**: [vs. alternatives]
```