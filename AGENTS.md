# Development Guidelines

- Write or update unit tests for every behavioral change and bug fix. Keep tests focused, deterministic, and fast, and run the relevant tests with `uv run pytest` before handing off changes.
- Use Ruff for Python linting and formatting. Run `uv run ruff check` and `uv run ruff format --check` on all Python files you change, and resolve any issues those commands report.
