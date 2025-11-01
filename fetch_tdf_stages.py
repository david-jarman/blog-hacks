import asyncio, json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

BASE_URL = "https://www.letour.fr"
ROUTE_URL = f"{BASE_URL}/en/overall-route"

async def scrape():
    data = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        await page.goto(ROUTE_URL)
        await page.wait_for_selector("table")
        soup = BeautifulSoup(await page.content(), "html.parser")
        rows = soup.select("section.generalRace table tbody tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 6:
                continue
            stage_number = cells[0].get_text(strip=True)
            if not stage_number.isdigit():
                continue
            link_tag = cells[5].find("a")
            link = BASE_URL + link_tag["href"]
            stage = {
                "stage_number": stage_number,
                "type": cells[1].get_text(strip=True),
                "date": cells[2].get_text(strip=True),
                "start_finish": cells[3].get_text(strip=True),
                "distance": cells[4].get_text(strip=True),
                "details_url": link,
            }
            detail_page = await context.new_page()
            await detail_page.goto(link)
            await detail_page.wait_for_selector(".stageHeader__stage--main")
            d_soup = BeautifulSoup(await detail_page.content(), "html.parser")
            header = d_soup.select_one(".stageHeader__stage--main")
            details = {
                "date": header.select_one(".stageHeader__infos__date").get_text(strip=True),
                "route": header.select_one(".stageHeader__infos__route").get_text(strip=True),
            }
            for p_text in header.select(".stageHeader__length__text"):
                label = p_text.select_one(".stageHeader__length__label").get_text(strip=True)
                value = p_text.get_text(strip=True).replace(label, "").strip()
                details[label] = value
            mountains = []
            for item in d_soup.select("#mountain .mountain__infos"):
                name = item.select_one("h3").get_text(strip=True)
                km = item.select_one(".km").get_text(strip=True)
                percent = item.select_one(".percent")
                percent_text = percent.get_text(strip=True) if percent else ""
                category = item.select_one(".category")
                cat_text = category.get_text(strip=True) if category else ""
                mountains.append({"name": name, "km": km, "percent": percent_text, "category": cat_text})
            if mountains:
                details["mountain_passes"] = mountains
            stakes = d_soup.select_one("#stakes")
            if stakes:
                details["stakes_text"] = stakes.get_text(" ", strip=True)
            itinerary = d_soup.select_one("#itinerary")
            if itinerary:
                details["itinerary_text"] = itinerary.get_text(" ", strip=True)
            stage["details"] = details
            data.append(stage)
            await detail_page.close()
        await context.close()
        await browser.close()
    with open("tour_de_france_stages.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    asyncio.run(scrape())
