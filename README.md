## IATI Data Dump

#### A daily snapshot of all IATI data (and metadata) on the IATI registry.

 * [Download all IATI data](https://www.dropbox.com/s/kkm80yjihyalwes/iati_data.zip?dl=1)
 * [View on dropbox](https://www.dropbox.com/sh/iddx793xw47fwb0/AADwQBNWyCvQhh1E89a4XW7da?dl=0&lst=)

#### Rationale

Lots of IATI products do a daily pull of all IATI XML data. That involves downloading gigabytes of data, via thousands of HTTP requests. So it’s quite slow.

Downloading a single archive file is significantly faster. That’s available here!

#### How does this work?

We perform a daily fetch of all IATI data, compress it, and put the archive onto [dropbox](https://www.dropbox.com). There’s a timestamp on dropbox that lets you know how fresh the data is.

[This github gist](https://gist.github.com/codeforIATIbot/f117c9be138aa94c9762d57affc51a64) is updated with the list of erroring datasets.

#### Acknowledgements

The code relies heavily on [IATI Registry Refresher](https://github.com/IATI/IATI-Registry-Refresher), made by [@caprenter](https://github.com/caprenter) and [@Bjwebb](https://github.com/Bjwebb).
