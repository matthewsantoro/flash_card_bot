from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    func,
    BOOLEAN,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=True)
    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"))
    Level_id: Mapped[int] = mapped_column(ForeignKey("levels.level_id"), default=1)

    deck: Mapped["Deck"] = relationship("Deck", back_populates="card")
    level: Mapped["Level"] = relationship("Level", back_populates="card")


class Deck(Base):
    __tablename__ = "decks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=False, nullable=False)
    private: Mapped[bool] = mapped_column(BOOLEAN, default=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    card: Mapped[list["Card"]] = relationship("Card", back_populates="deck")
    creator: Mapped["User"] = relationship("User", back_populates="deck")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=False, nullable=False)

    deck: Mapped["Deck"] = relationship("Deck", back_populates="creator")


class Transitions(Base):
    __tablename__ = "transitions"
    transition_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    current_level_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("levels.level_id"), nullable=False
    )
    action_successful: Mapped[bool] = mapped_column(Boolean, nullable=False)
    next_level_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("levels.level_id"), nullable=False
    )

    current_level = relationship(
        "Level", foreign_keys=[current_level_id], back_populates="current_transitions"
    )
    next_level = relationship(
        "Level", foreign_keys=[next_level_id], back_populates="next_transitions"
    )


class Level(Base):
    __tablename__ = "levels"
    level_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    interval_days: Mapped[int] = mapped_column(Integer, nullable=False)

    card: Mapped[list["Card"]] = relationship("Card", back_populates="level")
    current_transitions = relationship(
        "Transitions",
        foreign_keys=[Transitions.current_level_id],
        back_populates="current_level",
    )
    next_transitions = relationship(
        "Transitions",
        foreign_keys=[Transitions.next_level_id],
        back_populates="next_level",
    )
