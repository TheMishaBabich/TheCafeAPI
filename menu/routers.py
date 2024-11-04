from typing import List

from fastapi import APIRouter, Request, Depends

from menu.dependencies import get_menu_service
from menu.services import MenuService
from . import Dish
from .schemas import DishResponse

menu_router = APIRouter()

@menu_router.post("/add")
async def add_dish(
        dish: DishResponse,
        menu_services: MenuService = Depends(get_menu_service),
):
    menu_services.add_dish(dish)

    return f"Dish add to category {dish.category} name {dish.title} description {dish.description} price {dish.price}"

@menu_router.get("/categories/",response_model=List[DishResponse])
async def get_categories(
    category: str,
    menu_services: MenuService = Depends(get_menu_service)
) -> List[DishResponse]:
    return menu_services.get_category(category)

@menu_router.post("/delete/dish")
async def delete_dish(
        dish_title: str,
        menu_services: MenuService = Depends(get_menu_service)
        ):
    dish = menu_services.delete_dish(dish_title)
    if dish:
        return menu_services.delete_dish(dish_title)