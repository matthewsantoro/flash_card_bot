import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.models import  Card, Category, Base, User, Set




class Database:
    def __init__(self, db_config):
        self.db_config = db_config
        self.engine = None
        self.SessionLocal = None

    async def connect(self):
        """Создает асинхронный движок и сессию."""
        DATABASE_URL = f"postgresql+asyncpg://{self.db_config['USER']}:{self.db_config['PASSWORD']}@{self.db_config['HOST']}:{self.db_config['PORT']}/{self.db_config['DATABASE']}"
        self.engine = create_async_engine(DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        logging.info("Подключение к базе данных успешно установлено.")

    async def close(self):
        """Закрывает соединение с базой данных."""
        await self.engine.dispose()
        logging.info("Соединения с базой данных закрыты.")

    async def setup(self):
        """Создает необходимые таблицы в базе данных, если они не существуют."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logging.info("Таблицы успешно созданы или уже существуют.")

    async def get_session(self):
        """Возвращает новую сессию для работы с базой данных."""
        async with self.SessionLocal() as session:
            yield session
    
    async def add_category(self, session: AsyncSession, name: str):
        new_category = Category(name=name)
        session.add(new_category)
        await session.commit()
        return new_category

    async def add_card(session: AsyncSession, question: str, answer: str, category_id: int):
        new_card = Card(question=question, answer=answer, category_id=category_id)
        session.add(new_card)
        await session.commit()
        return new_card
    
    async def add_user(session: AsyncSession, user_id: int, name: str ) -> User:
        new_user = User(name=name, id=user_id)
        session.add(new_user)
        await session.commit()
        return new_user
    
    async def user_exists(session: AsyncSession, user_id: int): 
        return session.query(User).filter(User.id == user_id).first() is not None
    
    async def add_set(session: AsyncSession, name: str, creator: User, private: bool = True ) -> Set:
        new_set = Set(name=name, creator_id=creator, private=private)
        session.add(new_set)
        await session.commit()
        return new_set
   