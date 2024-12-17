from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
class Category(Base):
    __tablename__ = 'categories'  # Исправлено на __tablename__

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    cards: Mapped[list["Card"]] = relationship("Card", back_populates="category")

class Card(Base):
    __tablename__ = 'cards'  # Исправлено на __tablename__

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String(1000), nullable=False)
    answer: Mapped[str] = mapped_column(String(1000), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))  # Внешний ключ для категории
    set_id: Mapped[int] = mapped_column(ForeignKey('sets.id'))  # Внешний ключ для набора

    category: Mapped["Category"] = relationship("Category", back_populates="cards")
    set: Mapped["Set"] = relationship("Set", back_populates="cards")

class Set(Base):
    __tablename__ = 'sets'  # Исправлено на __tablename__

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    cards: Mapped[list["Card"]] = relationship("Card", back_populates="set")  # Исправлено на "set"