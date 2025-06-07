from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String

db = SQLAlchemy()


class Playground(db.Model):
    __tablename__ = 'playground'
    id = mapped_column(Integer, primary_key=True)
    type = mapped_column(String, nullable=False, unique=True)
    did_you_knows = db.relationship('DidYouKnow', backref='playground', lazy=True)
    hypotheticals = db.relationship('Hypotheticals', backref='playground', lazy=True)
    hot_takes = db.relationship('HotTakes', backref='playground', lazy=True)
    never_have_i_evers = db.relationship('NeverHaveIEver', backref='playground', lazy=True)
    would_you_rather_questions = db.relationship('WouldYouRather', backref='playground', lazy=True)
    story_builders = db.relationship('StoryBuilder', backref='playground', lazy=True)
    riddles = db.relationship('Riddle', backref='playground', lazy=True)
    two_truths_and_a_lie = db.relationship('TwoTruthsAndALie', backref='playground', lazy=True)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.type}>'
    # def to_dict(self):
    #     return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class WouldYouRather(db.Model):
    __tablename__ = 'would_you_rather'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    scenario = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'


class NeverHaveIEver(db.Model):
    __tablename__ = 'never_have_i_ever'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    question = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

class Riddle(db.Model):
    __tablename__ = 'riddle'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    question = mapped_column(String, nullable=False, unique=True)
    answer = mapped_column(String, nullable=False)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
class StoryBuilder(db.Model):
    __tablename__ = 'story_builder'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    starter = mapped_column(String, nullable=False, unique=True)
    difficulty = mapped_column(String, nullable=False, default='easy')
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

# class Statement:  # model for each two truths and a lie statement
#     def __init__(self, statement: str, is_true: bool):
#         self.statement = statement
#         self.is_true = is_true


class TwoTruthsAndALie(db.Model):
    __tablename__ = 'two_truths_and_a_lie'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    true_statement_1 = mapped_column(String, nullable=False, unique=True)
    true_statement_2 = mapped_column(String, nullable=False, unique=True)
    false_statement = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))

    __table_args__ = (
        db.UniqueConstraint('true_statement_1', 'true_statement_2', 'false_statement', name='unique_statements_combo'),
    )
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'


class Hypotheticals(db.Model):
    __tablename__ = 'hypotheticals'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    scenario = mapped_column(String, nullable=False , unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'


class HotTakes(db.Model):
    __tablename__ = 'hot_takes'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    opinion = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'


class DidYouKnow(db.Model):
    __tablename__ = 'did_you_know'
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)
    fact = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
