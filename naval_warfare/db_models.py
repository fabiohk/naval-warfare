from sqlalchemy import JSON
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()


class StandardMixin:
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)


class Game(StandardMixin, Base):
    __tablename__ = "games"

    settings_id = Column("settings_id", Integer, ForeignKey("game_settings.id"))

    settings = relationship("GameSettings", back_populates="games")
    boards = relationship("Board", back_populates="game")


class Player(StandardMixin, Base):
    __tablename__ = "players"

    name = Column("name", String(255), unique=True, index=True)

    boards = relationship("Board", back_populates="player")


class Board(StandardMixin, Base):
    __tablename__ = "boards"

    length = Column("length", Integer)
    width = Column("width", Integer)

    game_id = Column("game_id", Integer, ForeignKey("games.id"))
    player_id = Column("player_id", Integer, ForeignKey("players.id"))

    game = relationship(Game, back_populates="boards")
    player = relationship(Player, back_populates="boards")


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

    slug = Column("slug", String(255), unique=True)
    configuration = Column("configuration", JSON)

    games = relationship("Game", back_populates="settings")
