import databases
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class StandardMixin(Base):
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)


class Game(StandardMixin):
    __tablename__ = "games"

    settings_id = Column("settings_id", Integer, ForeignKey("game_settings.id"))
    settings = relationship("GameSettings", back_populates="games")


class Player(StandardMixin):
    __tablename__ = "players"

    name = Column("name", String(255), unique=True, index=True)


class Ship(StandardMixin):
    __tablename__ = "ships"

    kind = Column("kind", String(255), unique=True)
    length = Column("length", Integer)


class GameSettings(StandardMixin):
    __tablename__ = "game_settings"

    games = relationship("Game", back_populates="settings")
