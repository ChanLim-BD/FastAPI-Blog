import os

from sqlalchemy import create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from typing import AsyncGenerator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from fastapi import status
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv



# database connection URL
load_dotenv()
DATABASE_CONN = os.getenv("DATABASE_CONN")

"""동기 방식"""
# engine = create_engine(DATABASE_CONN, #echo=True,
                    #    poolclass=QueuePool,
                    #    poolclass=NullPool, # Connection Pool 사용하지 않음. 
                    #    pool_size=10, max_overflow=0,
                    #    pool_recycle=300)

"""비동기 방식"""
engine: AsyncEngine = create_async_engine(DATABASE_CONN, #echo=True,
                    #   poolclass=QueuePool,
                    #   poolclass=NullPool, # Connection Pool 사용하지 않음. 
                       pool_size=10, max_overflow=0,
                       pool_recycle=300)

async def direct_get_conn():
    conn = None
    try:
        conn = await engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    

async def context_get_conn():
    conn = None
    try:
        conn = await engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    finally:
        if conn:
            await conn.close()




# 엔진 생성
engine_orm = create_async_engine(DATABASE_CONN, echo=True)

# 세션 로컬 생성
AsyncSessionLocal = sessionmaker(
    engine_orm,
    expire_on_commit=False,
    class_=AsyncSession
)
# 모델의 기본 클래스 생성
Base = declarative_base()

# 데이터베이스 세션을 얻기 위한 의존성
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session