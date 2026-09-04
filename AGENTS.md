# Engineering guidelines

## Scope

This repository is a reusable small-dashboard starter. Keep it generic: product-specific
rules, names, vendors, and assumptions belong in replaceable modules, not shared code.

## Architecture

- Maintain a modular monolith. Each business module owns its domain, application layer,
  ports, and adapters. Modules communicate through explicit application interfaces.
- Follow hexagonal architecture. Domain and application code must not import FastAPI,
  SQLite, HTTP clients, environment readers, or other infrastructure frameworks.
- Dependencies point inward: adapters implement ports; the composition root wires objects.
- Prefer cohesive objects with one reason to change. Apply SOLID principles and dependency
  inversion; avoid global mutable state and service locators.
- Keep configuration at the outer boundary and parse environment variables with `envbind`.

## Code quality

- Write small, intention-revealing functions and precise names. Avoid hidden side effects,
  boolean traps, speculative abstractions, duplication, and comments that restate code.
- Use Python type hints everywhere and keep strict `mypy` and `ruff` checks passing.
- Model invalid states out of the domain where practical. Raise specific exceptions and
  translate them at boundaries.
- Keep React components focused, accessible, typed, and independent from transport details.
  Use the Carbon design system instead of one-off UI primitives.

## Security

- Treat all external input as untrusted. Validate it at boundaries and return minimal errors.
- Never commit secrets, tokens, real user data, or local databases. Never log credentials,
  authorization codes, cookies, or token bodies.
- Use OpenID Connect discovery, authorization-code flow, state/nonce protections, exact
  redirect URIs, short-lived signed sessions, secure cookie flags in deployed environments,
  and least-privilege scopes.
- Pin supported dependency ranges, keep lock files current, run as a non-root container user,
  and review dependency updates before merging.

## Tests and delivery

- Add unit tests for every behavior change. Prefer in-memory fakes and dependency injection.
- Tests must be deterministic, isolated, and runnable after clone with `make test`; they must
  not require network services, credentials, a pre-existing database, or files outside tests.
- Run `make quality` before merging. Keep the single-container contract and persistent
  `/data` SQLite volume intact.

