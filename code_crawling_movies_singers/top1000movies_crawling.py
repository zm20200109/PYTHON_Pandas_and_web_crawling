import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

start_url = "https://www.imdb.com/list/ls006266261/"
chromedriver_location = r"C:\Users\Korisnik\miniconda3\Scripts\chromedriver.exe"

def get_soup_from_selenium(start_url):
    service = Service(chromedriver_location)
    driver = webdriver.Chrome()
    driver.get(start_url)
    return BeautifulSoup(driver.page_source, features='html.parser')


#soup = get_soup_from_selenium(start_url)
#print(soup.text)

def get_next_page(start_url,page=1):
    if page>1:
        return start_url+"?sort=list_order,asc&st_dt=&mode=detail&page="+str(page)
    else:
        return start_url

#page_3 = get_next_page(start_url,3)
#print(page_3)

def get_soup_from_page(start_url, page):
    return get_soup_from_selenium(get_next_page(start_url,page))

soup1 = get_soup_from_page(start_url,1)
print(soup1.text)
#%%
def get_info_from_soup(soup):
    # (rb, title, godina, zanrovi, imdb skor, metaskor, minutaza, kratak opis)
    movies = soup.find_all('div',attrs={'class':'lister-item mode-detail'})
    result_list = list()
    #print(len(movies))
    for movie in movies[:]:
        content =movie.find_next('div',attrs={'class':'lister-item-content'})
        #print(content)
        rank = content.h3.span.text.split(".")[0] #RANK!!!
        #print(rank)
        title = content.h3.a.text # Title !!!
        #print(title)
        year_released = content.h3.find_next('span',attrs={'class':'lister-item-year text-muted unbold'}).text.rstrip(")").lstrip("(")
        #print(year_released)
        runtime = content.find_next('p',attrs={'class':'text-muted text-small'}).find_next('span',attrs={'class':'runtime'}).text.split(" ")[0]
        #print(runtime)
        genres = content.find_next('p',attrs={'class':'text-muted text-small'}).find_next('span',attrs={'class':'genre'}).text.strip()
        #print(genres)
        imdb_rating = content.find_next('div',attrs={'class':'ipl-rating-widget'}).find_next('div',attrs={'class':'ipl-rating-star small'}).find_next('span',attrs={'class':'ipl-rating-star__rating'}).text
        #print(imdb_rating)

        metasc_base = content.find_next('div', attrs={'class':'inline-block ratings-metascore'})
        if metasc_base.find_next('span',attrs={'class':'metascore favorable'}) !=None:
            meta = metasc_base.find_next('span',attrs={'class':'metascore favorable'}).text.strip()
        elif metasc_base.find_next('span',attrs={'class':'metascore mixed'})!=None:
            meta = metasc_base.find_next('span',attrs={'class':'metascore mixed'})
        else:
            meta = metasc_base.find_next('span',attrs={'class':'metascore unfavorable'})
        description = content.find_next('p',attrs={'class':''}).text.strip(r"\n")
        #print(description)
        print(rank, title, genres, imdb_rating, meta, runtime,description)
        result_list.append((rank, title, genres, imdb_rating, meta, runtime,description))
    return result_list
#%%
soup3 = get_soup_from_selenium(get_next_page(start_url,5))
list_soup3 = get_info_from_soup(soup3)
for elem in list_soup3:
    print(elem)
#%%
# genericka metoda koja izvlaci supe do maksimalne stranice.

def crawl(start_url, max_page):
    for page in range(max_page): # ovo ide od 0 do max_page - 1
        yield get_soup_from_page(start_url,page+1)

def get_movies_info_list(start_url, max_page):
    soups = crawl(start_url, max_page)
    res_list = []
    while True:
        try:
            soup = next(soups)
            list_supl = get_info_from_soup(soup)
            for elem in list_supl:
                res_list.append(elem)
        except StopIteration:
            break
    return res_list

#%%
list_of_movies = get_movies_info_list(start_url, 10)
#%%
df_movies = pd.DataFrame(list_of_movies, columns=['Rank','Title','Genre','IMDB_Rating', 'Metascore','Duration','Siege'])
df_movies['IMDB_Rating']=pd.to_numeric(df_movies['IMDB_Rating'], errors='coerce')
ninety_percent_quantile = df_movies['IMDB_Rating'].quantile(0.9)
top_ratings_df=df_movies.loc[df_movies['IMDB_Rating']>ninety_percent_quantile]
print(top_ratings_df)
#%%
def write_to_csv(list_of_movies):
    from pathlib import Path
    import csv
    from sys import stderr
    try:
        with open(Path.cwd()/'../data/movies/imdb_top_1000_result.csv', 'w') as fobject:
            csv_writer = csv.writer(fobject)
            csv_writer.writerow(('Rank','Title','Genre','IMDB_Rating', 'Metascore','Duration','Siege'))
            for elem in list_of_movies:
                csv_writer.writerows(elem)
    except OSError as err:
        stderr.write(f"{err}")

write_to_csv(list_of_movies)
#%%
soups = crawl(start_url,2)
while True:
    try:
        print(next(soups))
    except StopIteration:
        break


#%%
list_of_values = get_info_from_soup(soup1)
for el in list_of_values:
    print(el)
import pandas as pd
#%%
movies = pd.DataFrame(list_of_values, columns=['Rank','Title','Genres','IMDB_Rating','Metascore','Runtime','Description'])
print(movies)