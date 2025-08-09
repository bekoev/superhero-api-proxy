from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db.base import DBModelBase


class HeroDB(DBModelBase):
    __tablename__ = "heroes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    powerstats: Mapped[PowerStatsDB] = relationship(
        back_populates="hero", cascade="all, delete-orphan", lazy="selectin"
    )


class PowerStatsDB(DBModelBase):
    __tablename__ = "powerstats"

    id: Mapped[int] = mapped_column(primary_key=True)
    intelligence: Mapped[int] = mapped_column(nullable=True)
    strength: Mapped[int] = mapped_column(nullable=True)
    speed: Mapped[int] = mapped_column(nullable=True)
    power: Mapped[int] = mapped_column(nullable=True)
    hero_id: Mapped[int] = mapped_column(ForeignKey("heroes.id"), nullable=False)
    hero: Mapped[HeroDB] = relationship(back_populates="powerstats")
