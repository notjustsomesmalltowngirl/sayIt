from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String

db = SQLAlchemy()


class Playground(db.Model):
    __tablename__ = 'playground'
    id = mapped_column(Integer, primary_key=True)
    type = mapped_column(String, nullable=False, )
    description = mapped_column(String, nullable=False)

    # def to_dict(self):
    #     return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class WouldYouRather(db.Model):
    __tablename__ = 'would_you_rather'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    question_one = mapped_column(String, nullable=False)
    question_two = mapped_column(String, nullable=False)


class NeverHaveIEver(db.Model):
    __tablename__ = 'never_have_i_ever'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    question = mapped_column(String, nullable=False)


class Riddle(db.Model):
    __tablename__ = 'riddle'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    question = mapped_column(String, nullable=False)
    answer = mapped_column(String, nullable=False)


class StoryBuilder(db.Model):
    __tablename__ = 'story_builder'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    starter = mapped_column(String, nullable=False)


class TwoTruthsAndALie(db.Model):
    __tablename__ = 'two_truths_and_a_lie'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)


class Hypotheticals(db.Model):
    __tablename__ = 'hypotheticals'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    scenario = mapped_column(String, nullable=False)


class HotTakes(db.Model):
    __tablename__ = 'hot_takes'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    opinion = mapped_column(String, nullable=False)


class DidYouKnow(db.Model):
    __tablename__ = 'did_you_know'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    fact = mapped_column(String, nullable=False)