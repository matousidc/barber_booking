# Barber booking app

- REST API made with FastAPI.
- API endpoints:
    - fetch_schedule - GET: show schedule for a given week using Jinja template
    - book_slot - PUT: books available time slot for user distinguished by email
- Using SQLAlchemy ORM, PlanetScale serverless MySQL database, Pydantic models.