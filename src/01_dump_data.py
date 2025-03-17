import json
from os import getenv

from atlassian import Confluence
from dotenv import load_dotenv

from model.ConfluencePageData import ConfluencePageData

load_dotenv()

CONFLUENCE_ACCESS_TOKEN = getenv('CONFLUENCE_ACCESS_TOKEN')
CONFLUENCE_BASE_URL = getenv('CONFLUENCE_BASE_URL')
CONFLUENCE_USERNAME = getenv('CONFLUENCE_USERNAME')


def get_pages_by_label(confluence: Confluence, label, start=0, limit=5):
    return confluence.get_all_pages_by_label(label=label, start=start, limit=limit)

def get_pages_by_space(confluence: Confluence, space, start=0, limit=5):
    return confluence.get_all_pages_from_space(space=space, start=start, limit=limit)


def get_page_data(confluence: Confluence, page_id) -> ConfluencePageData:
    page = confluence.get_page_by_id(page_id, expand='body.storage,version,space')
    return ConfluencePageData(
        id=page['id'],
        space=page['space']['name'],
        title=page['title'],
        contents=page['body']['storage']['value'],
        url=f"{page['_links']['base']}{page['_links']['webui']}",
        last_updated=page['version']['when']
    )


def save_page_data_to_json(page_data: ConfluencePageData, output_dir='../data/confluence'):
    filepath = f"{output_dir}/{page_data.id}.json"
    with open(filepath, 'w') as file:
        json.dump(page_data.to_dict(), file)


if __name__ == '__main__':
    confluence = Confluence(
        url=CONFLUENCE_BASE_URL,
        username=CONFLUENCE_USERNAME,
        password=CONFLUENCE_ACCESS_TOKEN
    )

    pages = get_pages_by_label(confluence, 'ai-poc')

    for page in pages:
        page_data = get_page_data(confluence, page['id'])
        save_page_data_to_json(page_data)
        print(f'Saved page: {page_data.title} ({page_data.id})')

