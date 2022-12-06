import sys
import shutil
import json
from os.path import dirname, exists, join
from os import makedirs
from time import sleep

import requests


def request_with_backoff(*args, attempts=100, backoff=0.1, **kwargs):
    for attempt in range(1, attempts + 1):
        # exponential backoff
        wait = (pow(2, attempt) - 1) * backoff
        try:
            result = requests.request(*args, **kwargs)
            if result.status_code == 200:
                sleep(wait)
                return result
        except requests.exceptions.ConnectionError:
            pass
        print(f'Error! Retrying after {wait} seconds')
        sleep(wait)
    raise Exception(f'Failed after {attempts} attempts. Giving up.')


def main(args):
    cache = '--cache' in args
    skip_metadata = '--skip-metadata' in args
    if skip_metadata:
        print('Skipping metadata')

    # Loop through each page and save the URL end-points of the data files
    # You may need to set up an empty directory called "urls"
    print('Fetching:')

    tmpl = 'curl -L -k -f -s ' + \
           '-H "Accept: application/xhtml+xml, application/xml,*/*;q=0.9" ' + \
           '--retry 4 --retry-delay 10 -y 30 ' + \
           '-Y 1000 -A "IATI data dump 1.0" ' + \
           '--create-dirs -o data/{publisher_id}/{dataset_name}.xml ' + \
           '"{url}" 2>&1 >/dev/null ; exitcode=$? ; ' + \
           'test "$exitcode" != 0 && ' + \
           'echo $exitcode {publisher_id} {dataset_name} "{url}" > ' + \
           'logs/{dataset_name}.log && touch ' + \
           'data/{publisher_id}/{dataset_name}.xml\n'

    datasets = requests.get(
        "https://registry.codeforiati.org/dataset_list.json").json()["result"]

    publishers = requests.get(
        "https://registry.codeforiati.org/publisher_list.json").json()["result"]
    publishers = {
        publisher["name"]: publisher
        for publisher in publishers
    }

    for dataset in datasets:
        organization = dataset['organization']
        if dataset['resources'] == [] or not organization:
            continue
        dataset_name = dataset['name']
        url = dataset['resources'][0]['url']
        publisher_id = organization["name"]

        if cache:
            filename = join(publisher_id, dataset_name + '.xml')
            cache_file = join('cache', filename)
            if exists(cache_file):
                out_file = join('data', filename)
                out_path = dirname(out_file)
                if not exists(out_path):
                    makedirs(out_path, exist_ok=True)
                shutil.move(cache_file, out_file)

        if not skip_metadata:
            metadata_filepath = f'metadata/{publisher_id}'
            if not exists(metadata_filepath):
                makedirs(metadata_filepath)
                publisher_metadata = publishers[publisher_id]
                publisher_metadata_file = f'{metadata_filepath}.json'
                with open(publisher_metadata_file, 'w') as f:
                    json.dump(publisher_metadata, f)
            metadata_file = f'{metadata_filepath}/{dataset_name}.json'
            with open(metadata_file, 'w') as f:
                json.dump(dataset, f)

        with open(f'urls/{publisher_id}', 'a') as f:
            f.write(f'{dataset_name} {url}\n')

        output = tmpl.format(
            publisher_id=publisher_id,
            dataset_name=dataset_name,
            url=url.replace(' ', '%20'),
        )
        with open('downloads.curl', 'a') as f:
            f.write(output)


if __name__ == '__main__':
    main(sys.argv[1:])
