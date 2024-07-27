from dotenv import load_dotenv
import os
import requests
load_dotenv()
hf_token=os.getenv("HF_TOKEN")


def query(api_url, headers, payload):
	response = requests.post(api_url, headers=headers, json=payload)
	return response.json()

def split_tag_list(tag_list, chunk_size):
    return [tag_list[i:i+chunk_size]for i in range(0, len(tag_list), chunk_size)]

def classify(tag_list,text, chunk_size=10, num_tags=5):
    chunks=split_tag_list(tag_list, chunk_size)
    zips=[]
    for chunk in chunks:
        api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
        headers = {"Authorization": f"Bearer {hf_token}"}
        payload={
            "inputs":text, 
            "parameters":{"candidate_labels":chunk, "multi_label": True}
        }
        response=query(api_url, headers, payload)
        print(response)
        zipped_response=list(zip(response["labels"], response["scores"]))
        zips.append(zipped_response)
    joined_list=[item for tuple_chunk in zips for item in tuple_chunk ]
    sorted_list=sorted(joined_list, key=lambda x: x[1], reverse=True)
    return sorted_list[:num_tags]


     
     