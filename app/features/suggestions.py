from app.db.database import SessionLocal
from app.db.models import User, Theme

async def handle_theme_submission(user_id: int, theme_value: str) -> str:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if not user:
            user = User(user_id=user_id, read_rules=True)
            session.add(user)
            session.commit()

        theme = Theme(user_id=user.user_id, theme=theme_value)
        session.add(theme)
        session.commit()

        return "Theme suggestion submitted!"
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        session.close()

async def list_all_suggestions() -> str:
    session = SessionLocal()
    try:
        themes = session.query(Theme).all()
        if not themes:
            return "No theme suggestions found."

        suggestions = "\n".join(
            [
                f"{theme.theme_id}: {theme.theme} (by user {theme.user_id} at {theme.suggestion_time})"
                for theme in themes
            ]
        )
        return f"Theme Suggestions:\n{suggestions}"
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        session.close()
