---
applyTo: "docs/**/*.md"
---
# Project documentation writing guidelines

## General Guidelines
- Write clear and concise documentation.
- Use consistent terminology and style.
- Include code examples where applicable.

## Grammar
* Use present tense verbs (is, open) instead of past tense (was, opened).
* Write factual statements and direct commands. Avoid hypotheticals like "could" or "would".
* Use active voice where the subject performs the action.
* Write in second person (you) to speak directly to readers.

## Code Examples
- **Always use Polars** for data processing code examples (NOT pandas unless explicitly necessary)
- **Always use `uv`** for package management commands (NOT pip or conda)
- Example code snippets should reflect the project's technology stack:
  ```python
  # Data loading with Polars
  import polars as pl
  df = pl.read_csv("data/1_raw/disease_data.csv")
  ```
  ```bash
  # Package installation with uv
  uv pip install polars
  ```

## Markdown Guidelines
- Use headings to organize content.
- Use bullet points for lists.
- Include links to related resources.
- Use code blocks for code snippets.

