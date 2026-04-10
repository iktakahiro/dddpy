# Coding Rules

## 1. Communication & Style

- Write code comments, commit messages, and pull request titles and summaries in English.
- Use docstrings and documentation in English; follow the rules in Section 3.

## 2. Workflow & Commits

- Separate development tasks from commit tasks unless otherwise instructed.
- Execute commits only after receiving explicit instructions from the developer.
- Use the Conventional Commits format for git commit messages.
  - Reference: <https://www.conventionalcommits.org/en/v1.0.0/>
  - Format:

    ```text
    <type>[optional scope]: <description>

    [optional body]
    ```

  - Types: `fix`, `feat`, `chore`, `doc`, `refactor`, `test`
  - Add a scope when relevant, e.g., `fix(admin): ...`
- Split commits by scope if multiple files change; keep unrelated changes (e.g., README vs features) in separate commits.
- Always run `make format` and `make test` before creating a commit to keep CI green.

## 3. Documentation Comments

- Write docstrings in English, comply with PEP 257, and follow the Google Python Style Guide.
- Keep wording concise; include only information that adds clarity.
- Start with a one-line summary in the imperative mood; keep it under 72 characters when reasonable.
- Insert a blank line after the summary when adding sections such as `Args`, `Returns`, `Raises`.
- Use triple double quotes and indent continuation lines with four spaces.
- Document parameters in an `Args:` section only when they exist, matching parameter names and noting defaults when helpful.
- Describe return values in a `Returns:` section (or `Yields:` for generators) with types in parentheses.
- List possible exceptions in a `Raises:` section when the function intentionally raises them.
- Provide an `Examples:` section using doctest-style snippets if it clarifies usage.
- Class docstrings should summarize the responsibility of the class and include an `Attributes:` section when necessary.
- Module docstrings belong at the top of the file, summarizing purpose and important side effects or constants.
- Use the following templates as references.

```python
def calculate_discount(price: float, rate: float) -> float:
    """Calculate discounted price.

    Args:
        price (float): Original price.
        rate (float): Discount rate as a decimal (e.g., 0.2 for 20%).

    Returns:
        float: Discounted price after applying the rate.

    Raises:
        ValueError: If price or rate is negative.

    Example:
        >>> calculate_discount(100, 0.1)
        90.0
    """
```

```python
class UserClient:
    """Client for interacting with the User API.

    This client handles authentication and common API endpoints.
    """
```

```python
"""user_client.py

This module provides a simple client for accessing user data via API.
"""
```

## 4. Project Overview

- Onion Architecture around a todo domain with FastAPI presenting HTTP endpoints.
- Tech stack: FastAPI, SQLAlchemy + SQLite, uv for dependency management, Docker devcontainer.
- Key directories:
  - `dddpy/domain`: Entities, value objects, repository interfaces, domain exceptions.
  - `dddpy/usecase`: Application services implementing todo use cases.
  - `dddpy/infrastructure`: Dependency injection wiring and SQLite repositories.
  - `dddpy/presentation`: FastAPI handlers, schemas, error messages.
  - `tests`: Pytest suites across layers.

## 5. Development Workflow

- Install dependencies with `make install`.
- Run the application locally with `make dev`; docs are served at `http://127.0.0.1:8000/docs`.
- Leverage the `.devcontainer` configuration when using VSCode Remote-Container.
- Consult REST samples in `README.md` for manual endpoint testing.

## 6. Testing & Quality Gates

- Run `make test` to execute Pytest.
- Keep Pyrefly and ruff clean for type checking and linting/formatting.
- Maintain Onion Architecture boundaries when modifying or adding features.
