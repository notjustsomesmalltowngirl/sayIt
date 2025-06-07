from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String

db = SQLAlchemy()


class MasterClass(db.Model):
    __abstract__ = True
    id = mapped_column(Integer, primary_key=True)

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name != 'playground_id'
        }

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'


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


class WouldYouRather(MasterClass):
    __tablename__ = 'would_you_rather'
    category = mapped_column(String, nullable=False)
    scenario = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class NeverHaveIEver(MasterClass):
    __tablename__ = 'never_have_i_ever'
    category = mapped_column(String, nullable=False)
    question = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class Riddle(MasterClass):
    __tablename__ = 'riddle'
    category = mapped_column(String, nullable=False)
    question = mapped_column(String, nullable=False, unique=True)
    answer = mapped_column(String, nullable=False)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class StoryBuilder(MasterClass):
    __tablename__ = 'story_builder'
    category = mapped_column(String, nullable=False)
    starter = mapped_column(String, nullable=False, unique=True)
    difficulty = mapped_column(String, nullable=False, default='easy')
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class TwoTruthsAndALie(MasterClass):
    __tablename__ = 'two_truths_and_a_lie'
    category = mapped_column(String, nullable=False)
    true_statement_1 = mapped_column(String, nullable=False, unique=True)
    true_statement_2 = mapped_column(String, nullable=False, unique=True)
    false_statement = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))

    __table_args__ = (
        db.UniqueConstraint('true_statement_1', 'true_statement_2', 'false_statement', name='unique_statements_combo'),
    )


class Hypotheticals(MasterClass):
    __tablename__ = 'hypotheticals'
    category = mapped_column(String, nullable=False)
    scenario = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class HotTakes(MasterClass):
    __tablename__ = 'hot_takes'
    category = mapped_column(String, nullable=False)
    opinion = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class DidYouKnow(MasterClass):
    __tablename__ = 'did_you_know'
    category = mapped_column(String, nullable=False)
    fact = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))
