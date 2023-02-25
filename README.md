# MILANO HOUSES' ANNOUNCEMENTS WEB SCRAPING 
### I craeted a dataset containing houses announcementes in Milano through web scraping

This repository contains the code I used to create the milano-housing dataframe, available in kaggle

I used **beautiful soup** to scrape the [Immobilare website](https://www.immobiliare.it/vendita-case/milano/?criterio=rilevanza), a house-announcement webpage. 

When the [immobiliare_scrapint.py](https://github.com/tommella90/milano-housing-price/blob/main/immobiliare_scraping.py) script runs, it automatically updates the dataframe with all the non already existing announcements. 

The [clean_data.py](https://github.com/tommella90/milano-housing-price/blob/main/clean_data.py) script cleans the data scraped and returns a zipped csv with a pandas 
dataframe inside. 

____________________________________
You can simply download the data. 
Alternatively, you can run the scripts: they scripts are made so that it automatically updates the dataframe with all the new annoucements. 
Over time, it will be possibile to perform time-series analysis. 


***How to use***:
____________________________________
## 1 GIT REPOSITORY

```
git clone https://github.com/tommella90/milano-housing-price/
```

```
pip install requirements.txt
```

```
python main.py
```

### 2 DOCKER IMAGE
Download this [docker image](https://hub.docker.com/repository/docker/tommella90/milano-housing/general) 
```
docker push tommella90/milano-housing:tagname
```

```
docker run -it tommella90/milano-housing:2
```

