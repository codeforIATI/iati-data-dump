## IATI Data Dump

#### A daily snapshot of all IATI data (and metadata) on the IATI registry.

[Download all IATI data](https://iati-data-dump.codeforiati.org/)

#### Rationale

Lots of IATI products do a daily pull of all IATI XML data. That involves downloading gigabytes of data, via thousands of HTTP requests. So it’s quite slow.

Downloading a single archive file is significantly faster. That’s available here!

#### How does this work?

We perform a daily fetch of all IATI data, compress it, and uploads the archive. There’s a metadata.json file inside the zip, that lets you know how fresh the data is.

[This github gist](https://gist.github.com/codeforIATIbot/f117c9be138aa94c9762d57affc51a64) is updated with the list of erroring datasets.

#### Acknowledgements

The original code relied heavily on [IATI Registry Refresher](https://github.com/IATI/IATI-Registry-Refresher), made by [@caprenter](https://github.com/caprenter) and [@Bjwebb](https://github.com/Bjwebb).

The new, much faster code was contributed by [@notshi](https://github.com/notshi) and [@xriss](https://github.com/xriss).
