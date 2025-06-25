#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from playwright.sync_api import sync_playwright
import re

url = "https://bolig.sit.no/en/"

def get_trondheim_count(url: str) -> int | None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)   # oder .chromium
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")    # JS fertig?
        # Warten, bis die Checkbox im DOM ist
        #page.wait_for_selector("input[id='Trondheim']", timeout=10_000)

        soup = BeautifulSoup(page.content(), "html.parser")

        browser.close()


        m = re.search(r"Trondheim\s*\(\s*(\d+)\s*\)", soup.get_text(" ", strip=True))
        return int(m.group(1)) if m else None
def main() -> None:

    while True:
        amount = get_trondheim_count(url)

        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"{ts}: {amount}")
        #requests.post("https://ntfy.sh/trondheim-alert", data= f"⚠️ Trondheim: {amount} Zimmer frei!")
        if amount != 0:
            requests.post("https://ntfy.sh/trondheim-alert", data= f"⚠️ Trondheim: {amount} Zimmer frei!")
            print("x")
            time.sleep(1800)
        else:
            time.sleep(300)


if __name__ == "__main__":
    sys.exit(main())
