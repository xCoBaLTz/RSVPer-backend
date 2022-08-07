import email_validator
import fastapi


def validate_email(email: str) -> str:
    try:
        valid_email = email_validator.validate_email(email=email)
        return valid_email.email
    except email_validator.EmailNotValidError:
        raise fastapi.HTTPException(
            status_code=400, detail="Please enter a valid email!"
        )
