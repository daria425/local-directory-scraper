from abc import ABC, abstractmethod
import re
from urllib.parse import urlparse, parse_qs
from .autotagging import classify_tags
import pandas as pd
from bs4 import BeautifulSoup


file_path="./data.json"
class ContentReaderBase(ABC):
    def __init__(self, html_content, use_local_classifier):
        self.html_content = html_content
        self.use_local_classifier=use_local_classifier
        self.soup_object = BeautifulSoup(self.html_content, "html.parser")
        self.tag_list = [
    "benefits-advice",
    "debt-advice",
    "budget-advice",
    "homelessness",
    "housing-rights",
    "home-swap",
    "energy-bills",
    "council-tax",
    "credit-union",
    "mental-health",
    "long-term-health-condition",
    "disability",
    "neurodiversity",
    "cancer",
    "bereavement",
    "drugs&alcohol",
    "domestic-abuse",
    "criminal-justice",
    "gambling",
    "fire&flood",
    "victim-support",
    "suicide",
    "families",
    "children",
    "young-adult",
    "elder",
    "single-parents",
    "young-parents",
    "pregnancy",
    "adult-social-care",
    "employability",
    "small-businesses",
    "foodbank",
    "food-projects",
    "community-larder",
    "clothing-bank",
    "household-goods",
    "community-hub",
    "ex-army",
    "refugees",
    "carers",
    "womens-support",
    "mens-support",
    "lgbtq+",
    "fishermen",
    "drinks",
    "hospitality",
    "racial-justice"
]



    @staticmethod
    def read_html_from_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return html_content

    @staticmethod
    def filter_contact_info(contact_list):
        def is_valid_contact(item):
            # Check if the item is a number or contains "Fax"
            return bool(re.match(r'^[\d\s\+\-\(\)]+$', item))
        
        # Filter the list using the is_valid_contact function
        return [item for item in contact_list if is_valid_contact(item)]

    @staticmethod
    def get_query_str(url, query_str):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        id_value = query_params.get(query_str, [None])[0]
        return id_value
    

    
    @abstractmethod
    def get_main_categories(self):
        pass

    @abstractmethod
    def get_last_page(self):
        pass

    @abstractmethod
    def extract_info(self):
        pass

    def create_tag_str(self, text):
        top_tags=classify_tags(self.tag_list, text, self.use_local_classifier)
        tag_strings=[item[0] for item in top_tags]
        tags=" ".join(tag_strings)
        return tags

    def create_df(self):
        results = self.extract_info()
        df = pd.DataFrame.from_dict(results)
        df["Name"]=df["Name"].str.strip().replace('\n', '')
        df["Short text description"] = df["Short text description"].str.strip()
        return df

