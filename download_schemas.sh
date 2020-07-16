#!/bin/bash
# download schemas
versions=$(curl -sL http://reference.iatistandard.org/201/codelists/downloads/clv3/csv/en/Version.csv | tail -n +2 | cut -d, -f1)
for version in $versions; do
    mkdir -p schemas/$version
    curl -sL https://raw.githubusercontent.com/IATI/IATI-Schemas/version-$version/xml.xsd > schemas/$version/xml.xsd
    xmllint --noout schemas/$version/xml.xsd 2> /dev/null || exit $?
    curl -sL https://raw.githubusercontent.com/IATI/IATI-Schemas/version-$version/iati-common.xsd > schemas/$version/iati-common.xsd
    xmllint --noout schemas/$version/iati-common.xsd 2> /dev/null || exit $?
    curl -sL https://raw.githubusercontent.com/IATI/IATI-Schemas/version-$version/iati-activities-schema.xsd > schemas/$version/iati-activities-schema.xsd
    xmllint --noout schemas/$version/iati-activities-schema.xsd 2> /dev/null || exit $?
    curl -sL https://raw.githubusercontent.com/IATI/IATI-Schemas/version-$version/iati-organisations-schema.xsd > schemas/$version/iati-organisations-schema.xsd
    xmllint --noout schemas/$version/iati-organisations-schema.xsd 2> /dev/null || exit $?
done
