from bs4 import BeautifulSoup 

file_path="./output.html"

def read_html_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

html=read_html_from_file(file_path)
soup=BeautifulSoup(html, "html.parser")
item_list=soup.find("ol", class_="results-list list-unstyled")
# print(item_list)
organization_list=item_list.find_all("li", class_="mb-4")
for organization in organization_list:
    organization_link_item=organization.find("a")
    org_link, org_name=organization_link_item['href'], organization_link_item.text
    print(org_link, org_name)


    

    


