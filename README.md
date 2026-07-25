# PDFML
PDFML (Portable Document Markup Language)

Overview

PDFML (Portable Document Markup Language) is a lightweight markup language designed specifically for generating PDF documents. It provides a clean, human-readable syntax that enables developers and users to create structured, professional-quality PDF files without manually working with low-level PDF libraries.

Unlike general-purpose markup languages such as HTML, PDFML focuses exclusively on PDF generation. Every element is designed around document layout, typography, and printable content rather than web rendering.

PDFML aims to make PDF creation as simple as writing a document.

---

Why PDFML?

Creating PDF documents often requires writing large amounts of code or learning complex APIs. PDFML simplifies this process by introducing a concise markup language that separates document structure from implementation.

With PDFML, users can describe what a document should contain instead of how to draw every element.

---

Features

Current features include:

- Simple and readable markup syntax
- Native PDF document generation
- Titles, headings, and subtitles
- Paragraph formatting
- Text alignment
- Bold text
- Text color support
- Tables with rows and cells
- Page spacing
- Manual page breaks
- Metadata support
- Multi-page documents
- UTF-8 text support
- Lightweight compiler architecture

---

Planned Features

The PDFML roadmap includes many additional capabilities, including:

- Variables
- Conditional statements ("if", "else if", "else")
- Boolean values
- Loops
- Reusable components
- Template system
- Images
- Lists
- Headers and footers
- Automatic page numbering
- Hyperlinks
- Custom fonts
- Syntax highlighting
- Better error reporting
- Package/import system
- Extensions
- PDF themes

---

Philosophy

PDFML follows several core principles:

- Simple syntax
- Human-readable documents
- Fast compilation
- Easy maintenance
- Consistent formatting
- Focused exclusively on PDF generation

Instead of becoming another HTML alternative, PDFML is designed to be the dedicated language for producing printable PDF documents.

---

Example

{head align="center"}
{b}Hello, PDFML!{/b}
{/head}

{space height=20 /}

{body align="justify"}
Welcome to PDFML.
{/body}

---

Example Output

The example above produces a PDF document with:

- Centered title
- Bold heading
- Vertical spacing
- Justified paragraph

without writing any Python code directly.

---

Architecture

A typical PDFML compilation process follows this pipeline:

PDFML Source
      │
      ▼
Lexer
      │
      ▼
Parser
      │
      ▼
Compiler
      │
      ▼
PDF Document

Each component has a dedicated responsibility:

- Lexer — Tokenizes PDFML source code.
- Parser — Builds the document structure.
- Compiler — Converts parsed nodes into a PDF.
- CLI — Provides command-line compilation.

---

Project Goals

The primary goals of PDFML are:

- Simplify PDF document creation.
- Provide an intuitive markup language.
- Produce professional-quality PDF files.
- Reduce the amount of programming required.
- Keep the syntax clean and consistent.
- Offer a dedicated solution for printable documents.

---

Design Principles

PDFML was created with the following design principles:

- Readability over complexity.
- Explicit document structure.
- Minimal syntax.
- Predictable behavior.
- Extensible architecture.
- Developer-friendly workflow.

---

Current Status

Project Status: Active Development

PDFML is currently under active development. Existing functionality is stable enough for creating structured PDF documents, while new language features and compiler improvements continue to be developed.

---

Developer

Creator: Ahmad Zaky Wildani

PDFML is an independent software project created to explore a modern and developer-friendly approach to PDF generation.

---

License

Copyright © 2026 PDFML. All rights reserved.

---

Vision

«"Our goal is to make PDF generation as simple as writing a document."»

PDFML is built for developers who want a dedicated language for creating structured PDF documents with a clean, expressive, and easy-to-learn syntax.
