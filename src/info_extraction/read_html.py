from bs4 import BeautifulSoup 
import pandas as pd
from urllib.parse import urlparse, parse_qs
import re
file_path="./output.html"

def read_html_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

def filter_contact_info(contact_list):
    def is_valid_contact(item):
        # Check if the item is a number or contains "Fax"
        return bool(re.match(r'^[\d\s\+\-\(\)]+$', item))
    
    # Filter the list using the is_valid_contact function
    return [item for item in contact_list if is_valid_contact(item)]

def get_id(url):
    parsed_url=urlparse(url)
    query_params = parse_qs(parsed_url.query)
    id_value = query_params.get('id', [None])[0]
    return id_value

def get_last_page(html_content):
    soup_object=BeautifulSoup(html_content, "html.parser")
    try:
        result_nav=soup_object.find("nav", attrs={"aria-label":"Results pagination"})
        last_page_btn=result_nav.find_all("a",string=re.compile(r'\b.*last.*\b', re.IGNORECASE) )
        if (last_page_btn):
            last_page_query_str=last_page_btn[0]["data-sr"]
        else:
            last_page_query_str=None
        return last_page_query_str
    except Exception as e:
        print(e)

    


def extract_info_islington(html_content):
    soup_object=BeautifulSoup(html_content, "html.parser")
    result_nav=soup_object.find("nav", attrs={"aria-label":"Results pagination"})
    print(result_nav)
    item_list=soup_object.find("ol", class_="results-list list-unstyled")
    organization_list=item_list.find_all("li", class_="mb-4")
    results=[]
    for organization in organization_list:
        organization_link_item=organization.find("a")
        prefix="https://findyour.islington.gov.uk/kb5/islington/directory/"
        org_link, org_name=organization_link_item['href'], organization_link_item.text
        org_id=get_id(org_link)
        org_description_item=organization.find("div", class_="mb-3 w-100")
        org_description=org_description_item.text
        link_btns=organization.find_all("a", class_="btn btn-outline-dark mb-3 mr-3")
        org_postcode=''
        org_email=''
        org_website=''
        org_phone=''
        for btn in link_btns:
            if btn.find("span", class_="far fa-map-marker-alt fa-fw"):
                org_postcode=btn.text
            elif btn.find("span", class_="far fa-envelope"):
                org_email=btn['href']
                org_email=org_email.replace("mailto:", "")
            elif btn.find("span", class_="far fa-link"):
                org_website=btn["href"]
            elif btn.find("span", class_="fas fa-phone"):
                org_phone=btn['href']
                org_phone=org_phone.replace("tel:", "")
        result={
            "id":org_id,
            "name": org_name, 
            "description": org_description, 
            "organization_link": prefix+org_link, 
            "postcode": org_postcode, 
            "organization_website":org_website
        }
        results.append(result)
    return results

def create_df(html_object, location):
    if location.lower()=="islington":
        results=extract_info_islington(html_object)
    df=pd.DataFrame.from_dict(results)
    df["description"]=df["description"].str.strip()
    return df

    


def extract_info_camden(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    result_list = soup.find_all("div", class_="result_hit")
    results = []

    for result in result_list:
        prefix = "https://cindex.camden.gov.uk/kb5/camden/cd/"
        org_link_item = result.find("header").find("h3")
        org_name, org_link = org_link_item.text, org_link_item.find("a")['href']
        org_id = get_id(org_link)
        
        org_address = result.find("div", class_="address_lines")
        org_adress_lines = [span.text for span in org_address.find_all("span")]
        org_postcode = org_adress_lines[-1]
        org_adress_lines = ','.join(org_adress_lines)
        
        org_description = result.find("div", class_="hit-body")
        org_description_text = ''
        for child in org_description.children:
            if child.name is None:
                org_description_text += str(child).strip()
        
        telephone_nums = result.find("div", class_="hit-telephone")
        telephone_num_lines = [span.text for span in telephone_nums.find_all("span")]
        telephone_num_lines = filter_contact_info(telephone_num_lines)
        telephone_num_lines = ','.join(telephone_num_lines)
        
        links = result.find("footer").find_all("a")
        org_email = ''
        org_website = ''
        for link in links:
            if link.find("i", class_="fa fa-envelope"):
                org_email = link["href"]
                org_email=org_email.replace("mailto:", "")
            elif link.find("i", class_="fa fa-external-link"):
                org_website = link["href"]
        
        result = {
            "id": org_id,
            "name": org_name,
            "description": org_description_text,
            "organization_link": prefix + org_link,
            "address": org_adress_lines,
            "postcode": org_postcode,
            "organization_website": org_website,
            "telephone": telephone_num_lines,
            "email": org_email
        }
        results.append(result)
    
    return results

html_content=read_html_from_file(file_path)
results=extract_info_camden(html_content)
print(results[0])


    




    
    
    

    


