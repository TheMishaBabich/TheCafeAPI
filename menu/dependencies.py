from fastapi import Depends
from sqlalchemy.orm import Session

from db import get_db_session
from menu.repository import MenuRepository
from menu.services import MenuService


def get_menu_repository(db: Session = Depends(get_db_session)) -> MenuRepository:
    return MenuRepository(db)

def get_menu_service(repository: MenuRepository = Depends(get_menu_repository)) -> MenuService:
    return MenuService(repository)