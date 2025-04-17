from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from facilibras.config.db import get_db_session

T_Session = Annotated[Session, Depends(get_db_session)]
