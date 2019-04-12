#!/bin/bash
## Perform several validation tests on the files in a downloaded data snapshot

IFS=$'\n'

echo "Downloading Schemas"
./download_schemas.sh

# Check for xml well formedness errors
rm -f xml-errors validation-errors

FILES=urls/*
for f in $FILES; do
    for url_line in `cat $f`; do
        org_name=`basename $f`
        package_name=`echo $url_line | sed 's/ .*$//'`
        filename="data/$org_name/$package_name.xml"
        echo "Checking XML: $package_name"
        # Check file is not empty
        if [[ -s $filename ]]; then
            xmllint --noout $filename 2> /dev/null
            if [ $? -ne 0 ]; then
                echo $org_name $url_line >> xml-errors;
                continue
            fi
        fi

        echo "Validating: $filename"
        if [[ -s $filename ]]; then
            topel="`xmllint --xpath "name(/*)" "$filename"`"
            version="`xmllint --xpath "string(/*/@version)" "$filename"`"
            if [ "$version" == "1.01" ] || [ "$version" == "1" ] || [ "$version" == "1.0" ] || [ "$version" == "1.00" ]; then version="1.01"; fi
            xmllint --noout --schema schemas/$version/$topel-schema.xsd "$filename" 2> /dev/null
            if [ $? -ne 0 ]; then
                echo $org_name $url_line >> validation-errors;
            fi
        fi
    done
done
# Prevent empty gist that won't be uploaded
echo "." >> xml-errors
echo "." >> validation-errors
