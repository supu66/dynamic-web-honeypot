# Development Setup

Project: Dynamic Web Honeypot

Company: Aetheris Technologies

Version: 1.0

Status: Active

Last Updated: 2026-08-01

---

# Purpose

This document provides step-by-step instructions for setting up a local development environment for the Dynamic Web Honeypot project.

It is intended to ensure that every contributor follows a consistent setup process, reducing environment-related issues and improving collaboration throughout the software development lifecycle.

---

# Prerequisites

Before setting up the project, ensure that you:

- Have administrator privileges on your development machine.
- Have a stable internet connection to install dependencies.
- Have a GitHub account for version control and collaboration.
- Are familiar with basic Git and command-line operations.

---

# Required Software

The following software is required to develop and run the project locally:

- **Visual Studio Code** — Source code editor
- **Git** — Version control system
- **Python 3.14+** — Application runtime
- **Google Chrome** — Browser for testing
- **GitHub Account** — Repository hosting and collaboration

---

# Recommended VS Code Extensions

- Python
- Pylance
- Black Formatter
- GitLens
- Error Lens
- Markdown All in One
- Material Icon Theme

---

# Clone Repository

```bash
git clone <repository-url>
cd dynamic-web-honeypot
```

---

# Project Initialization

After cloning the repository:

1. Navigate to the project directory.
2. Create a virtual environment.
3. Activate the virtual environment.
4. Install project dependencies.
5. Verify that all required packages are installed before running the application.

---

# Create Virtual Environment

```bash
python -m venv .venv
```

---

# Activate Virtual Environment

Windows

```powershell
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

```bash
python run.py
```

---

# Project Structure

Refer to:

docs/04_System_Architecture.md

---

# Git Workflow

Before working:

```bash
git pull
```

After changes:

```bash
git add .
git commit
git push
```

---

# Development Workflow

The recommended development process is:

1. Pull the latest changes from the repository.
2. Create or update your development environment.
3. Implement a small, focused feature or improvement.
4. Test your changes locally.
5. Update documentation when necessary.
6. Commit changes using Conventional Commits.
7. Push changes to the remote repository.

Following this workflow helps maintain a clean and predictable development process.

---

# Coding Standards

Follow:

docs/03_Engineering_Guidelines.md

---

# Troubleshooting

Common setup issues include:

- Git is not installed or not available in the system PATH.
- The virtual environment has not been activated.
- Required Python packages are missing.
- An unsupported Python version is being used.
- Environment variables are not configured correctly.

When troubleshooting, verify each setup step before proceeding to application-specific debugging.

---

# Future Improvements

- Docker
- Docker Compose
- CI/CD
- Automated testing

---

# Developer Notes

A consistent development environment is essential for maintaining code quality and reducing configuration-related issues.

Contributors are encouraged to follow this setup guide before making changes to the project and to keep their local environment aligned with the documented requirements.

Future updates to the development workflow should be reflected in this document to ensure it remains an accurate onboarding reference.