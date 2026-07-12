# Security Policy

## Supported Versions

The `main` branch is the supported development line.

## Reporting a Vulnerability

Please do not open public issues for secrets, authentication bypasses, data leaks, or access-control bugs.

Open a private security advisory on GitHub or contact the repository maintainer directly. Include:

- affected version or commit;
- steps to reproduce;
- expected impact;
- suggested mitigation, if known.

## Security Notes

- Passwords are hashed with `pbkdf2_sha256`.
- Sessions use signed HttpOnly cookies.
- `.env` is ignored by Git.
- External AI providers receive only the current interview question, expected points, answer, profession, level, and language.

