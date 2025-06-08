from pydantic import Field, BaseModel, EmailStr, model_validator


class LoginForm(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    password: str = Field(min_length=8, max_length=24)
    
class RegisterForm(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: EmailStr = Field(max_length=50)
    password1: str = Field(min_length=8, max_length=24)
    password2: str = Field(min_length=8, max_length=24)
    
    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password1 != self.password2:
            raise ValueError("Passwords do not match")
        return self

class VerificationForm(BaseModel):
    verification_code: int = Field(lt=1000000, gt=99999)
    
    
    