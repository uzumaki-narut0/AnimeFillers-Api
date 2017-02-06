import urllib.request
from bs4 import BeautifulSoup
from flask import Flask, request
from flask_restful import Resource, Api
from pprint import pprint
import os

app = Flask(__name__)
api = Api(app)


base_url = 'http://www.animefillerlist.com'
page = urllib.request.urlopen(base_url + "/shows")
soup = BeautifulSoup(page,'html.parser')
root = soup.findAll('div', attrs = {"id":"ShowList"})
'''
Extracting all anime Urls and appending them in anime_links[]
'''
anime_links = []
for link in root[0].find_all('a'):
    anime_links.append(base_url + link.get('href'))
#print(anime_links[1])


'''
Visiting urls one by one
and creating api
'''
anime_list = []
i = 0
for link in anime_links:
    anime_page = urllib.request.urlopen(link)
    anime_soup = BeautifulSoup(anime_page,'html.parser')
    anime_name = anime_soup.find('h1').string
    anime_list.append({"anime_name":anime_name,"fillers_list":[]})
    episode_list = anime_soup.find('table', attrs = {"class":"EpisodeList"})
    #now we got episodes list, start appending them to dictionary
    #print(episode_list)
    if not episode_list:
        continue
    filler_list_odd = episode_list.findAll('tr',attrs = {"class":"filler odd"})
    filler_list_even = episode_list.findAll('tr',attrs = {"class":"filler even"})
    print(filler_list_even)
    
   # print(episode_row_data.string)
    
    for episode in filler_list_even:
        episode_name = episode.find('td',attrs = {"class":"Title"})
        episode_no = episode.find('td',attrs = {"class":"Number active"})
        episode_air_date = episode.find('td',attrs = {"class":"Date"})
        anime_list[i]["fillers_list"].append({"name":episode_name.string,"episode_no":episode_no.string,"air_date":episode_air_date.string})
    for episode in filler_list_odd:
        episode_name = episode.find('td',attrs = {"class":"Title"})
        episode_no = episode.find('td',attrs = {"class":"Number active"})
        episode_air_date = episode.find('td',attrs = {"class":"Date"})
        anime_list[i]["fillers_list"].append({"name":episode_name.string,"episode_no":episode_no.string,"air_date":episode_air_date.string})
    i += 1
    '''
    if i == 20:
        break
        '''
    
class AnimeFillersApi(Resource):
    def get(self):
        return {"result": anime_list}
    

api.add_resource(AnimeFillersApi, '/')

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
