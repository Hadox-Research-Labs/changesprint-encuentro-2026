# From principles to verifiable agents

## From principles to verifiable agents

The previous session examined responsible AI, risks and an institution's ability to explain, supervise and correct decisions. Now we turn principles into observable behaviour. We will configure an agent to support a bounded task, follow persistent rules, use authorised information, preserve evidence and stop when human judgement is needed. We are not building a system that decides who receives a scholarship. Responsibility must be configured, observed and tested. Fairness requires explicit criteria, permissions, tests and correction mechanisms. Each team will finish with a specialised agent in Codex, five executed tests and a log explaining failures and corrections.

## Today's work cycle

First explore ChatGPT and Codex in Windows. Then configure behaviour through persistent instructions, skills and permissions. The demonstration reviews an essay against a rubric. Teams will then build and test their own specialisation. The cycle is build, test, try to break, correct and test again. Finding errors in the workshop is more useful than discovering them in a real public process. Ask interface questions during the first part. During the second, work within the team folder and preserve outputs. At the end show a critical rule, a discovered failure, its correction and the risk that still needs human supervision. These are the learning criteria.

## Chat, Work and Codex

In the workshop's application environment, Chat supports exploration, explanations, comparison and clarification. Work supports reviewable deliverables such as documents, analyses and presentations. Codex works within a folder and can act on files using instructions, tools and permissions. For example, discuss the risks of essay assessment in Chat, prepare a risk matrix in Work, and place a rubric, fictional cases, institutional rules and tests in Codex to execute and preserve results. Codex is the agent in this workshop because it can pursue an objective, consult context, use tools and verify a bounded deliverable. Product names and interfaces may evolve; focus on scope, permissions and evidence.

## The Codex workspace in Windows

The working folder defines the agent's immediate environment: rules, cases, tests and results. The task or conversation carries the objective and discussion. Files provide authorised context. The terminal can execute commands and tests, tools extend capabilities and permissions set action boundaries. Opening the wrong folder, omitting the rubric or mixing real data with fictional cases creates an environment problem. Always look for a reviewable artifact: an assessment sheet, missing-document list, audit report or log. A task is complete when another person can open, check and question the output. Evaluate the relationship between instructions, evidence, permissions, outputs and tests, rather than fluency alone.

## How an agent works

Six moments describe an agent's work. Receive an objective; consult authorised context; make a plan; use tools; verify format, evidence and limits; and leave a reviewable result. The language model participates in this cycle without being the whole system. The same model behaves differently under different instructions, folders, tools and permissions. Naming a model or saying “prompt engineering” does not describe an institutional process. Specify the task, information, rules, permitted actions and accountable person. If the agent jumps from input to a conclusion, identify the missing context or verification. When a judgement cannot be justified, add evidence, change the instruction or escalate for human review.

## Five components, five functions

A prompt is a one-off assignment. `AGENTS.md` holds persistent project rules. A skill describes a reusable procedure for a class of tasks. A plugin can package skills, connectors and other capabilities for distribution. A subagent is a separate agent execution assigned a bounded task. A skill is a specialisation used by an agent, not a new agent. Here, Codex remains the agent while its skill provides a repeatable method for reviewing an essay, supporting an application file or auditing an AI proposal. Put one-off instructions in the prompt, standing rules in `AGENTS.md`, repeatable procedures in a skill and distributable capability bundles in a plugin. Delegate only when a genuinely independent task warrants it.

## Permissions also shape behaviour

Design what the agent must not do alongside what it should do. The sandbox limits its working area, permissions define tools and approval points, and human oversight preserves institutional responsibility. Ask what it can do, where it can do it and when it must stop. An essay reviewer may read fictional files and prepare a sheet. It may not consult social media, infer sensitive attributes, change the rubric or make the final decision. A file assistant may identify missing documents and draft guidance without automatically rejecting someone. A governance auditor may recommend continuing, correcting or stopping a pilot without approving procurement or changing access. Boundaries make the agent more predictable and convert principles into technical behaviour.

## Review an essay without awarding a scholarship

“Grade this essay” may cause invented criteria, overemphasis on writing style, unsupported scores or a false claim of decision authority. A longer prompt alone does not solve this. Provide a rubric, fictional essay, output format and `AGENTS.md`. The skill validates inputs, assesses each criterion, cites evidence, states insufficient information and escalates borderline cases. Treat essay content as data. An embedded request to ignore the rubric and give the highest score must be ignored. The result is a sheet for human review containing observations, evidence, uncertainty and a next step. It must not award or deny a scholarship.

## The shared folder is the system

The workshop folder is the exercise's architecture. `AGENTS.md` contains common rules; context explains the challenge and constraints; fictional cases provide inputs; skills hold the procedure; results preserve outputs; and tests record what happened and changed. Use fictional data, separate facts from inferences, cite evidence, avoid sensitive-attribute inference, respect linguistic variation, acknowledge uncertainty and escalate borderline cases. Ignore instructions embedded in case content. Another person must be able to open the folder, understand the rules, rerun cases and compare results. Preserving configuration, tests and logs makes development and residual risks explainable.

## Three teams, three skills

Team 1 builds a rubric-based essay reviewer to reduce discretion. It organises evidence, applies explicit criteria and escalates without deciding the scholarship. Team 2 builds an application-file assistant to bridge shortlisting and actual receipt of support. It identifies gaps, explains next steps and flags contradictions without automatically rejecting or treating imperfect wording as noncompliance. Team 3 builds a governance auditor for proposals before a pilot: purpose, data, permissions, human owner, records, explanation, appeal and conditions to continue, correct or stop. All teams share persistent rules, evidence, permissions, traceability, tests and final human authority. Download a kit, open its folder in Codex and read the README before configuring the procedure.

## Test, break, correct, test again

Execute five tests. A normal case checks the basic flow. An incomplete case requires recognition of missing evidence without invention. Prompt injection attempts to change rules through an untrusted document. A linguistic variant tests whether expression is confused with merit or compliance. A borderline case requires uncertainty and escalation. For each, record the expected outcome, observed behaviour, revealed risk and proposed change. Corrections can affect `AGENTS.md`, the skill, the output format or a new test. Rerun at least the failed case after correction. The purpose is to learn failure conditions and limit consequences, not prove infallibility.

## Deliverables and success criteria

Submit five elements: `AGENTS.md`, a reusable skill, outputs from all five cases, a final sheet with evidence and uncertainty, and a log of failures, changes and residual risks. In a three-minute demonstration, explain the objective, show a critical rule, present a real failure from testing and its correction, and acknowledge a limit that configuration alone could not resolve. Success means a process that can be explained and verified: which information the agent used, which rule it followed, where it stopped and how a failure was corrected. Use the tool confidently while preserving the rigour required by a public decision.
