from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import sys

# get n of seasons
# https://imdb-api.com/API/Title/{api_key}/{series_id}

# get season episodes (with ratings)
# https://imdb-api.com/API/SeasonEpisodes/{api_key}/{series_id}/{season_number}

browser = webdriver.Chrome()

def get_n_of_seasons(series_id):
    url = f"https://www.imdb.com/title/{series_id}/episodes"
    browser.get(url)
    selector = browser.find_element(By.ID, "bySeason")
    options = selector.find_elements(By.TAG_NAME, "option")
    return len(options)

def get_url(series_id, season):
    url = f"https://www.imdb.com/title/{series_id}/"
    return url + f"episodes?season={season}"

def get_season_ratings(series_id, season):
    browser.get(get_url(series_id, season))
    episode_list = browser.find_elements(By.CLASS_NAME, "ipl-rating-star__rating")

    ratings = []
    i = 0
    while i < len(episode_list):
        val = episode_list[i].get_attribute("innerHTML")
        if len(val) == 3 and val[1] == ".":
            ratings.append(float(val))
        i += 23            
    return ratings

if __name__ == "__main__":
    series_id = sys.argv[1]
    p = os.getcwd() + "/" + series_id + ".json"
    if not os.path.exists(p):
        seasons = []
        for season in range(1, get_n_of_seasons(series_id)+1):
            rat = get_season_ratings(series_id, season)
            seasons.append(rat)
            print("S" + str(season) + " " + str(rat))
        
        to_save = "{" + f'"data": {seasons}' + "}"

        f = open(series_id + ".json", "a")
        f.write(to_save)
        f.close()
    else:
        print("Series already stored!")

