from sqlalchemy.orm import Session
from models import Pantry, Location
from session import engine
from datetime import date

session = Session(engine)

kitchen = Location(location="Kitchen")
session.add(kitchen)
session.commit()

print(kitchen.id)

milk = Pantry(
    name="milk",
    expire=(2026, 2, 1),
    img_path="milk.png",
    location=kitchen
)
egg = Pantry(
    name="egg",
    expire=(2026, 2, 4),
    img_path="egg.png",
    location=kitchen
)

session.add_all([milk, egg]
                )
session.commit()
