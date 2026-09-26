# Development Workflow

## 1. Overview

The project will use Git for version control and GitHub for remote source
code management.

Development will follow a structured workflow instead of making all changes
directly on the main branch.

The workflow will be:

```text
Create Issue / Task
       |
       v
Create Feature Branch
       |
       v
Implement Change
       |
       v
Run Tests Locally
       |
       v
Commit Changes
       |
       v
Push Branch
       |
       v
Create Pull Request
       |
       v
GitHub Actions CI
       |
       v
Review / Fix
       |
       v
Merge to Main