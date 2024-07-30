import json
from google.api import httpbody_pb2
from google.cloud import aiplatform_v1
import os
from dotenv import load_dotenv
load_dotenv()
region=os.getenv("VERTEX_AI_REGION")
endpoint=os.getenv("VERTEX_AI_RESOURCE_NAME")
prediction_client = aiplatform_v1.PredictionServiceClient(
    client_options={"api_endpoint": f"{region}-aiplatform.googleapis.com"}
)

def make_endpoint_request(data):
    json_data = json.dumps(data)

    http_body = httpbody_pb2.HttpBody(
        data=json_data.encode("utf-8"),
        content_type="application/json",
    )

    request = aiplatform_v1.RawPredictRequest(
        endpoint=endpoint,
        http_body=http_body,
    )

    response = prediction_client.raw_predict(request)
    data=json.loads(response.data)
    return data
