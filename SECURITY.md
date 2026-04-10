# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within PSYCHE, please send an email to the maintainer. All security vulnerabilities will be promptly addressed.

**Please do NOT open a public GitHub issue for security vulnerabilities.**

## Security Best Practices Enforced

- **No secrets in code.** All API keys, tokens, and credentials are loaded from environment variables.
- **Input validation.** All API endpoints use Pydantic v2 validation.
- **Rate limiting.** Token bucket rate limiting on all API endpoints.
- **Bearer auth.** API key required for non-public endpoints.
- **Differential privacy.** Context Fusion Module applies DP noise to user signals.
- **Data isolation.** User listening data is never shared between users without explicit opt-in.
- **No PII in logs.** Structured logging strips user identifiable information.
- **Dependency scanning.** GitHub Dependabot enabled for all packages.
