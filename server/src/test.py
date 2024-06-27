from dependencies.scraper import Scraper
url="https://cindex.camden.gov.uk/kb5/camden/cd/results.action?communitychannel=1-9&sr=10&nh=10"

html, title=Scraper().scrape(url)
print(html, title)