from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
import uuid

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = mapped_column(String, nullable=False, unique=True)
    is_admin = mapped_column(Boolean, default=False)
    remarks = relationship('Remark', back_populates='user')
    chats = relationship('Chat', back_populates='sender')

    def __repr__(self):
        return f'{self.__class__.__name__}(id= {self.id}, username={self.username})'


class Chat(db.Model):
    __tablename__ = 'chats'
    id = mapped_column(Integer, primary_key=True)
    text = mapped_column(String, nullable=False)
    sent_at = mapped_column(DateTime, default=datetime.utcnow)
    sender = relationship('User', back_populates='chats')
    sender_id = mapped_column(Integer, ForeignKey('users.id'))


class NewsItem(db.Model):  # topics that would be commented upon
    __tablename__ = 'newsitems'
    id = mapped_column(Integer, primary_key=True)
    type = mapped_column(String, nullable=False)
    headline = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=False)
    url = mapped_column(String, nullable=False)
    published_at = mapped_column(DateTime)
    created_at = mapped_column(DateTime, default=datetime.utcnow)

    remarks = relationship('Remark', back_populates='news_item', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f'{self.__class__.__name__}(id= {self.id}, type={self.type})'


class Remark(db.Model):
    __tablename__ = 'remarks'
    id = mapped_column(Integer, primary_key=True)
    content = mapped_column(String, nullable=False)
    user_id = mapped_column(String, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    user = relationship('User', back_populates='remarks')
    created_at = mapped_column(DateTime, default=datetime.utcnow)
    news_item_id = mapped_column(Integer, ForeignKey('newsitems.id', ondelete='CASCADE'))

    news_item = relationship('NewsItem', back_populates='remarks')

    def __repr__(self):
        return f'{self.__class__.__name__}(id= {self.id},)'
