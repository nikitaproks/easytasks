from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from src.db.engine import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
