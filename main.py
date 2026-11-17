#from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
import services
#from fastapi import FastAPI, Depends, HTTPException, status
from db import engine, get_db
from fastapi import FastAPI, Depends, HTTPException, status, Response
app = FastAPI(
    title="Corporate Event Management API",
    description="API for managing corporate events and employee registrations.",
    version="1.0.0"
)
@app.post("/events", response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db)
):
    return services.create_event(db=db, event=event)
@app.get("/events", response_model=list[schemas.EventResponse])
def read_events(db: Session = Depends(get_db)):
    return services.get_events(db=db)
@app.get("/events/{event_id}", response_model=schemas.EventResponse)
def read_event(event_id: int, db: Session = Depends(get_db)):

    event = services.get_event(db=db, event_id=event_id)

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return event

@app.put("/events/{event_id}", response_model=schemas.EventResponse)
def update_event(
    event_id: int,
    event_data: schemas.EventUpdate,
    db: Session = Depends(get_db)
):
    updated_event = services.update_event(
        db=db,
        event_id=event_id,
        event_data=event_data
    )

    if updated_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return updated_event
@app.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    deleted = services.delete_event(db=db, event_id=event_id)

    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
@app.post(
    "/events/{event_id}/registrations",
    response_model=schemas.RegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
def register_employee(
    event_id: int,
    registration_data: schemas.RegistrationCreate,
    db: Session = Depends(get_db)
):
    result = services.create_registration(
        db=db,
        event_id=event_id,
        registration_data=registration_data
    )

    if result == "event_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    if result == "duplicate":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee is already registered for this event"
        )

    if result == "capacity_full":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Event has reached maximum capacity"
        )

    return result
@app.get(
    "/events/{event_id}/registrations",
    response_model=list[schemas.RegistrationResponse]
)
def read_event_registrations(
    event_id: int,
    db: Session = Depends(get_db)
):
    registrations = services.get_event_registrations(
        db=db,
        event_id=event_id
    )

    if registrations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return registrations
@app.delete(
    "/registrations/{registration_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def cancel_registration(
    registration_id: int,
    db: Session = Depends(get_db)
):
    deleted = services.delete_registration(
        db=db,
        registration_id=registration_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)