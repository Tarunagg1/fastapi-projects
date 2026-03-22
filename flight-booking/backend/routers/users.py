from backend.schemas.auth import UserInfo, Token

from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from backend.crud.users import create_user, get_user_by_email
from backend.external_services import email
from backend.external_services.email import send_email_async
from backend.models.users import UserInDb
from backend.schemas.users import UserCreate, UserRead
from backend.crud.database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import BackgroundTasks
from backend.utils.security import authenticate_user, create_access_token
from backend.utils.cookies import get_cookie_settings, get_cookie_domain
from backend.schemas.auth import GroupRead, PermissionRead

router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, session: Session = Depends(get_session)):
    try:
        user = get_user_by_email(session, user_in.email)
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user = create_user(session, user_in.email, user_in.password)

        # Send welcome email to user
        # await send_email_async(
        #     subject="Welcome to Aero Bound Ventures! ✈️",
        #     recipients=[user_in.email],
        #     body_text="Thank you for registering with us. We're excited to have you on board!"
        # )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/token", response_model=Token)
def login(response: Response,form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ], session: Session = Depends(get_session)) -> Token:
    try:
        user = authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.email})

        # Set HTTP-only cookie
        cookie_settings = get_cookie_settings()
        cookie_domain = get_cookie_domain()
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=cookie_settings["httponly"],
            secure=cookie_settings["secure"],
            samesite=cookie_settings["samesite"],
            max_age=cookie_settings["max_age"],
            domain=cookie_domain,
        )

        # Build user info with groups and permissions
        groups_with_permissions = [
            GroupRead(
                name=group.name,
                description=group.description,
                permissions=[
                    PermissionRead(
                        name=perm.name,
                        codename=perm.codename,
                        description=perm.description,
                    )
                    for perm in group.permissions
                ],
            )
            for group in user.groups
        ]

        user_info = UserInfo(
            id=user.id,
            email=user.email,
            groups=groups_with_permissions,
        )

        return Token(token_type="bearer", user=user_info)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

