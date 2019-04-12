#!/bin/bash
# download schemas
versions=$(curl -s http://reference.iatistandard.org/201/codelists/downloads/clv3/csv/en/Version.csv | tail -n +2 | cut -d, -f1)
for version in $versions; do
    mkdir -p schemas/$version
    curl -s https://raw.githubusercontent.com/IATI/IATI-Schemas/version-$version/xml.xsd > schemas/$version/xml.xsd
    curl -s https://raw.githubusercontent.com/IATI/IATI-Schemas/version-$version/iati-common.xsd > schemas/$version/iati-common.xsd
    curl -s https://raw.githubusercontent.com/IATI/IATI-Schemas/version-$version/iati-activities-schema.xsd > schemas/$version/iati-activities-schema.xsd
    curl -s https://raw.githubusercontent.com/IATI/IATI-Schemas/version-$version/iati-organisations-schema.xsd > schemas/$version/iati-organisations-schema.xsd
done
