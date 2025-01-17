from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, func,BOOLEAN
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
# class Category(Base):
#     __tablename__ = 'categories'  
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

#     cards: Mapped[list["Card"]] = relationship("Card", back_populates="category")

class Card(Base):
    __tablename__ = 'cards'  

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String(1000), nullable=False)
    answer: Mapped[str] = mapped_column(String(1000), nullable=False)
   
    deck_id: Mapped[int] = mapped_column(ForeignKey('decks.id')) 
    number: Mapped[int] = mapped_column(Integer, nullable=True)

    deck: Mapped["Deck"] = relationship("Deck", back_populates="card")

class Deck(Base):
    __tablename__ = 'decks' 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=False, nullable=False)
    private: Mapped[bool] = mapped_column(BOOLEAN, default=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id')) 

    card: Mapped[list["Card"]] = relationship("Card", back_populates="deck")  
    creator: Mapped["User"] = relationship("User", back_populates="deck")

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=False, nullable=False)

    deck: Mapped["Deck"] = relationship("Deck", back_populates="creator")
