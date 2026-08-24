from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.auth_utils import hash_password, verify_password, create_access_token
from app.config import settings
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # 1. Validate college email domain
    email_domain = user_data.email.split("@")[-1].lower()

    if email_domain != settings.COLLEGE_EMAIL_DOMAIN.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only college email addresses are allowed"
        )

    # 2. Check whether email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # 3. Hash the password
    password_hash = hash_password(user_data.password)

    # 4. Create the user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=password_hash,
        role=UserRole.STUDENT,
        hostel_block=user_data.hostel_block
    )

    # 5. Save the user to PostgreSQL
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 6. Return the newly created user
    return new_user


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    # 1. Find user by email
    user = db.query(User).filter(User.email == user_data.email).first()

    # 2. Verify password
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Build token payload
    role_value = getattr(user.role, "value", user.role)

    access_token = create_access_token({
        "sub": str(user.id),
        "role": role_value,
    })

    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(current_user: User = Depends(get_current_user)):
    return current_user