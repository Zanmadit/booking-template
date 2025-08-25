import pytest
from httpx import AsyncClient

@pytest.mark.parametrize("user_id,booking_id,status_code", [
    (2, 2, 200),
    (2, 3, 200),
    (2, 1, 409),
])
async def test_delete_and_get_booking(user_id, booking_id, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.delete(f"/bookings/{booking_id}", params={
        "user_id": user_id,
        "booking_id": booking_id
    })
    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")
    assert response.status_code == 200
