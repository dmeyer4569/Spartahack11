from sqlalchemy import String, Date, Text, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

class Base(DeclarativeBase):
    pass

class Pantry(Base):
    __tablename__ = "pantry_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    expire: Mapped[Date] = mapped_column(Date)
    img_path: Mapped[str] = mapped_column(Text)
    
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))
    # Many to one 
    location: Mapped["Location"] = relationship(
        back_populates="items"
    )

    def __repr__(self) -> str:
        return f"Pantry_Item(id={self.id!r}, name={self.name!r}, expire={self.expire!r}, img_path={self.img_path!r}, stt={self.stt!r})"
    
class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[str] = mapped_column(String(255))

    # One to Many
    items: Mapped[List["Pantry"]] = relationship(
        back_populates="location", 
        cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"id={self.id}, location={self.location}"
