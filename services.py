

from sqlalchemy.orm import Session

from models import Event, Registration
from schemas import EventCreate, EventUpdate, RegistrationCreate
def create_event(db: Session, event: EventCreate):
    
    new_event = Event(
        title=event.title,
        description=event.description,
        event_date=event.event_date,
        location=event.location,
        max_capacity=event.max_capacity
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event
def get_events(db: Session):
    
    return db.query(Event).all()
def get_event(db: Session, event_id: int):
    
    return db.query(Event).filter(Event.id == event_id).first()
def update_event(db: Session, event_id: int, event_data: EventUpdate):
    
    db_event = get_event(db, event_id)

    if db_event is None:
        return None

    update_data = event_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)

    return db_event
def delete_event(db: Session, event_id: int):
    
    db_event = get_event(db, event_id)

    if db_event is None:
        return None

    db.delete(db_event)
    db.commit()

    return True
def create_registration(db: Session, event_id: int, registration_data: RegistrationCreate):
    
    # Step 1: Check whether the event exists
    event = db.query(Event).filter(Event.id == event_id).first()

    if event is None:
        return "event_not_found"

    # Step 2: Check whether this employee has already registered
    existing_registration = db.query(Registration).filter(
        Registration.event_id == event_id,
        Registration.employee_email == registration_data.employee_email
    ).first()

    if existing_registration:
        return "duplicate"

    # Step 3: Count existing registrations for this event
    registration_count = db.query(Registration).filter(
        Registration.event_id == event_id
    ).count()

    # Step 4: Check whether the event is full
    if registration_count >= event.max_capacity:
        return "capacity_full"

    # Step 5: Create the new registration
    new_registration = Registration(
        event_id=event_id,
        employee_name=registration_data.employee_name,
        employee_email=registration_data.employee_email
    )

    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)

    return new_registration
def get_event_registrations(db: Session, event_id: int):
    
    # Check whether the event exists
    event = db.query(Event).filter(Event.id == event_id).first()

    if event is None:
        return None

    # Get all registrations belonging to this event
    registrations = db.query(Registration).filter(
        Registration.event_id == event_id
    ).all()

    return registrations
def delete_registration(db: Session, registration_id: int):
    
    # Find the registration
    registration = db.query(Registration).filter(
        Registration.id == registration_id
    ).first()

    # Check whether it exists
    if registration is None:
        return None

    # Delete the registration
    db.delete(registration)
    db.commit()

    return True