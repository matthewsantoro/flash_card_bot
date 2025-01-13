import logging
from os import getenv
from sqlalchemy import delete, func, select, text

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from models.models import Card, Base, User, Set


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
                    SELECT id, ROW_NUMBER() OVER (PARTITION BY set_id ORDER BY id) AS new_number
                    FROM cards
                    WHERE set_id = OLD.set_id
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
    async def add_card(self, question: str, answer: str, set_id: int, number: int):
        async with self.Session() as session:

            new_card = Card(
                question=question, answer=answer, set_id=set_id, number=number
            )
            session.add(new_card)
            await session.commit()
            await session.refresh(new_card)
            return new_card

    async def get_last_card_number_in_set(self, set_id: int):
        async with self.Session() as session:
            result = await session.execute(
                select(func.count()).select_from(Card).where(Card.set_id == set_id)
            )
            return result.scalar()

    async def delete_card(self, card_id: int):
        async with self.Session() as session:
            await session.execute(delete(Card).where(Card.id == card_id))
            await session.commit()

    async def get_cards_by_set_id(self, set_id: int):
        async with self.Session() as session:
            result = await session.execute(select(Card).where(Card.set_id == set_id))
            return result.scalars().all()

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

    # SETS
    async def get_sets_by_user_id(self, user_id: int) -> list[Set]:
        async with self.Session() as session:
            result = await session.execute(select(Set).where(Set.creator_id == user_id))
            return result.scalars().all()

    async def get_set_by_id(self, set_id: int) -> list[Set]:
        async with self.Session() as session:
            result = await session.execute(select(Set).where(Set.id == set_id))
            return result.scalars().firt()

    async def add_set(self, name: str, creator_id: int, private: bool = True) -> Set:
        async with self.Session() as session:
            new_set = Set(name=name, creator_id=creator_id, private=private)
            session.add(new_set)
            await session.commit()
            await session.refresh(new_set)
            return new_set
