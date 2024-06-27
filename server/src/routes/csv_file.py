from fastapi import APIRouter, Query
from fastapi.responses import Response
from ..dependencies.make_csv import make_category_csv
from ..models.ScrapeRequest import ScrapeRequest
from ..dependencies.helpers import replace_url


router=APIRouter(prefix="/csv-file")

@router.post("/")
def send_csv(request_url: ScrapeRequest, region: str = Query(..., description="Region of the URL")):
    url=replace_url(request_url.url)
    df=make_category_csv(url, region)
    response_headers={'Content-Disposition': 'attachment; filename="data.csv"'}
    return Response(df.to_csv(index=False), headers=response_headers, media_type="text/csv" )
    
