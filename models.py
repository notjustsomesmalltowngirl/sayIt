from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Boolean
import uuid

db = SQLAlchemy()


class User(db.Model):
    id = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = mapped_column(String, nullable=False, unique=True)
    is_admin = mapped_column(Boolean, default=False)

    # TODO: will add an is_admin attr here for happi and me
    def __repr__(self):
        return f'User(id= {self.id}, username={self.username})'

#
# class Topic(db.Model):  # topics that would be commented upon
#     id = mapped_column(primary_key=True)
#     type = mapped_column(String, nullable=False)
#     headline = mapped_column(String, nullable=False)
#
#
#
# class Comments(db.Model):  # users comments on particular topics
#     ...
