from fastapi import APIRouter, Query
from ..dependencies.scraper import Scraper
from ..dependencies.database import Database
from ..dependencies.categories import Categories
from ..dependencies.content_reader import CamdenContentReader, IslingtonContentReader
from ..models.ScrapeRequest import ScrapeRequest
from ..dependencies.helpers import replace_url
from dotenv import load_dotenv
import os
load_dotenv()
mongo_db_uri=os.environ.get("MONGODB_URI")
router=APIRouter(
    prefix='/search'
)

@router.get("/")
def get_regional_categories(region:str):
    db=Database(mongo_db_uri, "directory-contents")
    categories=Categories().get_main_categories(region, from_db=True, db=db)
    db.close()
    return categories

@router.post("/subcategories")
def get_subcategories(request_url: ScrapeRequest, region: str = Query(..., description="Region of the URL")):
    db=Database(mongo_db_uri, "directory-contents")
    url=replace_url(request_url.url)
    subcategories=Categories().get_subcategories(url, region, from_db=True, db=db)
    db.close()
    return subcategories






