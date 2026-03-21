from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from backend.crud.users import create_user, get_user_by_email
from backend.external_services.email import send_email_async
from backend.models.users import UserInDb
from backend.schemas.users import UserCreate, UserRead
from backend.crud.database import get_session

router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, session: Session = Depends(get_session)):
    try:
        user = get_user_by_email(session, user_in.email)
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user = create_user(session, user_in.email, user_in.password)
        
        # Send welcome email to user
        await send_email_async(
            subject="Welcome to Aero Bound Ventures! ✈️",
            recipients=[user_in.email],
            body_text="Thank you for registering with us. We're excited to have you on board!"
        )
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))