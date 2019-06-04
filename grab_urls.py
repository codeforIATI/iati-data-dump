import json
from os.path import exists
from os import makedirs
from time import sleep

import requests


def request_with_backoff(*args, attempts=5, backoff=0.5, **kwargs):
    for attempt in range(1, attempts + 1):
        try:
            result = requests.request(*args, **kwargs)
            return result
        except requests.exceptions.ConnectionError:
            wait = attempt * backoff
            print(f'Rate limited! Retrying after {wait} seconds')
            sleep(wait)
    raise Exception(f'Failed after {attempts} attempts. Giving up.')


# Loop through each page and save the URL end-points of the data files
# You may need to set up an empty directory called "urls"
print('Fetching:')
api_root = 'https://iatiregistry.org/api/3/action'
page = 1
page_size = 1000
while True:
    print(f'Page {page}')
    start = page_size * (page - 1)
    result = request_with_backoff(
        'post',
        f'{api_root}/package_search',
        data={'start': start, 'rows': page_size}).json()['result']
    if result['results'] == []:
        break

    for package in result['results']:
        organization = package['organization']
        if package['resources'] == [] or not organization:
            continue
        metadata_filepath = f'metadata/{organization["name"]}'
        if not exists(metadata_filepath):
            makedirs(metadata_filepath)
            org_metadata = request_with_backoff(
                'post',
                f'{api_root}/group_show',
                data={'id': organization['name']}).json()['result']
            org_metadata_file = f'{metadata_filepath}.json'
            with open(org_metadata_file, 'w') as f:
                json.dump(org_metadata, f)
        metadata_file = f'{metadata_filepath}/{package["name"]}.json'
        with open(metadata_file, 'w') as f:
            json.dump(package, f)

        file = f'urls/{organization["name"]}'
        url_string = '{name} {url}\n'.format(
            name=package['name'],
            url=package['resources'][0]['url'],
        )
        with open(file, 'a') as f:
            f.write(url_string)
    page += 1
