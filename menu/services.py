from typing import List

from fastapi import HTTPException

from .repository import MenuRepository
from .schemas import  DishResponse
from . import Dish

class MenuService:
    def __init__(self, repository: MenuRepository):
        self.repository = repository

    def add_dish(self, dish_request: DishResponse) -> DishResponse:
        dish = Dish(
            category=dish_request.category,
            title=dish_request.title,
            description=dish_request.description,
            price=dish_request.price,
        )
        try:
            dish = self.repository.add_dish(dish)
            return DishResponse(message=f"Dish '{dish.title}' added successfully.")
        except Exception as e:
            print(e)
            return DishResponse(message="An error occurred while adding the dish.")

    def get_category(self, category: str) -> List[DishResponse]:
        dishes = self.repository.get_category(category)
        if not dishes:
            raise HTTPException(status_code=404, detail="Category not found")
        return [DishResponse.model_validate(dish) for dish in dishes]

    def delete_dish(self, dish_title: str) -> DishResponse:
        dish = self.repository.delete_dish(dish_title)
        if dish is None:
            raise HTTPException(status_code=404, detail="Dish not found")
        return f"Dish '{dish.title}' deleted successfully."