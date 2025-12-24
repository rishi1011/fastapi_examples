from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base
from app.db_connection import (
    AsyncSessionLocal,
    get_db_session,
    get_engine,
    enable_wal,
)
from app.operations import create_ticket, get_ticket, update_ticket_price, delete_ticket, create_event, update_ticket_details


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()

    await enable_wal()
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


class TicketRequest(BaseModel):
    price: float | None
    show: str | None
    user: str | None = None


@app.post("/ticket", response_model=dict[str, int])
async def create_ticket_route(
    ticket: TicketRequest,
    db_session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
):
    ticket_id = await create_ticket(
        db_session,
        ticket.show,
        ticket.user,
        ticket.price,
    )
    return {"ticket_id": ticket_id}


@app.get("/ticket/{ticket_id}")
async def read_ticket(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    ticket_id: int,
):
    ticket = await get_ticket(db_session, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


class TicketDetailsUpdateRequest(BaseModel):
    seat: str | None = None
    ticket_type: str | None = None


class TicketUpdateRequest(BaseModel):
    price: float | None = Field(None, ge=0)


@app.put("/ticket/{ticket_id}")
async def update_ticket_details_route(
    ticket_id: int,
    ticket_update: TicketDetailsUpdateRequest,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    update_dict_args = ticket_update.model_dump(exclude_unset=True)

    print("BEFORE update_ticket_details")
    updated = await update_ticket_details(db_session, ticket_id, update_dict_args)
    print("AFTER update_ticket_details")

    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return {"detail": "Details updated."}


@app.put("/ticket/{ticket_id}/price/{new_price}")
async def update_ticket_price_route(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    ticket_id: int,
    new_price: float,
):
    updated = await update_ticket_price(db_session, ticket_id, new_price)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"detail": "Price updated"}


@app.delete("/ticket/{ticket_id}")
async def delete_ticket_route(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    ticket_id: int,
):
    ticket = await delete_ticket(db_session, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"detail": "Ticket removed"}


class TicketResponse(TicketRequest):
    id: int


@app.post("/event", response_model=dict[str, int])
async def create_event_route(
    db_session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    event_name: str,
    nb_tickets: int | None = 0,
):
    event_id = await create_event(db_session, event_name, nb_tickets)
    return {"event_id": event_id}
