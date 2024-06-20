from fastapi import APIRouter, Query
from ..dependencies.scraper import Scraper
from ..dependencies.content_reader import CamdenContentReader, IslingtonContentReader
from ..models.ScrapeRequest import ScrapeRequest
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

@router.post("/subcategories")
def get_subcategories(request_url: ScrapeRequest, region: str = Query(..., description="Region of the URL")):
    html=Scraper().scrape(request_url.url)[0]
    if region=="camden":
        subcategories=CamdenContentReader(html).get_subcategories()
    elif region=="islington":
        subcategories=IslingtonContentReader(html).get_subcategories()
    return subcategories






