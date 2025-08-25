import asyncio
from datetime import datetime
import json
import pytest
from sqlalchemy import insert, delete, text

from app.database import Base, async_session_maker, engine
from app.config import settings

from app.users.models import Users
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings

from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from app.main import app as fastapi_app

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.drop_all(bind=sync_conn))
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(bind=sync_conn))

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)
        
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)
        await session.commit()


@pytest.fixture(scope="function")
async def ac():         #ac - AsyncClient
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="function")
async def authenticated_ac():        
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email":"test2@example.com",
            "password": "hashed_pass_2"
        })
        assert ac.cookies["booking_access_token"]
        yield ac


# @pytest.fixture(scope="function")
# async def async_session():
#     async with async_session_maker() as session:
#         yield session

# @pytest.fixture(autouse=True)
# async def clear_users_table(async_session):
#     await async_session.execute(text("DELETE FROM bookings"))
#     await async_session.execute(text("DELETE FROM users"))
#     await async_session.commit()

# def test_abv(ac):       #ac можем наследовать, чтобы не переписывать всегда (к примеру, ac.get()...)
#     async with AsyncClient(transport=transport, base_url="http://test") as ac:
#       ac.post(...)

# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()