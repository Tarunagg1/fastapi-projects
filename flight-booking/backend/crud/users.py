
from sqlmodel import Session, select
from backend.models.users import UserInDb
from backend.utils.security import hash_password



def get_user_by_email(session: Session, email: str) -> UserInDb:
    # This is a placeholder function. In a real application, you would query the database.
    return session.exec(select(UserInDb).where(UserInDb.email == email)).first()


def create_user(session: Session, email: str,password: str) -> UserInDb:
    # This is a placeholder function. In a real application, you would hash the password and save the user to the database.
    hashed_password = hash_password(password)
    user = UserInDb(email=email, password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
