# vAIbe-OS

> **Your AI agent's operating system** — turn any AI IDE into a structured partner with memory, skills, and evolution.

🇷🇺 [Читать на русском](README.ru.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 🤔 The Problem

You open a new chat with your AI assistant. It's brilliant — for a couple of hours. Then it forgets what you said yesterday. It doesn't know your projects. It can't find that decision you made last week. Every session starts from scratch.

**Sound familiar?**

You're not using AI wrong. Your AI just doesn't have a home.

## 💡 The Solution

vAIbe-OS gives your AI agent a **structured workspace** — a personal vault of projects, tasks, knowledge, and skills that persists across every session.

Think of it as **Obsidian for AI agents**: everything is plain Markdown files in a Git repo. No vendor lock-in, no proprietary formats, no cloud dependency.

| What you get | How it works |
|---|---|
| 🗂️ **Structure** | Projects, tasks, meetings, knowledge base — your AI knows where everything is from day one |
| 🧠 **Memory** | Everything lives in files. Context doesn't disappear when you close the chat |
| 🌱 **Evolution** | The system improves itself via `/evolve`, adapting to how *you* work |
| 🎯 **Skills** | 47 skills for task management, planning, research, design, sales, and strategy — ready to use |
| 📚 **Domain knowledge** | Curated reference skills — project management, strategy frameworks, sales methodologies, startup finance, and more. Your AI has domain expertise from the start |

## 🚀 Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/vaibe-studio/vaibe-os.git
cd vaibe-os

# 2. Run the installer (needs uv — https://docs.astral.sh/uv/)
uv run --project .vaibe/scripts/installer .vaibe/scripts/installer/main.py

# 3. Open in your AI IDE and introduce yourself!
#    Just say: "Hi! I'm [your name], I work on [what you do].
#    Let's get to know each other so you can help me better."
```

That's it. The installer creates your workspace, and your AI agent adapts to your personal work style from the very first conversation.

### 🎮 First things to try

Once you're set up, just talk to your AI agent naturally:

- **"Create a task for my project"** → organizes it in the right place with proper structure
- **"Process my inbox"** → imports files from `Инбокс/` into your knowledge base
- **"What did we learn today? Evolve the system"** → the system improves its own skills based on your session
- **"Give me a morning briefing"** → summarizes your tasks, deadlines, and priorities

## 🏗️ How It Works

vAIbe-OS is built on **one canon, many native wrappers**. You write everything once in `.vaibe/`; per-IDE wrappers are generated from it and committed alongside (the `GENERATED` marker means *don't edit by hand*).

```
vAIbe-OS/
├── 📋 AGENTS.md                              → AI reads this first (rule spine + judgment boundaries)
├── 🧠 .vaibe/                                → The canon — the single source of truth
│   ├── rules/                                → 15 always-on rules (structure, git, behavior, guards…)
│   ├── skills/                               → 47 skills (task mgmt, planning, research, evolve…)
│   ├── agents/                               → Specialized subagents (architect, explorer, reviewer)
│   └── scripts/                              → Python tools as self-contained uv projects (doctor, pdf…)
├── 🤖 .claude/ .cursor/ .codex/ .opencode/   → Generated native wrappers (GENERATED — don't edit)
├── 🩺 CLAUDE.md                              → Generated IDE shim → AGENTS.md
├── 📁 Проекты/                               → Your projects (tasks, meetings, docs)
├── 📚 База знаний/                           → Your personal knowledge base
└── 📥 Инбокс/                                → Drop files here for processing
```

Change the canon, then regenerate and verify the native layer with the built-in **doctor**:

```bash
D=.vaibe/scripts/doctor
uv run --project $D $D/main.py treat       # regenerate native wrappers from the canon
uv run --project $D $D/main.py diagnose    # check canon ↔ native integrity (CI gate)
```

> **Cross-IDE compatible**: works with Cursor, Claude Code, Codex, OpenCode, and any IDE that reads [AGENTS.md](https://agents.md/).

## 🎯 Core Commands

| Command | What it does |
|---|---|
| `/task-create` | Creates a structured task card in your project |
| `/task-execute` | Executes a task with an interactive plan |
| `/inbox-check` | Imports and organizes files from your inbox |
| `/plan-update` | Creates or updates your project plan |
| `/tasks-report` | Shows task status across projects |
| `/daily-briefing` | Morning overview: tasks, deadlines, inbox |
| `/weekly-review` | Weekly progress, blockers, and priorities |
| `/evolve` | System learns from your session and improves itself |

All skills are Markdown playbooks in `.vaibe/skills/` — readable, editable, extensible. The agent discovers them automatically by their `description`; there is no registry to maintain.

## 💚 Philosophy

vAIbe-OS isn't just a folder structure. It's built on a belief that **AI should be a partner, not a tool** — and definitely not a replacement.

Three principles that make it different:

- 🤝 **Partnership** — your AI understands your context, suggests proactively, but never decides for you
- 🛡️ **Autonomy** — if you remove vAIbe-OS tomorrow, you should be *more* competent than before you started using it
- 🌱 **Evolution** — the system grows with you through `/evolve`, getting better at *your* way of working

> Curious about the deeper foundations? See the [Ontology](.vaibe/rules/ontology.md) (5 laws of system evolution) and the [Manifesto](.vaibe/rules/manifesto.md) (behavioral principles).

## 🖥️ Supported AI IDEs

| IDE | How it connects | Status |
|---|---|---|
| **Cursor** | `.cursor/` (generated) | ✅ Full support |
| **Claude Code** | `CLAUDE.md` + `.claude/` (generated) | ✅ Supported |
| **Codex** | `.codex/` (generated) | ✅ Supported |
| **OpenCode** | `AGENTS.md` + `.opencode/` (generated) | ✅ Supported |
| **Any other** | `AGENTS.md` + `.vaibe/` | 🟡 Basic support |

> 💎 **Tip on model choice.** vAIbe-OS works with any LLM, but we recommend leading models (Claude Opus/Sonnet, GPT-4o, Gemini Pro) — skill quality, planning, and `/evolve` are noticeably better on top-tier models. If you have the choice, go with the best.

## 💬 Community

Join the conversation, share your skills, ask questions, and shape where vAIbe-OS goes next:

- 📨 **Telegram** — [t.me/vAIbe_OS](https://t.me/vAIbe_OS)

## 🌱 Supporting vAIbe-OS

vAIbe-OS is free for personal and team use — forever. No strings attached.

If you use it commercially and it helps your business generate revenue, we'd be grateful for a voluntary contribution. We suggest 1–5% of the net profit vAIbe-OS helped create. These funds go directly toward development, community building, and keeping the project alive.

| Method | Link | Best for |
|--------|------|----------|
| 🇷🇺 Boosty | [boosty.to/vaibe_os](https://boosty.to/vaibe_os/donate) | Russian cards, SBP, international cards (USD/EUR), PayPal |
| ₿ Crypto | See below | Works worldwide, no restrictions |

<details>
<summary>💰 Crypto wallets</summary>

| Coin | Network | Address |
|------|---------|---------|
| USDT | TRC-20 | `29YoJ7rdjVPkkpuHFbKj3picPQTW1N2vawU28NHgd7rF` |
| BTC | Bitcoin | `bc1qj5s2tmtp4nvnr3vzpgjsd5m0568f2arfc8vucu` |
| ETH | Ethereum | `0x98804f5e2E9BfEEec04f745c5A6C81f3a8E4FD12` |
| SOL | Solana | `29YoJ7rdjVPkkpuHFbKj3picPQTW1N2vawU28NHgd7rF` |
| TON | TON | `UQDCLj4yhDXX0RYyvcRJmsvDPWZvib75UxUA0FUWr0LS8e2A` |

</details>

## 🤝 Contributing

We'd love your help! Here's how to get started:

**Add a new skill:**
1. Create `.vaibe/skills/your-skill/SKILL.md` with YAML frontmatter (`name`, `description`)
2. Include: Purpose, Procedure, Output format, Quality bar
3. Regenerate the native wrappers: `uv run --project .vaibe/scripts/doctor .vaibe/scripts/doctor/main.py treat`
4. The agent discovers it automatically by its `description` — no registration needed

**Improve existing skills:** Every skill is a Markdown file in `.vaibe/skills/`. Read it, improve it, regenerate, submit a PR.

**Report issues:** Found a bug or have an idea? [Open an issue](../../issues).

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

[MIT](LICENSE) — use it however you want. We just ask that you share the love. 💚

---

<p align="center">
  <strong>vAIbe-OS</strong> — your second brain, structured for AI<br>
  <em>Built with 💚 by humans and AI agents working together</em>
</p>
