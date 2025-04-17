from typing import Annotated

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)

T_OAuth2 = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]
T_Token = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
