# Book Style Guide

This document is the single source of truth for writing, formatting, and structuring the **Linux Support Engineer Master Handbook**. All contributions must adhere to these guidelines to ensure consistency across all volumes and chapters.

---

## 1. Terminology and Voice

* **Target Title**: Always use **Linux Support Engineer**. Do not use "Linux Engineer", "Support Admin", or "SysAdmin" unless drawing a direct comparison.
* **Tone**: The voice should be authoritative yet accessible. It should sound like a senior engineer mentoring a junior engineer—practical, direct, and focused on real-world troubleshooting.
* **Focus**: Prioritize **why** something fails and **how** to fix it over simply reciting how to configure it.

---

## 2. File Naming Conventions

* **Chapters**: `V[VolumeNumber]-C[ChapterNumber]-[short-title].md` (e.g., `V1-C01-welcome-to-linux-support-engineering.md`). Use lowercase, hyphenated words.
* **General Documents**: ALL CAPS for core reference files (e.g., `README.md`, `TOC.md`, `COMMAND_INDEX.md`).
* **Images/Assets**: `v[volume]-[chapter]-[short-desc].png` (e.g., `v1-c02-linux-architecture.png`).

---

## 3. Heading Hierarchy

Do not skip heading levels.
* `#` (H1): Used exclusively for the main Chapter Title or Document Title.
* `##` (H2): Used for primary sections (e.g., Learning Objectives, Introduction, Hands-on Lab).
* `###` (H3): Used for sub-sections (e.g., specific concepts, individual lab steps).
* `####` (H4): Used sparingly for deeply nested steps or minor breakdowns.

---

## 4. Markdown and Callout Conventions

### Callouts (GitHub Alerts)
Do not invent new callout types. Restrict usage to the following five official GitHub alerts:

```md
> [!NOTE]
> General background context or comparisons (e.g., Windows vs. Linux notes).

> [!TIP]
> Best practices or efficient workflows.

> [!IMPORTANT]
> Key concepts or "Senior Engineer Thinking" insights.

> [!WARNING]
> Common pitfalls, mistakes, or mild troubleshooting warnings.

> [!CAUTION]
> Actions that can cause downtime, data loss, or system failure.
```

### Links
* **Always use relative paths** for internal links. Do not use absolute paths (e.g., `file:///`).
* Example: `[Chapter 2](../chapters/V1-C02-linux-architecture-and-distributions.md)`

### Code Blocks
Always specify the syntax language.
* Terminal output or simple text: `text`
* Configuration files: `ini`, `yaml`, `conf`
* Shell commands: `bash`
  * Use `$` for standard user execution.
  * Use `#` for root/superuser execution.

---

## 5. Dual-Distribution Approach

This handbook is designed to teach both **Debian-based** (e.g., Ubuntu Server) and **RHEL-based** (e.g., RHEL, CentOS, Rocky Linux) distributions simultaneously.
* **Shared Commands**: When a command applies to both (e.g., `cat`, `grep`, `systemctl`), present it universally without distinction.
* **Diverging Commands**: When package managers, file paths, or specific utilities differ, you **must** explicitly split the instruction. Do not assume the reader knows which to use.
  
Example:
> **Debian/Ubuntu**: `# apt install nginx`
> **RHEL/Rocky**: `# dnf install nginx`

---

## 6. Chapter Template Structure

Every chapter must begin with YAML frontmatter, followed immediately by the chapter title, a statistics block, and standard sections.

### YAML Frontmatter
```yaml
---
volume: 1
chapter: 1
part: 1
id: V1-C01
title: Chapter Title Here
difficulty: Beginner
estimated_time: 2-3 Hours
reading_time: 40 Minutes
labs: 1
interview_questions: 2
prerequisites: None
last_updated: YYYY-MM
status: Draft
---
```

### Required Markdown Sections (In Order)
1. `# Chapter X — Title`
2. **Statistics Block** (Bulleted list directly under the title)
   * **Difficulty:** Beginner
   * **Estimated Time:** 2 Hours
   * **Hands-on Labs:** 1
   * **Interview Questions:** 2
3. `## Learning Objectives`
4. `## Introduction`
5. `## Theory & Concepts`
6. `## Real-World Scenarios`
7. `## Hands-on Lab`
8. `## Interview Questions`
9. `## Chapter Summary`
10. `## Completion Checklist`
11. `## Navigation` (Footer with Previous, Volume Contents, and Next links)
