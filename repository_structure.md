# Repository Structure

This file defines the directory hierarchy of the **Linux Support Engineer Master Handbook** repository. To keep the project clean and navigable, all files should strictly adhere to this structure.

```text
linux-support-engineer-master-handbook/
│
├── README.md                           # Main handbook overview and introduction
├── repository_structure.md             # This file
├── series_structure.md                 # Handbook series outline and goals
├── BOOK_STYLE_GUIDE.md                 # Single source of truth for writing and formatting
├── CHANGELOG.md                        # Project release and modification history
├── lms-website-plan.md                 # Project architecture for LMS platform
├── LICENSE                             # Project licensing agreement
├── .gitignore                          # Git patterns to exclude
│
├── handbooks/                          # Compiled and publishable final PDF volumes
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
    ├── volume01/                       # Volume 1: Linux Fundamentals
    │   ├── chapters/                   # Directory containing Volume 1 chapters
    │   ├── practice-files/             # Directory containing standalone chapter practice guides
    │   ├── scripts/                    # Build scripts for Volume 1 PDF generation
    │   ├── diagrams/                   # Cached Mermaid SVGs
    │   └── assets/                     # Media and assets specific to Volume 1
    ├── volume02/                       # Volume 2: Linux System Administration
    ├── volume03/                       # Volume 3: Enterprise Linux Services
    ├── volume04/                       # Volume 4: Enterprise Infrastructure & Troubleshooting
    └── volume05/                       # Volume 5: Senior Engineer & Optimization
```

> [!NOTE]
> Additional volumes (`volume-02-linux-administration`, etc.) will be added sequentially once the preceding volumes and their chapters are fully drafted.