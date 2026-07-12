# Security

- Passwords are hashed with Passlib bcrypt.
- Sessions use signed HttpOnly cookies with SameSite=Lax.
- `.env` is ignored by Git.
- User input is escaped by Jinja2 templates.
- Interview access is checked by owner before report or answer access.
- API keys are not logged.

