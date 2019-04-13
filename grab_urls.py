import json
from os.path import exists
from os import makedirs

import requests


# Loop through each page and save the URL end-points of the data files
# You may need to set up an empty directory called "urls"
print('Fetching:')
api_root = 'https://iatiregistry.org/api/3/action'
page = 1
page_size = 1000
while True:
    print(f'Page {page}')
    start = page_size * (page - 1)
    result = requests.post(
        f'{api_root}/package_search',
        data={'start': start, 'rows': page_size}).json()['result']
    if result['results'] == []:
        break

    for package in result['results']:
        organization = package['organization']
        if len(package['resources']) > 0 and organization:
            metadata_filepath = f'metadata/{organization["name"]}'
            if not exists(metadata_filepath):
                makedirs(metadata_filepath)
                org_metadata = requests.post(
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
