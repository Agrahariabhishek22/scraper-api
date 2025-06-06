from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_events():
    Title, Date_Time, Venue, Price, Link, Images = [], [], [], [], [], []

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.eventbrite.com.au/d/australia--sydney/events/")
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "lxml")

    tit = soup.find_all("h3", class_="Typography_body-lg__487rx")
    for i in tit: Title.append(i.text.strip())

    date = soup.find_all("div", class_="Stack_root__1ksk7")
    for dat in date:
        d = dat.find("p", class_="Typography_root__487rx #3a3247 Typography_body-md-bold__487rx Typography_align-match-parent__487rx")
        Date_Time.append(d.get_text(strip=True) if d else "N/A")

    venue = soup.find_all("div", class_="Stack_root__1ksk7")
    for ven in venue:
        v = ven.find("p", class_="Typography_root__487rx #585163 Typography_body-md__487rx event-card__clamp-line--one Typography_align-match-parent__487rx")
        Venue.append(v.get_text(strip=True) if v else "Online")

    price_blocks = soup.find_all("div", class_="DiscoverVerticalEventCard-module__priceWrapper___usWo6")
    for pr in price_blocks:
        p = pr.find("p", class_="Typography_root__487rx #3a3247 Typography_body-md-bold__487rx Typography_align-match-parent__487rx")
        Price.append(p.text.strip() if p else "N/A")

    ln_blocks = soup.find_all("div", class_="event-card__vertical")
    for block in ln_blocks:
        ln = block.find("a", rel="noopener")
        Link.append(ln.get("href") if ln else "")

    img_blocks = soup.find_all("div", attrs={"data-testid": "event-card-image-container"})
    for img in img_blocks:
        im = img.find("img", class_="event-card-image")
        Images.append(im.get("src") if im else "")

    driver.quit()

    scraped_data = []
    for i in range(min(len(Title), len(Date_Time), len(Venue), len(Price), len(Link), len(Images))):
        scraped_data.append({
            "title": Title[i],
            "date_time": Date_Time[i],
            "venue": Venue[i],
            "price": Price[i],
            "link": Link[i],
            "image": Images[i]
        })

    return scraped_data
