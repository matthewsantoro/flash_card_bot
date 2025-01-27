from datetime import datetime, timedelta
import logging
from os import getenv
from sqlalchemy import Update, delete, func, select, text

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from models.models import Card, Base, User, Deck, Transitions, Level


class Database:
    def __init__(self):
        self.db_host = getenv("DB_HOST")
        self.db_user = getenv("DB_USER")
        self.db_password = getenv("DB_PASSWORD")
        self.db_port = getenv("DB_PORT")
        self.db_database = getenv("DB_DATABASE")
        self.connect = f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}"
        self.async_engine = create_async_engine(self.connect, echo=True)
        self.Session = async_sessionmaker(bind=self.async_engine, class_=AsyncSession)

    async def close(self):
        """Закрывает соединение с базой данных."""
        await self.engine.dispose()
        logging.info("Соединения с базой данных закрыты.")

    async def setup(self):
        """Создает необходимые таблицы в базе данных, если они не существуют."""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(
                text(
                    """
            CREATE OR REPLACE FUNCTION update_card_numbers()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Обновляем номера карточек для всех записей с тем же set_id
                UPDATE cards
                SET number = new_numbers.new_number
                FROM (
                    SELECT id, ROW_NUMBER() OVER (PARTITION BY deck_id ORDER BY id) AS new_number
                    FROM cards
                    WHERE deck_id = OLD.deck_id
                ) AS new_numbers
                WHERE cards.id = new_numbers.id;

                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        """
                )
            )

            await conn.execute(
                text(
                    """
                DROP TRIGGER IF EXISTS update_card_numbers_trigger ON cards;
                """
                )
            )

            await conn.execute(
                text(
                    """
                CREATE TRIGGER update_card_numbers_trigger
                AFTER DELETE ON cards
                FOR EACH ROW
                EXECUTE FUNCTION update_card_numbers();
        """
                )
            )
            logging.info("Таблицы успешно созданы или уже существуют.")

    # CARDS
    async def add_card(self, question: str, answer: str, deck_id: int, number: int):
        async with self.Session() as session:

            new_card = Card(
                question=question, answer=answer, deck_id=deck_id, number=number
            )
            session.add(new_card)
            await session.commit()
            await session.refresh(new_card)
            return new_card

    async def get_last_card_number_in_deck(self, deck_id: int):
        async with self.Session() as session:
            result = await session.execute(
                select(func.count()).select_from(Card).where(Card.deck_id == deck_id)
            )
            return result.scalar()

    async def delete_card(self, card_id: int):
        async with self.Session() as session:
            await session.execute(delete(Card).where(Card.id == card_id))
            await session.commit()

    async def get_cards_by_deck_id(self, deck_id: int):
        async with self.Session() as session:
            result = await session.execute(
                select(Card).where(Card.deck_id == deck_id).order_by(Card.number)
            )
            return result.scalars().all()

    async def edit_front_card_by_card_id(self, card_id: int, front: str):
        async with self.Session() as session:
            await session.execute(
                Update(Card).where(Card.id == card_id).values(question=front)
            )
            await session.commit()

            result = await session.execute(select(Card).where(Card.id == card_id))
            return result.scalar_one_or_none()

    async def edit_front_card_by_card_id(self, card_id: int, front: str):
        async with self.Session() as session:
            await session.execute(
                Update(Card).where(Card.id == card_id).values(question=front)
            )
            await session.commit()

            result = await session.execute(select(Card).where(Card.id == card_id))
            return result.scalar_one_or_none()

    async def update_card(self, card: Card):
        async with self.Session() as session:
            await session.merge(card)
            await session.commit()

    async def get_study_cards_by_deck_id(self, deck_id: int):
        async with self.Session() as session:
            result = await session.execute(
                select(Card).where(
                    (Card.deck_id == deck_id) & (Card.last_reviewed <= func.now())
                )
            )
            return result.scalars().all()

    async def update_level_card(self, action_successful: bool, card_id: int):
        async with self.Session() as session:
            card_result = await session.execute(select(Card).where(Card.id == card_id))
            print("mamba222")
            card = card_result.scalar_one()
            print("mamba333")
            transition_result = await session.execute(
                select(Transitions).where(
                    (Transitions.current_level_id == card.level_id)
                    & (Transitions.action_successful == action_successful)
                )
            )
            transition = transition_result.scalar_one()

            card.level_id = transition.next_level_id

            next_level = (
                await session.execute(
                    select(Level).where(
                        (Level.level_id == transition.next_level_id)
                    )
                )
            ).scalar_one()

            card.last_reviewed = datetime.now() + timedelta(
                days=next_level.interval_days
            )

            await session.commit()

    async def get_next_time_to_learn(self):
        async with self.Session() as session:
            time_result = await session.execute(select(func.min(Card.last_reviewed)))
            
            return time_result.scalar() 
    # USER
    async def add_user(self, user_id: int, name: str) -> User:
        async with self.Session() as session:
            new_user = User(name=name, id=user_id)
            session.add(new_user)
            await session.commit()

    async def get_user_by_id(self, user_id: int) -> User:
        async with self.Session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalars().first()

    # DECK
    async def get_decks_by_user_id(self, user_id: int) -> list[Deck]:
        async with self.Session() as session:
            result = await session.execute(
                select(Deck).where(Deck.creator_id == user_id)
            )
            return result.scalars().all()

    async def get_deck_by_id(self, deck_id: int) -> list[Deck]:
        async with self.Session() as session:
            result = await session.execute(select(Deck).where(Deck.id == deck_id))
            return result.scalars().first()

    async def add_deck(self, name: str, creator_id: int, private: bool = True) -> Deck:
        async with self.Session() as session:
            new_deck = Deck(name=name, creator_id=creator_id, private=private)
            session.add(new_deck)
            await session.commit()
            await session.refresh(new_deck)
            return new_deck

    async def edit_deck_name(self, deck_id: int, name: str):
        async with self.Session() as session:
            await session.execute(
                Update(Deck).where(Deck.id == deck_id).values(name=name)
            )
            await session.commit()

    async def delete_deck_by_id(self, deck_id: int):
        async with self.Session() as session:
            await session.execute(delete(Card).where(Card.deck_id == deck_id))
            await session.execute(delete(Deck).where(Deck.id == deck_id))
            await session.commit()

    async def update_deck(self, deck: Deck):
        async with self.Session() as session:
            await session.merge(deck)
            await session.commit()

    #LEVEL
    async def get_level_by_id(self, level_id: int):
        async with self.Session() as session:
            result = await session.execute(select(Level).where(Level.level_id == level_id))
            return result.scalars().first()
            

    # TRANSITIONS

    # async def get_transitions_by_current_level_id(self, deck_id: int) -> list[Deck]:
    #     async with self.Session() as session:
    #         result = await session.execute(select(Deck).where(Deck.id == deck_id))
    #         return result.scalars().first()
