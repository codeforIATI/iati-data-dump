#!/bin/bash
## Perform several validation tests on the files in a downloaded data snapshot

# Check for xml well formedness errors
for f in data/*/*; do
    # Check file is not empty
    if [[ -s $f ]]; then
        xmllint $f > /dev/null
    fi
done 2> xmlerrors
# Prevent empty gist that won't be uploaded
echo "." >> xml-errors

./download_schemas.sh

# Validate all the files against the relevant schema
for f in data/*/*; do
    if [[ -s $f ]]; then
        echo $f;
    fi
done > list
for f in data/*/*; do
    if [[ -s $f ]]; then
        topel="`xmllint --xpath "name(/*)" "$f"`"
        version="`xmllint --xpath "string(/*/@version)" "$f"`"
        if [ "$version" == "1.01" ] || [ "$version" == "1" ] || [ "$version" == "1.0" ] || [ "$version" == "1.00" ]; then version="1.01";
        elif [ "$version" == "1.02" ]; then version="1.02";
        else version="1.03"; fi
        if [ "$topel" == "iati-activities" ]; then
            xmllint --schema schemas/$version/iati-activities-schema.xsd --noout "$f" 2> /dev/null
            if [ $? -eq 0 ]; then echo $f; fi
        elif [ "$topel" == "iati-organisations" ]; then
            xmllint --schema schemas/$version/iati-organisations-schema.xsd --noout "$f" 2> /dev/null
            if [ $? -eq 0 ]; then echo $f; fi
        fi
    fi
done > list-validate
comm -23 list list-validate > validation-errors
echo "." >> validation-errors
