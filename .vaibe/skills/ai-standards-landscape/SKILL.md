---
name: ai-standards-landscape
description: ISO 42001, NIST AI RMF, EU AI Act, responsible AI, LLM evaluation standards. Reference material (non-actionable knowledge).
license: MIT
---

# AI Standards and Governance Landscape

Practical reference for AI regulation, standards, risk management frameworks, responsible AI principles, and LLM evaluation practices. Enables the agent and user to navigate the evolving AI governance landscape, assess compliance requirements, and build trustworthy AI systems.

Meta-relevance: vAIbe-OS is itself an AI system. Understanding these standards is both a product knowledge need and a self-governance concern.

## When to use

- Evaluating AI-related risks in projects involving ML/LLM integration
- Assessing compliance requirements for AI products targeting EU or international markets
- Designing responsible AI practices for development teams
- Selecting or evaluating AI models and tools
- Preparing governance documentation for AI systems
- Building trust with stakeholders around AI usage

---

## ISO/IEC 42001:2023 — AI Management System

### What it is

The world's first international standard for Artificial Intelligence Management Systems (AIMS). Published December 2023 by ISO/IEC. Certifiable — organizations can obtain third-party certification.

### Structure

Follows the Annex SL high-level structure (same as ISO 27001, ISO 9001, ISO 14001), enabling integration with existing management systems.

| Clause | Topic | Key requirements |
|---|---|---|
| 4 | Context of the organization | Understand stakeholders, scope, internal/external factors affecting AI |
| 5 | Leadership | Top management commitment, AI policy, roles and responsibilities |
| 6 | Planning | AI risk assessment, risk treatment, system impact assessment, objectives |
| 7 | Support | Resources, competence, awareness, communication, documented information |
| 8 | Operation | Operational planning, AI risk assessment execution, impact assessment |
| 9 | Performance evaluation | Monitoring, measurement, internal audit, management review |
| 10 | Improvement | Nonconformity, corrective action, continual improvement |

### Key controls (Annex A)

- AI governance policies and organizational roles
- AI risk assessment and treatment procedures
- Data quality and data governance
- Bias detection and mitigation
- Transparency and explainability requirements
- Human oversight mechanisms
- Impact assessments (individual and societal)
- AI incident management and response
- Supply chain and third-party AI governance

### When it matters

Relevant for any organization developing, deploying, or procuring AI systems. Particularly valuable for: demonstrating due diligence to regulators, building customer trust, structuring internal AI governance, and preparing for EU AI Act compliance (complementary frameworks).

---

## NIST AI Risk Management Framework (AI RMF 1.0)

### What it is

Voluntary framework released by NIST in January 2023 for managing risks throughout the AI system lifecycle. Designed to be flexible, non-sector-specific, and use-case agnostic. Accompanied by a detailed Playbook with suggested actions.

### Four core functions

#### Govern (cross-cutting)

Cultivates a culture of risk management. Establishes policies, processes, accountability structures, and organizational commitment. Infused throughout the other three functions.

Key categories:
- Govern 1: Policies, processes, and practices for AI risk management
- Govern 2: Accountability structures, roles, training
- Govern 3: Workforce diversity, equity, inclusion in AI risk management
- Govern 4: Organizational culture of AI risk awareness
- Govern 5: Engagement with external AI actors and stakeholders
- Govern 6: Third-party and supply chain risk management

#### Map (context and risk identification)

Establishes context for framing AI risks. Identifies intended purposes, stakeholders, potential impacts, system categorization, and risk/benefit analysis.

Key categories:
- Map 1: Context established — purposes, laws, norms, deployment settings
- Map 2: System categorization — tasks, methods, knowledge limits, human oversight
- Map 3: Capabilities and benchmarks — benefits, costs, scope, proficiency requirements
- Map 4: Component risks — third-party software, data, IP considerations
- Map 5: Impact characterization — individuals, groups, communities, society

#### Measure (assessment and monitoring)

Quantitative, qualitative, and mixed-method analysis of AI risk. Includes testing, evaluation, verification, and validation (TEVV). Establishes metrics for trustworthiness, social impact, and human-AI interaction.

Key categories:
- Measure 1: Appropriate metrics identified and applied
- Measure 2: AI systems evaluated for trustworthy characteristics
- Measure 3: Mechanisms for tracking identified risks over time
- Measure 4: Feedback mechanisms for measurement improvement

#### Manage (response and mitigation)

Allocates resources to mapped and measured risks. Implements risk treatment plans. Prioritizes responses based on impact and likelihood.

Key categories:
- Manage 1: Risks prioritized based on impact, likelihood, and available resources
- Manage 2: Strategies to maximize benefits and minimize negative impacts
- Manage 3: Risks from third-party entities managed
- Manage 4: Regular monitoring and response adjustments

### Trustworthy AI characteristics (NIST)

