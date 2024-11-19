from src.wine_scraper import WineScraper

if __name__ == "__main__":
    # Inicialize o scraper com um delay de 20 segundos entre cada requisição, seguindo o robots.txt
    scraper = WineScraper(delay=20)
    
    try:
        # Comece a scraping a partir do progresso salvo
        scraper.scrape_all_pages()
        
        print("All wine data scraped and saved successfully!")

    except Exception as e:
        # Se ocorrer um erro, mostre uma mensagem
        print(f"An error occurred: {e}")
        print("Progress saved. You can restart the scraper to resume.")
