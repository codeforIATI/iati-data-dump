IATI Registry Refresher
=======================

[![License: MIT](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/IATI/IATI-Registry-Refresher#licence)

Introduction
------------

This application queries the [IATI Registry API](iatiregistry.org) for URLs of data recorded on the registry, and then downloads that data.

The application is just 2 scripts that you run one after the other:

 * `grab_urls.py` queries the registry and creates a text file called "downloads.curl" of curl commands for downloading the data. It also optionally downloads dataset metadata. If you don’t want to download dataset metadata, run:

    ```
    python grab_urls.py --skip-metadata
    ```
 * `fetch_data.sh` runs the generated downloads.curl file, and logs any errors encountered.


Requirements
------------
IATI Registry Refresher requires python 3.

It also requires curl.

On Ubuntu:

```
sudo apt-get install curl
sudo apt-get install python-pip python-dev
```

Then set up a virtual environment:

```
python3 -m venv pyenv
source pyenv/bin/activate
pip install -r requirements.txt
```

Installation and usage
----------------------

Clone the repository:
```
git clone https://github.com/codeforIATI/IATI-Registry-Refresher.git
cd IATI-Registry-Refresher
```

Create empty directories:
```
./reset_folders.sh
```

To create the downloads.curl file, run:
```
python grab_urls.py [--skip-metadata]
```

To fetch the data, run:
```
./fetch_data.sh
```

Bugs, issues and feature requests
---------------------------------

If you find any bugs, note any issues or have any feature requests, please
report them at https://github.com/codeforIATI/IATI-Registry-Refresher

Licence
-------

``` 
Copyright 2012 caprenter <caprenter@gmail.com>
     
This file is part of IATI Registry Refresher.
     
IATI Registry Refresher is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
    
IATI Registry Refresher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
    
You should have received a copy of the GNU General Public License
along with IATI Registry Refresher.  If not, see <http://www.gnu.org/licenses/>.
```
