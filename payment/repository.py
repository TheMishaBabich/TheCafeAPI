from sqlalchemy.orm import Session
from menu.model import Dish

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_curr_dish_price(self, title: str) -> Dish:
        return self.db.query(Dish).filter(Dish.title == title).first()



