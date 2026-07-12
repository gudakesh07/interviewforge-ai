# Database

SQLite is used by default through `DATABASE_URL=sqlite:///./interviewforge.db`.
PostgreSQL can be used with a SQLAlchemy URL such as `postgresql+psycopg://user:password@host:5432/db`.

Run migrations:

```bash
alembic upgrade head
```

