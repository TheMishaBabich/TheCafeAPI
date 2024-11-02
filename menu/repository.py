from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import Dish



class MenuRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_dish(self, dish: Dish) -> Dish:
        self.db.add(dish)
        try:
            self.db.commit()
            self.db.refresh(dish)
            return dish
        except IntegrityError:
            print("IntegrityError")
            self.db.rollback()
            raise

    def get_category(self, category: str) -> List[Dish]:
        try:
            return self.db.query(Dish).filter(Dish.category == category).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_dish(self, dish_title: str):
        dish = self.db.query(Dish).filter(Dish.title == dish_title).first()
        if dish:
            self.db.delete(dish)
            self.db.commit()
            return dish
        return None