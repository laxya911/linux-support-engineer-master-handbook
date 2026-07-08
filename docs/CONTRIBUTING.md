# Contributing Guide

Thank you for your interest in contributing to the **Linux Support Engineer Master Handbook**! Since this is a comprehensive, production-grade guide, we want to maintain the highest standard of clarity, formatting, and technical accuracy.

---

## Content Standards

* **Support-Focused**: When explaining concepts, focus on how a support engineer or administrator would interact with them. Always answer: *What could go wrong here? How do I troubleshoot it?*
* **Keep Comparisons Balanced**: Windows-to-Linux comparisons should be used sparingly and strategically—only where terms look similar or where a concept translates directly. Do not saturate every page with comparisons.
* **Hands-on Verification**: Every command, lab instruction, and code block must be tested and verified on standard enterprise distributions (primarily Ubuntu Server and Rocky Linux / Red Hat Enterprise Linux).

---

## File Naming Conventions

* All chapter files should be placed inside the `chapters/` folder of their respective volume.
* Chapters must be named using the format `V[VolumeNumber]-C[ChapterNumber]-[Short-Title].md`.
  * *Example*: `V1-C01-Welcome-to-Linux-Support-Engineering.md`
  * *Example*: `V1-C10-Linux-File-Permissions.md`
* File names should be lowercase and hyphenated, except for the volume and chapter prefixes.

---

## Markdown Formatting Guidelines

To ensure visual consistency, please follow these markdown patterns:

### 1. Headings
Use a single `#` heading for the chapter title, and organize sub-sections using `##` and `###`. Do not skip heading levels.

### 2. Code Snippets
Always specify the language syntax highlighting for code blocks (e.g., `bash`, `text`, `ini`, `yaml`).
* Normal user commands: Use `$` prompt.
* Root/Superuser commands: Use `#` prompt.

```bash
$ echo "Hello World"
# apt-get update
```

### 3. Alerts
Use GitHub-style alerts to highlight critical information:
```markdown
> [!NOTE]
> Detailed background info or helper notes.

> [!IMPORTANT]
> Key requirements or concepts to remember.

> [!WARNING]
> Warnings about unexpected behaviors.

> [!CAUTION]
> High-risk commands that could lead to data loss or service downtime.
```
