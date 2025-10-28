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

url = "https://www.ticketmaster.de/event/sombr-the-late-nights-and-young-romance-tour-europe-2026-tickets/599338472"

def get_trondheim_count(url: str) -> int | None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)   # oder .chromium
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")    # JS fertig?
        # Warten, bis die Checkbox im DOM ist
        #page.wait_for_selector("input[id='Trondheim']", timeout=10_000)

        soup = BeautifulSoup(page.content(), "html.parser")
        #print(soup.text)

        browser.close()


        m = re.search(r"Resale Tickets werden unten angezeigt, sobald sie verfügbar sind.", soup.get_text(" ", strip=True))

        return 0 if m else 1
def main() -> None:

    while True:
        tickets_avaliable = get_trondheim_count(url)

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{ts}: Check conducted")
        #requests.post("https://ntfy.sh/trondheim-alert", data= f"⚠️ Trondheim: {amount} Zimmer frei!")
        if tickets_avaliable == 1:
            requests.post("https://ntfy.sh/trondheim-alert", data= f"⚠️ Tickets gesichtet")
            print("Tickets Avaliable")
            time.sleep(1800)
        else:
            time.sleep(300)


if __name__ == "__main__":
    sys.exit(main())
