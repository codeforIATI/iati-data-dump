#!/bin/bash
#
#      fetch_data.sh
#
#      Copyright 2012 caprenter <caprenter@gmail.com>
#
#      This file is part of IATI Registry Refresher.
#
#      IATI Registry Refresher is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      IATI Registry Refresher is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with IATI Registry Refresher.  If not, see <http://www.gnu.org/licenses/>.
#
#      IATI Registry Refresher relies on other free software products. See the README.txt file
#      for more details.
#

# Set the internal field seperator to newline, so that we can loop over newline
# seperated url lists correctly.
IFS=$'\n'

FILES=urls/*
for f in $FILES
do
  for url_line in `cat $f`; do
    url=`echo $url_line | sed 's/^[^ ]* //'`
    package_name=`echo $url_line | sed 's/ .*$//'`
    mkdir -p data/`basename $f`/

    echo "$url"
    curl --location --insecure --fail --silent --show-error --header "Accept: application/xhtml+xml,application/xml,*/*;q=0.9" --retry 4 --retry-delay 10 --speed-time 30 --speed-limit 1000 --user-agent "IATI data dump" --create-dirs --output data/`basename $f`/$package_name.xml "$url" 2>&1 >/dev/null
    # Fetch the exitcode of the previous command
    exitcode=$?
    # If the exitcode is not zero (ie. there was an error), output to STDERR
    if [ $exitcode -ne 0 ]; then
      echo $exitcode `basename $f` $url_line >&2
    fi

    # Delay of 1/2 second between requests, so as not to upset servers
    sleep 0.5s
  done
done
