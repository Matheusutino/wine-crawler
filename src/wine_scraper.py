import time
import requests
from bs4 import BeautifulSoup
from src.utils import save_json, load_json

class WineScraper:
    """Class to scrape wine details from 'vinhosevinhos.com'."""

    BASE_URL = "https://www.vinhosevinhos.com/vinhos.html?p="
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    SAVE_FILE_PROGRESS = "data/wine_progress.json"
    SAVE_FILE_DATA = "data/wine_data.json"

    def __init__(self, delay=1):
        """
        Initializes the scraper with a configurable delay between requests.

        Args:
            delay (int): Time in seconds to wait between requests.
        """
        self.delay = delay
        self.progress = load_json(self.SAVE_FILE_PROGRESS) or {"start_page": 1, "last_saved_index": 0}
        self.all_data = load_json(self.SAVE_FILE_DATA) or []
        self.start_page = self.progress["start_page"]
        self.last_saved_index = self.progress["last_saved_index"]

    @staticmethod
    def extract_wine_details(url, soup):
        """Extracts wine details from the provided BeautifulSoup object."""
        def get_text(div_class, prefix=""):
            element = soup.find("div", class_=f"item {div_class}")
            return element.text.strip().replace(prefix, "").strip() if element else None

        return {
            "Name": soup.find("span", class_="base").text.strip() if soup.find("span", class_="base") else None,
            "URL Product": url,
            "Sku": soup.find("div", {'itemprop': 'sku'}).text.strip() if soup.find('div', {'itemprop': 'sku'}) else None,
            "Image": soup.find('img', {'class': 'img-fluid'})['src'] if soup.find('img', {'class': 'img-fluid'}) else None,
            "Num Reviews": soup.find("span", {'itemprop': 'reviewCount'}).text.strip() if soup.find('span', {'itemprop': 'reviewCount'}) else "0",
            "Grape": get_text("uva", "Uva:"),
            "Type": get_text("tipo", "Tipo:"),
            "Alcoholic Degree": get_text("graduacao", "Graduação alcoólica:"),
            "Harvest": get_text("safra", "Safra:"),
            "Region": get_text("regiao", "Região:"),
            "Winery": get_text("vinicola", "Vinícola:"),
            "Vineyard": get_text("vinhedo", "Vinhedo:"),
            "Wine Class": get_text("classe", "Classe:"),
            "Classification": get_text("classificacao", "Classificação:"),
            "Volume": get_text("volume", "Volume:"),
            "Maturation": get_text("amadurecimento", "Amadurecimento:"),
            "Temperature": get_text("temperatura", "Temperatura:"),
            "Storage Potential": get_text("tempoguarda", "Potencial de guarda:"),
            "Visual": get_text("visual", "Visual:"),
            "Olfaction": get_text("olfato", "Olfato:"),
            "Palate": get_text("paladar", "Paladar:"),
            "Pairing": get_text("harmonizacao", "Harmonização:"),
            "Closure": get_text("fechamento", "Fechamento:"),
            "Price": soup.find("span", class_="price").text.strip() if soup.find("span", class_="price") else None,
            "Description": soup.find("div", class_="data item content").text.strip() if soup.find("div", class_="data item content") else None
        }

    def save_progress(self, page_number, last_saved_index):
        """Saves the current progress to a JSON file."""
        progress = {"start_page": page_number, "last_saved_index": last_saved_index}
        save_json(progress, self.SAVE_FILE_PROGRESS)

    def save_data(self):
        """Saves the scraped data to a separate JSON file."""
        save_json(self.all_data, self.SAVE_FILE_DATA)

    def scrape_page(self, page_number):
        """Scrapes a single page of the wine list."""
        url = f"{self.BASE_URL}{page_number}"
        response = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find("div", class_="message info empty"):
            return False  # Page is empty

        product_links = soup.find_all("a", class_="product-item-link")
        for idx, link in enumerate(product_links[self.last_saved_index:-1], start=self.last_saved_index):
            url_product = link['href']
            wine_page = requests.get(url_product, headers=self.HEADERS)
            wine_soup = BeautifulSoup(wine_page.text, "html.parser")
            wine_data = self.extract_wine_details(url_product, wine_soup)
            self.all_data.append(wine_data)
            self.save_progress(page_number, idx + 1)  # Save progress
            self.save_data()
            time.sleep(self.delay)

        self.last_saved_index = 0  # Reset for the next page
        return True  # Page has data

    def scrape_all_pages(self):
        """Scrapes all pages until an empty page is encountered."""
        page_number = self.start_page
        while self.scrape_page(page_number):
            print(f"Scraped page {page_number}.")
            page_number += 1
        print("Scraping completed.")
        return self.all_data