The framework identifies seven characteristics of trustworthy AI:

1. **Valid and reliable** — performs as intended under expected and unexpected conditions
2. **Safe** — does not endanger human life, health, property, or environment
3. **Secure and resilient** — resistant to attacks, maintains functionality under adversity
4. **Accountable and transparent** — clear about capabilities, limitations, and decision processes
5. **Explainable and interpretable** — outputs can be understood by intended users
6. **Privacy-enhanced** — protects personally identifiable information and individual autonomy
7. **Fair with harmful bias managed** — does not systematically disadvantage individuals or groups

---

## EU AI Act (Regulation 2024/1689)

### What it is

The world's first comprehensive AI-specific legislation. Adopted by the European Parliament in March 2024, entered into force August 1, 2024. Applies to providers, deployers, importers, and distributors of AI systems in the EU market, regardless of where they are established.

### Risk-based classification

| Risk tier | Examples | Requirements |
|---|---|---|
| **Unacceptable** (prohibited) | Social scoring, manipulative AI, emotion recognition in workplaces/schools, untargeted facial recognition databases, predictive policing based solely on profiling | Banned entirely |
| **High risk** | Medical diagnosis, autonomous driving, biometric identification, critical infrastructure, education, employment, law enforcement, migration | Conformity assessment, risk management, data governance, transparency, human oversight, accuracy/robustness requirements |
| **Limited risk** (transparency) | Chatbots, AI-generated content, deepfakes | Must disclose AI interaction to users; label AI-generated content |
| **Minimal risk** | Spam filters, video game AI, inventory management | No specific obligations |

### General-purpose AI (GPAI) models

Special rules for foundation models and general-purpose AI (including LLMs):
- All GPAI: technical documentation, transparency, copyright compliance
- Systemic risk GPAI (high-capability models): additional obligations including adversarial testing, incident reporting, cybersecurity measures

### Implementation timeline

| Date | Milestone |
|---|---|
| August 1, 2024 | Act enters into force |
| February 2, 2025 | Prohibitions and AI literacy requirements apply |
| August 2, 2025 | GPAI model rules, governance bodies, penalties apply |
| August 2, 2026 | High-risk AI rules (Annex III), transparency obligations, national enforcement, regulatory sandboxes |
| August 2, 2027 | High-risk AI in regulated products; full compliance deadline |

### Penalties

- Prohibited AI violations: up to EUR 35 million or 7% of global annual turnover
- High-risk non-compliance: up to EUR 15 million or 3% of turnover
- Incorrect information to authorities: up to EUR 7.5 million or 1% of turnover

---

## Responsible AI principles

Across major frameworks (NIST, OECD, Microsoft, Google, Partnership on AI), responsible AI converges on these principles:

### Core principles

| Principle | Description |
|---|---|
| **Fairness** | AI should not create or reinforce unfair bias. Outcomes should be equitable across demographic groups |
| **Transparency** | Stakeholders should understand how AI systems work, what data they use, and what their limitations are |
| **Accountability** | Clear ownership of AI systems and their outcomes. Mechanisms for redress when things go wrong |
| **Explainability** | Users should be able to understand AI decisions at an appropriate level of detail |
| **Safety** | AI systems should operate reliably and not cause harm under normal or adversarial conditions |
| **Privacy** | Personal data must be protected. Users should have control over their data |
| **Human oversight** | Humans should remain in control of high-stakes decisions. AI augments, not replaces, human judgment |
| **Robustness** | Systems should perform consistently under varying conditions and resist adversarial manipulation |

### Applying to vAIbe-OS

vAIbe-OS embodies several responsible AI principles by design:

| Principle | vAIbe-OS implementation |
|---|---|
| Transparency | Manifesto publicly states capabilities and limitations; LLM limitations acknowledged |
| Human oversight | Judgment boundaries in AGENTS.md; confirmation steps before file operations |
| Accountability | Task versioning (results/v1, v2); change tracking via evolve skill |
| Fairness | Manifesto: "Do not impose values"; respect for subjective experience |
| Privacy | Personal projects via .gitignore; no external data transmission by default |
| Safety | `rules/guards.md` invariants; red lines in Manifesto |

---

## LLM evaluation and safety

### Evaluation dimensions

Modern LLM assessment covers seven dimensions:

1. **Accuracy and knowledge** — factual correctness, domain expertise, reasoning
2. **Safety and harm prevention** — refusal of harmful requests, content policy adherence
3. **Fairness and bias** — equitable performance across demographics and topics
4. **Robustness** — consistent performance under input variation, adversarial prompts
5. **Calibration and uncertainty** — model knows what it doesn't know
6. **Efficiency** — inference speed, cost, resource consumption
7. **Alignment and helpfulness** — follows instructions, provides useful responses

### Key benchmarks