class CamdenContentReader(ContentReaderBase):
    def __init__(self, html_content, use_local_classifier):
        super().__init__(html_content, use_local_classifier)
        self.prefix="https://cindex.camden.gov.uk/kb5/camden/cd/"

    def get_last_page(self):
        try:
            pagination_container = self.soup_object.find("ul", class_="pagination")
            last_page_link = pagination_container.find("a", class_="last-page")
            if last_page_link:
                last_page = self.get_query_str(last_page_link["href"], 'sr')
                return last_page
            else: 
                return None
        except Exception as e:
            print(e)
            return None

    def extract_info(self):
        result_list = self.soup_object.find_all("div", class_="result_hit")
        results = []
        for result in result_list:
            org_link_item = result.find("header").find("h3")
            org_name, org_link = org_link_item.text, org_link_item.find("a")['href']
            org_id = self.get_query_str(org_link, 'id')
            
            org_address = result.find("div", class_="address_lines")
            org_adress_lines = [span.text for span in org_address.find_all("span")] if org_address is not None else []
            if org_adress_lines:
                org_postcode = org_adress_lines[-1]
            else:
                org_postcode = ''
            org_adress_lines = ','.join(org_adress_lines)
            
            org_description = result.find("div", class_="hit-body")
            org_description_text = ''
            for child in org_description.children:
                if child.name is None:
                    org_description_text += str(child).strip()
            
            telephone_nums = result.find("div", class_="hit-telephone")
            telephone_num_lines = [span.text for span in telephone_nums.find_all("span")] if telephone_nums is not None else []
            telephone_num_lines = self.filter_contact_info(telephone_num_lines)
            telephone_num_lines = ','.join(telephone_num_lines)
            
            links = result.find("footer").find_all("a")
            org_email = ''
            org_website = ''
            for link in links:
                if link.find("i", class_="fa fa-envelope"):
                    org_email = link["href"]
                    org_email = org_email.replace("mailto:", "")
                elif link.find("i", class_="fa fa-external-link"):
                    org_website = link["href"]
            tags=self.create_tag_str(org_description_text)
            result = {
                "id": org_id,
                "Name": org_name,
                "Category tags": tags, 
                "Short text description": org_description_text,
                "Postcode": org_postcode,
                "Website": org_website,
                "Phone - call": telephone_num_lines,
                "Local / National": "Local", 
                "location": "Camden", 
                "Email": org_email
            }
           #get the tags with the description here
            results.append(result)
        return results
    def get_main_categories(self, save=True):
        category_container=self.soup_object.find("div", id="category-blocks")
        category_block_items=category_container.find_all("div", class_="sub_cat")
        categories=[]
        for block in category_block_items:
            link=block.find("a")
            rel_link=link["href"]
            category_description=link["data-content"]
            category_name=link["data-original-title"]
            category_link=self.prefix + rel_link
            result={
                "category_name":category_name, "category_description":category_description, "category_link": category_link
            }
            categories.append(result)
     
        return categories
    
    def get_subcategories(self):
       
        category_list_container=self.soup_object.find("div", class_="channel_facets").find("ul", class_=re.compile(r".*-cats"))
        category_list_items=category_list_container.find_all("a")
        subcategories=[]
        for item in category_list_items:
                    rel_link=item["href"].replace("/kb5/camden/cd/core/../", "")
                    subcategory_name=item["title"]
                    result={
                        "subcategory_link": self.prefix + rel_link, 
                        "subcategory_name":subcategory_name
                    }
                    subcategories.append(result)
        return subcategories
    
class IslingtonContentReader(ContentReaderBase):
    def __init__(self, html_content, use_local_classifier):
        super().__init__(html_content, use_local_classifier)
        self.prefix="https://findyour.islington.gov.uk/kb5/islington/directory/"

    def get_last_page(self):
        try:
            result_nav = self.soup_object.find("nav", attrs={"aria-label": "Results pagination"})
            last_page_btn = result_nav.find_all("a", string=re.compile(r'\b.*last.*\b', re.IGNORECASE))
            if last_page_btn:
                last_page_query_str = last_page_btn[0]["data-sr"]
            else:
                last_page_query_str = None
            return last_page_query_str
        except Exception as e:
            print(e)
            return None

    def extract_info(self):
        item_list=self.soup_object.find("ol", class_="results-list list-unstyled")
        organization_list=item_list.find_all("li", class_="mb-4")
        results=[]
        for organization in organization_list:
            organization_link_item=organization.find("a")
            org_link, org_name=organization_link_item['href'], organization_link_item.text
            org_id=self.get_query_str(org_link, 'id')
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
            tags=self.create_tag_str(org_description)
            result={
                "id": org_id,
                "Name": org_name,
                "Category tags": tags,
                "Short text description": org_description,
                "Postcode": org_postcode,
                "Website": org_website,
                "Phone - call":org_phone,
                "Local / National": "Local", 
                "location": "Islington", 
                "Email": org_email
            }
            results.append(result)
        return results
    
    def get_main_categories(self):
        category_section=self.soup_object.find("section", class_="category-blocks")
        category_block_items=category_section.find_all("div", class_="category-block")
        categories=[]
        for block in category_block_items:
            link=block.find("a")
            rel_link=link["href"]
            category_description=""
            category_name=link.find("h3").text
            category_link=self.prefix + rel_link
            result={"category_name": category_name.strip(), "category_description": category_description, "category_link": category_link
            }
            categories.append(result)
        return categories
    
    def get_subcategories(self):
        category_list_container=self.soup_object.find("div", id="facets-channels").find("ol", class_="list-unstyled")
        category_list_items=category_list_container.find_all("a")
        subcategories=[]
        for item in category_list_items:
            rel_link=item["href"].replace("/kb5/islington/directory/core/../", "")
            subcategory_name=item.text
            result={
                "subcategory_link": self.prefix + rel_link, 
                "subcategory_name":subcategory_name
            }
            subcategories.append(result)
        return subcategories

    





