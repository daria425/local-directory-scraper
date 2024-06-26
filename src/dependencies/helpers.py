import re
def replace_url(url, region):
    if (region=="islington"):
        pattern = r'(\w+)\.page'
    # Replace the word before .page with 'results'
        new_url = re.sub(pattern, 'results.page', url)
        return new_url
    else:
        return url

