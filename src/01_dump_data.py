from atlassian import Confluence
from dotenv import load_dotenv
from os import getenv
from pprint import pprint
from model.ConfluencePageData import ConfluencePageData
import json
load_dotenv()

CONFLUENCE_ACCESS_TOKEN = getenv('CONFLUENCE_ACCESS_TOKEN')
CONFLUENCE_BASE_URL = getenv('CONFLUENCE_BASE_URL')
CONFLUENCE_USERNAME = getenv('CONFLUENCE_USERNAME')

def get_pages_by_label(confluence_dep, label):
    return confluence_dep.get_all_pages_by_label(label=label, start=0, limit=5)

def get_page_data(confluence_dep, page_id):
    page_from_confluence = confluence_dep.get_page_by_id(page_id, expand='body.storage,version,space')
    return ConfluencePageData(
        id=page_from_confluence['id'],
        space=page_from_confluence['space']['name'],
        title=page_from_confluence['title'],
        contents=page_from_confluence['body']['storage']['value'],
        url=page_from_confluence['_links']['base'] + page_from_confluence['_links']['webui'],
        last_updated=page_from_confluence['version']['when']
    )

def save_page_data_to_json(page_data):
    with open(f'../data/confluence/{page_data.id}.json', 'w') as f:
        f.write(json.dumps(page_data.to_dict()))

if __name__ == '__main__':
    confluence = Confluence(
        url=CONFLUENCE_BASE_URL,
        username=CONFLUENCE_USERNAME,
        password=CONFLUENCE_ACCESS_TOKEN  # API token works as a password
    )

    pages = get_pages_by_label(confluence, 'ai-poc')
    pd = get_page_data(confluence, pages[0]['id'])
    save_page_data_to_json(pd)
    pprint(pd)