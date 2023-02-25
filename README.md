# MILANO HOUSES' ANNOUNCEMENTS WEB SCRAPING 
### I craeted a dataset containing houses announcementes in Milano through web scraping

This repository contains the code I used to create the milano-housing dataframe, available in kaggle

I used **beautiful soup** to scrape the [Immobilare website](https://www.immobiliare.it/vendita-case/milano/?criterio=rilevanza), a house-announcement webpage. 

When the [immobiliare_scrapint.py](https://github.com/tommella90/milano-housing-price/blob/main/immobiliare_scraping.py) script runs, it automatically updates the dataframe with all the non already existing announcements. 

The [clean_data.py](https://github.com/tommella90/milano-housing-price/blob/main/clean_data.py) script cleans the data scraped and returns a zipped csv with a pandas 
dataframe inside. 

Tu use it: 

```
git clone https://github.com/tommella90/milano-housing-price/
```

```
pip install requirements.txt
```

```
python main.py
```

Alternatively, you can use this [docker image](https://hub.docker.com/repository/docker/tommella90/milano-housing/general) 
