# Repository Structure

This file defines the directory hierarchy of the **Linux Support Engineer Master Handbook** repository. To keep the project clean and navigable, all files should strictly adhere to this structure.

```text
linux-support-engineer-master-handbook/
│
├── README.md                           # Main handbook overview and introduction
├── repository_structure.md             # This file
├── BOOK_STYLE_GUIDE.md                 # Single source of truth for writing and formatting
├── CHANGELOG.md                        # Project release and modification history
├── LICENSE                             # Project licensing agreement
├── .gitignore                          # Git patterns to exclude
│
├── assets/                             # Global media assets for metadata files
│   ├── covers/                         # Book and volume cover images
│   ├── diagrams/                       # Global architecture and flow diagrams
│   ├── icons/                          # Standardized command/info icons
│   └── screenshots/                    # General screenshots (non-volume specific)
│
├── docs/                               # Front-matter and general documentation
│   ├── PREFACE.md                      # Design philosophy and perspective shift
│   ├── HOW_TO_USE_THIS_BOOK.md         # Reading advice and lab setup instructions
│   ├── LEARNING_PATH.md                # Mapping of skills and technical equivalents
│   ├── CONTRIBUTING.md                 # Markdown style guide and guidelines
│   └── ROADMAP.md                      # Release milestones and completion progress
│
└── volumes/                            # Handbook volumes
    └── volume-01-linux-fundamentals/   # Volume 1: Linux Fundamentals
        ├── README.md                   # Volume 1 introduction and overview
        ├── TOC.md                      # Volume 1 detailed Table of Contents
        ├── SUMMARY.md                  # Volume manifest for automated builds
        ├── COMMAND_INDEX.md            # Key terms and command index for Volume 1
        ├── chapters/                   # Directory containing Volume 1 chapters
        ├── practice-files/             # Directory containing standalone chapter practice guides
        └── assets/                     # Media and assets specific to Volume 1
```

> [!NOTE]
> Additional volumes (`volume-02-linux-administration`, etc.) will be added sequentially once the preceding volumes and their chapters are fully drafted.