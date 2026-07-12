import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal, create_database
from app.repositories.user_repository import create_user, get_user_by_email


def main() -> None:
    create_database()
    with SessionLocal() as db:
        if get_user_by_email(db, "demo@example.com") is None:
            create_user(db, "demo", "demo@example.com", "demo-password")
        print("Demo user: demo@example.com / demo-password")


if __name__ == "__main__":
    main()
