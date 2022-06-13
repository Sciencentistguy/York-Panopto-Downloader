from selenium import webdriver

import time
import json
import os
import requests
import subprocess
import pprint

from selenium.webdriver.remote.webelement import WebElement


urls = []

driver = webdriver.Chrome(
    executable_path=DRIVER_PATH,
)

driver.get(
    "https://york.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#maxResults=1000&sortColumn=1&sortAscending=true"
)

elem = driver.find_elements_by_id("loginButton")[0]
elem.click()
elem = driver.find_elements_by_id("loginControl_externalLoginButton")[0]
elem.click()
time.sleep(1)
elem = driver.find_elements_by_id("user_id")[0]
elem.click()
elem.send_keys(PANOPTO_USERNAME)
elem = driver.find_elements_by_id("password")[0]
elem.click()
elem.send_keys(PANOPTO_PASSWORD)
elem = driver.find_elements_by_id("entry-login")[0]
elem.click()

time.sleep(5)

tables = driver.find_elements_by_class_name("content-table-list")

table = tables[0]

print(table.find_elements_by_class_name("list-title"))

for row in table.find_elements_by_css_selector("tr"):
    for cell in row.find_elements_by_tag_name("td"):
        cell: WebElement
        if cell.get_attribute("class") == "detail-cell":
            div = cell.find_elements_by_class_name("title-link")[0]
            a: WebElement = div.find_elements_by_tag_name("a")[0]
            href = a.get_attribute("href")
            text = a.find_elements_by_tag_name("span")[0].text

            urls.append((text, href))
#  driver.close()

driver.quit()

with open("downloader.log", "w") as f:
    f.write(str(urls))

for (name, url) in urls:
    print(f"{name}\n{url}\n")
    deliveryId = url.split("=")[1]

    ### SEE README
    response = None

    j = response.json()
    streams = j["Delivery"]["Streams"]

    pprint.pp(j)

    if streams[0]["StreamUrl"] is None:
        streams = j["Delivery"]["PodcastStreams"]
    for stream in streams:
        url = stream["StreamUrl"]
        tipe = stream["StreamType"]
        print(f"m3u8 url for stream type {tipe} is {url}")
        output_filename = f"{name} - Stream {tipe:02}.mkv".replace("/", "_")
        cmd = [
            "ffmpeg",
            "-protocol_whitelist",
            "file,http,https,tcp,tls,crypto",
            "-i",
            url,
            "-c",
            "copy",
            output_filename,
        ]

        if not os.path.exists(output_filename):
            subprocess.run(cmd)
