from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import Ticket, TicketCreate, TicketUpdate
from app.crud import create_ticket, get_tickets, get_ticket, update_ticket

router = APIRouter(
    prefix="/api/tickets",
    tags=["tickets"]
)

# Create ticket
@router.post("", response_model=Ticket, status_code=201)
def create_ticket_endpoint(ticket: TicketCreate, db: Session = Depends(get_db)):
    return create_ticket(db=db, ticket_data=ticket)

# List tickets
@router.get("", response_model=List[Ticket])
def list_tickets_endpoint(
    search: Optional[str] = Query(None, description="Search by ticket ID, customer name, or subject"),
    status: Optional[str] = Query(None, description="Filter by ticket status (Open, In Progress, Closed, or All)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    tickets = get_tickets(db=db, skip=skip, limit=limit, search=search, status=status)
    return tickets

# Get single ticket
@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket_endpoint(ticket_id: str, db: Session = Depends(get_db)):
    db_ticket = get_ticket(db=db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

# Update ticket
@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket_endpoint(ticket_id: str, ticket_update: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = update_ticket(db=db, ticket_id=ticket_id, update_data=ticket_update)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket
