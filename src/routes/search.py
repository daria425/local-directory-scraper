from fastapi import APIRouter
from dependencies.scraper import Scraper
from dependencies.content_reader import CamdenContentReader, IslingtonContentReader
router=APIRouter(
    prefix='/search'
)

@router.get("/")
def get_regional_categories(region:str):
    category_page=Scraper().get_category_page(region)
    if region=="camden":
        categories=CamdenContentReader(category_page).get_main_categories()
    elif region=="islington":
        categories=IslingtonContentReader(category_page).get_main_categories()
    return categories


