#!/bin/bash
## Perform several validation tests on the files in a downloaded data snapshot

IFS=$'\n'

echo "Downloading Schemas"
./download_schemas.sh || exit $?

# Check for xml well formedness errors
rm -f xml-errors validation-errors

FILES=urls/*
for f in $FILES; do
    for url_line in `cat $f`; do
        org_name=`basename $f`
        package_name=`echo $url_line | sed 's/ .*$//'`
        filename="data/$org_name/$package_name.xml"
        # Hack to ignore package "usaid-multiple-3"
        if [[ "$package_name" == "usaid-multiple-3" ]]; then
            continue
        fi
        # Check file is not empty
        if [[ -s $filename ]]; then
            echo "Checking XML: $package_name"
            xmllint --noout $filename 2> /dev/null
            if [ $? -ne 0 ]; then
                echo $org_name $url_line >> xml-errors;
                continue
            fi

            echo "Validating: $package_name"
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
