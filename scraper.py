# scraper.py
import asyncio
from playwright.async_api import async_playwright
import json

URL = "https://www.willhaben.at/iad/gebrauchtwagen/auto/gebrauchtwagenboerse?fromYear=1990&price-to=15000&VERKAEUFERART=PRIVAT"

seen_ads = set()

async def scrape_once():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL, wait_until="networkidle")

        try:
            await page.click('button:has-text("Alle akzeptieren")', timeout=5000)
        except:
            pass

        await page.wait_for_selector("article[data-testid='search-result-entry']", timeout=60000)
        cars = await page.query_selector_all("article[data-testid='search-result-entry']")
        results = []

        for car in cars:
            title = await car.query_selector("h2")
            title_text = await title.inner_text() if title else "N/A"

            link_elem = await car.query_selector("a")
            link = await link_elem.get_attribute("href") if link_elem else None

            if not link or link in seen_ads:
                continue

            seen_ads.add(link)

            price = await car.query_selector("div[data-testid='price']")
            price_text = await price.inner_text() if price else "N/A"

            image_elem = await car.query_selector("img")
            image_url = await image_elem.get_attribute("src") if image_elem else None

            results.append({
                "title": title_text.strip(),
                "price": price_text.strip(),
                "url": "https://www.willhaben.at" + link,
                "image": image_url,
                "phone": None
            })

        with open("oglasi.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        await browser.close()

# Ne pokreće se automatski