| Benchmark | What it tests | Notes |
|---|---|---|
| **HELM** | Holistic evaluation across language, vision, reasoning | Most comprehensive academic benchmark |
| **MMLU / MMLU-Pro** | Knowledge across 57+ subjects | Many models saturate MMLU; Pro version is harder |
| **TruthfulQA** | Hallucination and truthfulness | State-of-art models score surprisingly low |
| **HumanEval / MBPP** | Code generation | Pass@k metric; standard for coding capability |
| **HarmBench** | Red teaming and safety | 510 test cases; shows larger models ≠ safer |
| **AgentHarm** | LLM agent safety in tool use | Multi-step malicious task compliance testing |
| **MT-Bench** | Multi-turn conversation quality | Tests coherence, instruction following, reasoning |

### Red teaming practices

Systematic adversarial testing to discover vulnerabilities:
- Select diverse red team composition (security, domain experts, diverse demographics)
- Test categories: prompt injection, jailbreaking, harmful content generation, data extraction, bias elicitation
- Document findings with severity ratings and reproducibility
- Iterate: fix → retest → expand scope
- Distinguish between theoretical and practical risks

### AI-generated code risks

24.7% of AI-generated code contains security vulnerabilities (2025 data). Mitigations:
- Run SAST/SCA on all AI-generated code (see `.vaibe/skills/devops-practices/SKILL.md`)
- Review AI output with same rigor as human code
- Maintain security awareness in AI-assisted workflows
- Don't trust AI-generated code in security-sensitive contexts without verification

---

## Standards comparison and selection guide

| Need | Primary framework | Complementary |
|---|---|---|
| Certifiable AI management system | ISO/IEC 42001 | NIST AI RMF for operational detail |
| Risk-based approach to AI governance | NIST AI RMF | ISO 42001 for management structure |
| EU market compliance | EU AI Act | ISO 42001 for conformity evidence |
| Internal responsible AI program | NIST trustworthy AI characteristics | EU AI Act for regulatory alignment |
| LLM safety and evaluation | Red teaming + benchmarks | NIST AI RMF Measure function |
| Third-party AI procurement | ISO 42001 Annex A supply chain controls | NIST AI RMF Govern 6, Map 4 |

## Decision heuristics

- **Building AI for EU market** → start with EU AI Act risk classification; use ISO 42001 for management system; NIST AI RMF for operational detail
- **Internal AI tools (no external deployment)** → NIST AI RMF is sufficient; ISO 42001 if certification needed for enterprise clients
- **Using third-party LLMs** → assess provider's compliance; document your own risk assessment (NIST Map function); test outputs (NIST Measure)
- **Startup with limited resources** → prioritize responsible AI principles and basic risk assessment; formal certification can come later
- **AI in high-stakes domain (health, finance, legal)** → all three frameworks; emphasize human oversight, explainability, and bias testing

## Anti-patterns

- **Compliance theater** — checking boxes without genuine risk assessment; frameworks require substantive engagement
- **AI ethics washing** — publishing principles without implementing controls or measurement
- **Benchmark gaming** — optimizing for popular benchmarks while ignoring real-world failure modes
- **One-time risk assessment** — AI risks evolve as models, data, and deployment contexts change; continuous monitoring required
- **Ignoring GPAI rules** — assuming foundation model rules don't apply if you're "just using an API"; deployer obligations exist
- **Safety vs capability trade-off myth** — treating safety measures as obstacles to performance; well-governed AI systems are more reliable
- **Voluntary = optional thinking** — NIST AI RMF is voluntary, but it represents best practice; regulators and courts reference it

## Sources

- ISO/IEC 42001:2023. *Information technology — Artificial intelligence — Management system.* `https://www.iso.org/standard/81230.html`
- NIST. *AI Risk Management Framework (AI RMF 1.0).* January 2023. `https://nist.gov/itl/ai-risk-management-framework`
- NIST. *AI RMF Playbook.* `https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook`
- NIST. *AI 600-1: Generative AI Profile (companion to AI RMF).* July 2024. `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`
- EU. *Regulation (EU) 2024/1689 — Artificial Intelligence Act.* Official Journal, July 2024. `https://artificialintelligenceact.eu/`
- EU AI Act implementation timeline: `https://artificialintelligenceact.eu/implementation-timeline`
- DORA. *State of AI-assisted Software Development 2025.* `https://dora.dev/research/2025/dora-report`
- Responsible AI Labs. *LLM Evaluation Benchmarks 2025.* `https://responsibleailabs.ai/knowledge-hub/articles/llm-evaluation-benchmarks-2025`
- Cross-reference: `.vaibe/skills/devops-practices/SKILL.md` — DevSecOps and AI-generated code security
- Cross-reference: `.vaibe/rules/ontology.md` — vAIbe-OS ontological foundation (self-governance)
- Cross-reference: `.vaibe/rules/manifesto.md` — behavioral principles (transparency, honesty about LLM limitations)
