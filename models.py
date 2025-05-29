from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
import uuid

db = SQLAlchemy()


class User(db.Model):
    id = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'User(id= {self.id}, username={self.username})'


# class Topic(db.Model):  # topics that would be commented upon
#     ...
#
#
#
# class Comments(db.Model):  # users comments on particular topics
#     ...
