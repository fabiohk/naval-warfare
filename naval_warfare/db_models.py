import databases
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class StandardMixin:
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)


class Game(StandardMixin, Base):
    __tablename__ = "games"

    settings_id = Column("settings_id", Integer, ForeignKey("game_settings.id"))
    settings = relationship("GameSettings", back_populates="games")

    players = relationship("Player", secondary="boards")


class Player(StandardMixin, Base):
    __tablename__ = "players"

    name = Column("name", String(255), unique=True, index=True)

    games = relationship("Game", secondary="boards")


class Board(StandardMixin, Base):
    __tablename__ = "boards"

    length = Column("length", Integer)
    width = Column("width", Integer)

    game_id = Column("game_id", Integer, ForeignKey("games.id"))
    player_id = Column("player_id", Integer, ForeignKey("players.id"))

    game = relationship(Game, backref=backref("boards"))
    player = relationship(Player, backref=backref("boards"))


class ShipPosition(StandardMixin, Base):
    __tablename__ = "ships_position"

    direction = Column("direction", String(255))
    cartesian_position = Column("cartesian_position", Integer)


class Ship(StandardMixin, Base):
    __tablename__ = "ships"

    kind = Column("kind", String(255), unique=True)
    length = Column("length", Integer)


class GameSettings(StandardMixin, Base):
    __tablename__ = "game_settings"

    games = relationship("Game", back_populates="settings")
