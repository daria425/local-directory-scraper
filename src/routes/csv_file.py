from fastapi import APIRouter, Query
from ..dependencies.make_csv import make_category_csv
from ..models.ScrapeRequest import ScrapeRequest
from ..dependencies.helpers import replace_url
router=APIRouter(prefix="/csv-file")

@router.post("/")
def send_csv(request_url: ScrapeRequest, region: str = Query(..., description="Region of the URL")):
    url=replace_url(request_url.url, region)
    df_json=make_category_csv(url, region)
    return df_json
