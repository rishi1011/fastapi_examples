import asyncio

import pytest

from app.operations import sell_ticket_to_user, get_ticket

@pytest.mark.asyncio
async def test_concurrent_ticket_sales(
        add_special_ticket,
        db_session_test,
        second_session_test,    
):
    result = await asyncio.gather(
        sell_ticket_to_user(db_session_test, 1234, "Jake Fake"),
        sell_ticket_to_user(second_session_test, 1234, "John Doe")
    )

    assert result in (
        [True, False],
        [False, True],
    )

    ticket = await get_ticket(db_session_test, 1234)

    if result[0]:
        assert ticket.user == "Jake Fake"
    else:
        assert ticket.user == "John Doe "