# Glossary

Project: Dynamic Web Honeypot

Company: Aetheris Technologies

Version: 1.0

Status: Living Document

Last Updated: 2026-08-01

---

# Purpose

This glossary defines the technical, architectural, cybersecurity, and project-specific terminology used throughout the Dynamic Web Honeypot documentation.

Its purpose is to establish a shared vocabulary, improve consistency across documents, and make the project more accessible to contributors, students, and future maintainers.

---

# Cybersecurity Terms

## Honeypot

A decoy system intentionally designed to attract, detect, and monitor malicious activity without exposing legitimate systems to risk.

---

## Threat Intelligence

Information collected and analyzed about cyber threats, attack techniques, and adversaries to improve defensive capabilities.

---

## IOC (Indicator of Compromise)

Evidence suggesting that a system, network, or application has been compromised by malicious activity.

---

## CSRF (Cross-Site Request Forgery)

A web application attack that tricks an authenticated user into performing unintended actions. CSRF protection helps prevent this type of attack.

---

# Flask & Software Architecture

## Flask

A lightweight Python web framework used to build the Dynamic Web Honeypot.

---

## Application Factory

A Flask design pattern where the application is created through a function rather than a global object, improving modularity and testing.

---

## Blueprint

A Flask component used to organize routes and separate application functionality into reusable modules.

---

## Route

A URL endpoint that maps incoming HTTP requests to Python functions.

---

## Service Layer

The layer responsible for business logic, keeping application behavior separate from request handling.

---

## Model

A Python class representing data stored within the database.

---

# Database Terms

## SQLAlchemy

A Python Object Relational Mapper (ORM) that simplifies communication between Python applications and relational databases.

---

## SQLite

A lightweight, serverless relational database used during the project's initial development phase.

---

# Front-End Terms

## Template

An HTML page rendered dynamically by Flask using the Jinja template engine.

---

## Static Files

Resources that are delivered directly to the browser without server-side processing, including CSS, JavaScript, images, icons, and fonts.

---

# Application Terms

## Logger

A component responsible for recording application events, errors, and security-related activities.

---

## Session

Temporary data stored between HTTP requests to maintain user state during an active browsing session.

---

# Project Terms

## Aetheris Technologies

The fictional enterprise technology company created specifically for the Dynamic Web Honeypot project.

---

## Dynamic Web Honeypot

An educational cybersecurity project that simulates a realistic corporate website while safely monitoring and recording suspicious interactions for research and learning purposes.

---

## Application Factory Pattern

The architectural pattern adopted by the project to improve modularity, scalability, and maintainability.

---

## Living Document

Documentation intended to evolve alongside the project rather than remaining static after its initial creation.

---

# Documentation Terms

## Semantic Versioning (SemVer)

A versioning strategy using the format:

MAJOR.MINOR.PATCH

Example:

v0.1.0

---

## Sprint

A focused development period dedicated to completing a defined set of objectives.

---

## Milestone

A significant project achievement representing the completion of a major phase or objective.

---

# Usage Notes

This glossary is a living document.

Whenever new technical terminology, architectural concepts, or project-specific language is introduced, the corresponding definitions should be added here.

Maintaining a consistent vocabulary improves communication and reduces ambiguity throughout the project documentation.

---