import immobiliare_scraping as scraping
import clean_data as clean
import warnings
warnings.filterwarnings("ignore")

try:
    scraping.main()
except:
    "No new data to scrape. Try tomorrow"

clean.main()
