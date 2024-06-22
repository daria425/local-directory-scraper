from fastapi import APIRouter, Query
from ..dependencies.scraper import Scraper
from ..dependencies.content_reader import CamdenContentReader, IslingtonContentReader
from ..models.ScrapeRequest import ScrapeRequest
from ..dependencies.helpers import replace_url
router=APIRouter(
    prefix='/search'
)

@router.get("/")
def get_regional_categories(region:str):
    category_page=Scraper().get_category_page(region)
    if region=="camden":
        print(category_page)
        categories=CamdenContentReader(category_page).get_main_categories()
    elif region=="islington":
        categories=IslingtonContentReader(category_page).get_main_categories()
    return categories

@router.post("/subcategories")
def get_subcategories(request_url: ScrapeRequest, region: str = Query(..., description="Region of the URL")):
    url=replace_url(request_url.url, region)
    html=Scraper().scrape(url)[0]
    print(url)
    if region=="camden":
        subcategories=CamdenContentReader(html).get_subcategories()
    elif region=="islington":
        subcategories=IslingtonContentReader(html).get_subcategories()
    return subcategories






