#!/bin/bash
## Perform several validation tests on the files in a downloaded data snapshot

# Check for xml well formedness errors
rm -f xml-errors
for f in data/*/*; do
    echo "Checking XML: $f"
    # Check file is not empty
    if [[ -s $f ]]; then
        xmllint --noout $f 2> /dev/null
        if [ $? -ne 0 ]; then echo $f >> xml-errors; fi
    fi
done
# Prevent empty gist that won't be uploaded
echo "." >> xml-errors

echo "Downloading Schemas"
./download_schemas.sh

# Validate all the files against the relevant schema
rm -f validation-errors
for f in data/*/*; do
    echo "Validating: $f"
    if [[ -s $f ]]; then
        topel="`xmllint --xpath "name(/*)" "$f"`"
        version="`xmllint --xpath "string(/*/@version)" "$f"`"
        if [ "$version" == "1.01" ] || [ "$version" == "1" ] || [ "$version" == "1.0" ] || [ "$version" == "1.00" ]; then version="1.01"; fi
        xmllint --noout --schema schemas/$version/$topel-schema.xsd "$f" 2> /dev/null
        if [ $? -ne 0 ]; then echo $f >> validation-errors; fi
    fi
echo "." >> validation-errors
