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
| 🎯 **Skills** | 14 core skills for task management, planning, reporting, and more — ready to use |
| 📚 **Knowledge base** | 15+ curated reference materials — project management, strategy frameworks, sales methodologies, startup finance, and more. Your AI has domain expertise from the start |

## 🚀 Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/vaibe-os/vaibe-os.git
cd vaibe-os

# 2. Run the installer
python tools/installer/install.py

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

vAIbe-OS is a set of Markdown files that any AI IDE can read and follow:

```
vAIbe-OS/
├── 📋 AGENTS.md              → AI reads this first (judgment boundaries)
├── 🧠 .ai/                   → The brain: skills, knowledge, philosophy
│   ├── router.md             → Routes your request to the right skill
│   ├── skills/core/          → 14 core skills (task mgmt, planning, evolve...)
│   ├── skills/domain/        → 12 domain skills (presentations, research...)
│   ├── knowledge/            → 15+ reference materials (strategy, PM, sales...)
│   ├── ONTOLOGY.md           → Why the system exists (philosophical foundation)
│   └── MANIFESTO.md          → How the system behaves (principles)
├── 📁 Проекты/               → Your projects (tasks, meetings, docs)
├── 📚 База знаний/           → Your personal knowledge base
├── 📥 Инбокс/                → Drop files here for processing
└── 🔧 tools/                 → Python utilities (installer, vault-lint)
```

> **Cross-IDE compatible**: works with Cursor, Claude Code, OpenCode, and any IDE that reads [AGENTS.md](https://agents.md/).

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

All commands are Markdown playbooks in `.ai/skills/` — readable, editable, extensible.

## 💚 Philosophy

vAIbe-OS isn't just a folder structure. It's built on a belief that **AI should be a partner, not a tool** — and definitely not a replacement.

Three principles that make it different:

- 🤝 **Partnership** — your AI understands your context, suggests proactively, but never decides for you
- 🛡️ **Autonomy** — if you remove vAIbe-OS tomorrow, you should be *more* competent than before you started using it
- 🌱 **Evolution** — the system grows with you through `/evolve`, getting better at *your* way of working

> Curious about the deeper foundations? See our [Ontology](.ai/ONTOLOGY.md) (5 laws of system evolution) and [Manifesto](.ai/MANIFESTO.md) (9 behavioral principles).

## 🖥️ Supported AI IDEs

| IDE | How it connects | Status |
|---|---|---|
| **Cursor** | `.cursor/commands/` + `.cursor/rules/` | ✅ Full support |
| **Claude Code** | `CLAUDE.md` + `.ai/` | ✅ Supported |
| **OpenCode** | `AGENTS.md` + `.ai/` | ✅ Supported |
| **Any other** | `AGENTS.md` + `.ai/` | 🟡 Basic support |

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
1. Create `.ai/skills/domain/your-skill.md` with YAML frontmatter
2. Include: Purpose, Procedure, Output format, Quality bar
3. The router discovers it automatically — no registration needed

**Improve existing skills:** Every skill is a Markdown file. Read it, improve it, submit a PR.

**Report issues:** Found a bug or have an idea? [Open an issue](../../issues).

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

[MIT](LICENSE) — use it however you want. We just ask that you share the love. 💚

---

<p align="center">
  <strong>vAIbe-OS</strong> — your second brain, structured for AI<br>
  <em>Built with 💚 by humans and AI agents working together</em>
</p>
