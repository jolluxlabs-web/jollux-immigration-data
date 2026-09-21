# Security Policy

## Reporting

Please report suspected vulnerabilities privately through GitHub Security Advisories after the repository is published. Until then, contact the repository owner directly and do not open a public issue containing sensitive details.

## Data safety

This project does not require credentials or network access. Never add database URLs, API keys, analytics identifiers, environment files, production exports, or private application code.

Treat input workbooks as untrusted. Process them in a constrained environment when their origin is uncertain. The parser does not execute macros or formulas, but spreadsheet and archive files can still consume substantial resources.

Supported security fixes target the latest released minor version.
