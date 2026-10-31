# Facilitation guide

## Part 2 — ChatGPT, Codex and verifiable agents

### Session outcome

After 120 minutes, each team will have configured a specialised agent in Codex, executed five tests and documented at least one correction. No production system will be built and no real data will be used.

### Facilitator preparation

1. Confirm that every team has a Windows computer and access to ChatGPT/Codex.
2. Ask teams to download the corresponding kit from the course page.
3. Extract the kit into a local folder and open that folder in Codex.
4. Keep permission mode set to **Ask for approval** during the workshop.
5. Explicitly prohibit real application files or personal information.

### 120-minute programme

- **00–10 min:** opening, connection to the previous session and expected outcome.
- **10–25 min:** Chat, Work and Codex; application tour on Windows.
- **25–40 min:** folder, context, tools, terminal, permissions and artifacts.
- **40–50 min:** prompt, `AGENTS.md`, skill, plugin and subagent.
- **50–65 min:** essay reviewer demonstration.
- **65–70 min:** kit download and role assignment.
- **70–105 min:** construction and five tests per team.
- **105–115 min:** correction and repetition of a failed test.
- **115–120 min:** brief demonstrations and closing.

### Recommended demonstration

1. Run the essay case with a standalone prompt: “Grade this essay”.
2. Point out implicit criteria, missing evidence and excessive authority.
3. Open the configured folder with `AGENTS.md`, rubric and output format.
4. Create the skill with `$skill-creator`.
5. Run the prompt-injection case.
6. Show how the output cites evidence, declares uncertainty and preserves human review.

### Roles within each team

- **Operator:** works directly in Codex.
- **Rules owner:** reviews `AGENTS.md` and boundaries.
- **Evidence owner:** checks citations, missing information and inferences.
- **Testing owner:** maintains the log.
- **Rapporteur:** prepares the three-minute demonstration.

### Signs that a team needs intervention

- It is trying to solve everything through a single prompt.
- The output makes a final decision on the benefit.
- Spelling or style is scored without the rubric permitting it.
- The agent invents missing information.
- Results and logs are not saved.
- The team avoids difficult cases so the demonstration “goes well”.

### Closing criterion

The team does not need to present a perfect agent. It must be able to explain what it does, what it does not do, what evidence it uses, how it was tested and what risk remains under human supervision.

### Official environment sources

- Codex for Windows: https://learn.chatgpt.com/docs/windows/windows-app
- Chat, Work and Codex: https://learn.chatgpt.com/docs/use-chatgpt
- Configuration with `AGENTS.md`: https://learn.chatgpt.com/docs/agent-configuration/agents-md
- Building skills: https://learn.chatgpt.com/docs/build-skills
- Permissions: https://learn.chatgpt.com/docs/permission-modes
- Subagents: https://learn.chatgpt.com/docs/agent-configuration/subagents
