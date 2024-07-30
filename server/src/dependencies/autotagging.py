from dotenv import load_dotenv
import os
import requests
from transformers import pipeline
from .endpoint_request import make_endpoint_request
load_dotenv()
hf_token=os.getenv("HF_TOKEN")
api_url=os.getenv("HF_MODEL_URL")

def query(api_url, headers, payload):
	response = requests.post(api_url, headers=headers, json=payload)
	return response.json()

def split_tag_list(tag_list, chunk_size):
    return [tag_list[i:i+chunk_size]for i in range(0, len(tag_list), chunk_size)]

def classify_tags(tag_list,text, use_local_classifier, chunk_size=10, num_tags=5):
    chunks=split_tag_list(tag_list, chunk_size)
    zips=[]
    if use_local_classifier:
        for chunk in chunks:
             data={
                  "sequences": text, 
                  "candidate_labels": chunk
             }
             response=make_endpoint_request(data)
             zipped_response=list(zip(response["labels"], response["scores"]))
             zips.append(zipped_response)
    else:
        for chunk in chunks:
            headers = {"Authorization": f"Bearer {hf_token}"}
            payload={
                "inputs":text, 
                "parameters":{"candidate_labels":chunk, "multi_label": True}
            }
            response=query(api_url, headers, payload)
            zipped_response=list(zip(response["labels"], response["scores"]))
            zips.append(zipped_response)
    joined_list=[item for tuple_chunk in zips for item in tuple_chunk ]
    sorted_list=sorted(joined_list, key=lambda x: x[1], reverse=True)
    return sorted_list[:num_tags]
    
def classify_location(text,use_local_classifier):
     response=''
     candidates=["Local", "National"]
     if use_local_classifier:
        data={
             "sequences": text, 
             "candidate_labels": candidates
        }
        response=make_endpoint_request(data)
     else:
            headers = {"Authorization": f"Bearer {hf_token}"}
            payload={
                "inputs":text, 
                "parameters":{"candidate_labels":candidates}
            }
            response=query(api_url, headers, payload)
     location_tag=response["labels"][0]
     return location_tag
          

            
