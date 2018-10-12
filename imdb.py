import json
import requests
from bs4 import BeautifulSoup as bs
from datetime import date
from dateutil import parser


class IMDB_API:
    def __init__(self):
        self.today = date.today()
        self.suggest_api_endpoint = 'http://sg.media-imdb.com/suggests/{}/{}.json'
        self.adv_search_url = 'https://www.imdb.com/search/title?title={}&title_type=tv_series'
        self.episode_lst_url = 'https://www.imdb.com/title/%s/episodes?season=999'

    def id_search_fallback(self, show_name):
        """
        This is a fallback function which scrapes title id for the most popular match of
        given keyword.
        :param show_name:
        :return: IMDB title id as string
        """
        r = requests.get(self.adv_search_url.format(show_name))
        soup = bs(r.text, features="lxml")
        try:
            id = soup.find('h3', class_='lister-item-header').a['href'].split('/')[2]
            return id
        except (AttributeError, KeyError):
            return False

    def id_search(self, show_name):
        """
        This function uses imdb's suggest api,which returns best suggestions based on
        keyword as json,its faster than scraping webpage for title id.
        :param show_name:
        :return: IMDB title id as string
        """

        try:
            r = requests.get(self.suggest_api_endpoint.format(show_name[0], show_name))
            r.raise_for_status()
            jtext = r.text[r.text.index('{'):-1]
            jdata = json.loads(jtext, encoding='utf-8')
            for i in jdata.get('d'):
                if i.get('q', None) == 'TV series':
                    return i['id']

        except (json.JSONDecodeError, requests.exceptions.HTTPError):
            return self.id_search_fallback(show_name)  # fallback to slower function

        return self.id_search_fallback(show_name)

    def getnextepisode(self, series_name):
        """
        :param series_name: Tv series name string
        :return: String to be emailed informing about given show's next episode.
        """
        next_episode = "No Date/Year is available for next episode/season. "
        id = self.id_search(series_name)
        if id:
            r = requests.get(self.episode_lst_url % id)
            soup = bs(r.text, features="lxml")
            start_year, end_year = soup.find_all('span', class_='nobr')[0].text.strip()[1:-1].replace("\u2013",
                                                                                                      "-").split("-")
            if (end_year.strip()):
                return "The show has finished streaming all its episodes."
            all_epi_dates = [i.text.strip() if len(i.text.strip()) < 5 else parser.parse(i.text.strip()).date() for i in
                             soup.find_all('div', class_='airdate')]
            all_epi_dates = list(filter(None, all_epi_dates))
            for date in all_epi_dates:
                if isinstance(date, type(self.today)):
                    if date >= self.today:
                        next_episode = f"Next episode airs on {date.isoformat()}"
                        break
                else:
                    next_episode = f"The next season begins in {date}"
                    break

        return next_episode
