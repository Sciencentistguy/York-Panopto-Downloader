A python script to download every item you have access to on Panopto

Designed for use at the University of York

## Dependencies

- `ffmpeg`
- `chrom(e|ium)`
- `selenium`
- `chromedriver`
- `requests`

## Usage

Before use, this script must be modified somewhat, as it requires secrets.

First, the variables `DRIVER_PATH`, `PANOPTO_USERNAME` and `PANOPTO_PASSWORD` must be defined.

Second, the request code must be inserted. This is unique to your account, and uses session IDs and tokens that I could not reverse engineer.

My solution to this was to use firefox's "Copy as cURL" feature:

1. Load up any panopto player page, and open fireox's dev tools.
2. Select the network tab, and reload the page.
3. Once it has finished reloading, locate the `POST` request (there should only be one).
4. Right click on this request, and select "Copy -> Copy as cURL". This will copy a cURL command to your clipboard.
5. Convert this cURL command to the appropriate python code. I used https://curlconverter.com/ to do this.
6. Insert this code in download.py, replacing the line `response = None`
7. Run `python downloader.py`
8. Chrome will open, then it will close, then wait as ffmpeg downloads the files.

Note that if you have access to more than 1000 items on Panopto this script will only download the first 1000. To fix this, increase the `maxResults` parameter to the panopto url.

## Use with other institutions

I am unable to test this for other institutions that use panopto, but it should work with a little modification.

---

Available under the terms of version 2.0 of the Mozilla Public Licence
