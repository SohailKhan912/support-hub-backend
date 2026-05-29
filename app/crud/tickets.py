import logging
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional
from app.models import Ticket, Note
from app.schemas import TicketCreate, TicketUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper to generate ticket ID like TCK-1001
def generate_ticket_id(db: Session) -> str:
    # Find the max ticket ID numeric part
    last_ticket = db.query(Ticket).order_by(Ticket.id.desc()).first()
    if last_ticket:
        # Extract number from ticket_id (e.g., TCK-1001 → 1001)
        last_num = int(last_ticket.ticket_id.split("-")[1])
        new_num = last_num + 1
    else:
        new_num = 1001
    return f"TCK-{new_num}"

# Create new ticket
def create_ticket(db: Session, ticket_data: TicketCreate) -> Ticket:
    ticket_id = generate_ticket_id(db)
    db_ticket = Ticket(
        ticket_id=ticket_id,
        customer_name=ticket_data.customer_name,
        customer_email=ticket_data.customer_email,
        subject=ticket_data.subject,
        description=ticket_data.description,
        status="Open"
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    # Return ticket with notes relationship loaded
    return get_ticket(db, ticket_id)

# Get all tickets, with optional search and status filter
def get_tickets(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    status: Optional[str] = None
) -> List[Ticket]:
    query = db.query(Ticket).options(joinedload(Ticket.notes))
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                Ticket.ticket_id.ilike(search_term),
                Ticket.customer_name.ilike(search_term),
                Ticket.subject.ilike(search_term)
            )
        )
    if status and status != "All":
        query = query.filter(Ticket.status == status)
    # Order by created_at descending
    query = query.order_by(Ticket.created_at.desc())
    return query.offset(skip).limit(limit).all()

# Get single ticket by ticket_id
def get_ticket(db: Session, ticket_id: str) -> Optional[Ticket]:
    return db.query(Ticket).options(joinedload(Ticket.notes)).filter(Ticket.ticket_id == ticket_id).first()

# Update ticket (status and/or add note)
def update_ticket(db: Session, ticket_id: str, update_data: TicketUpdate) -> Optional[Ticket]:
    logger.info(f"CRUD: update_ticket called for ticket_id={ticket_id}")
    logger.info(f"CRUD: update_data.new_note = {repr(update_data.new_note)}")
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        return None
    # Update status if provided
    if update_data.status:
        db_ticket.status = update_data.status
    # Add note if provided
    if update_data.new_note and update_data.new_note.strip():
        logger.info(f"CRUD: Creating note = {update_data.new_note.strip()}")
        db_note = Note(
            ticket_id=ticket_id,
            note_text=update_data.new_note.strip()
        )
        db.add(db_note)
        db_ticket.notes.append(db_note)  # Add note to in-memory relationship
    db.commit()
    # Expire the ticket to force reloading from database
    db.expire(db_ticket)
    # Reload ticket with updated notes relationship
    updated_ticket = get_ticket(db, ticket_id)
    logger.info(f"CRUD: Updated ticket has {len(updated_ticket.notes)} notes")
    return updated_ticket
