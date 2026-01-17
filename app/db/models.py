from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, DateTime
from sqlalchemy.sql import func


metadata_obj = MetaData()


users = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("email", String),
    Column("password", String),
    Column("bio", String),
    Column("profile_pic", String)
)


users_on_verification = Table(
    "users_on_verification",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("email", String),
    Column("password", String),
    Column("token", String),
    Column("verification_code", Integer),
    Column("created_at", DateTime, server_default=func.now()),
)

recovery = Table(
    "recovery",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("token", String),
    Column("created_at", DateTime, server_default=func.now()),
)