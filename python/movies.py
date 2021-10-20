import requests
import os
from simple_term_menu import TerminalMenu
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE, STDOUT
import multiprocessing
import shlex
from select import select

downloads_folder = './downloads'

# ----------------------------------------------------------------------------
# -- Source: BatFlix ---------------------------------------------------------
# ----------------------------------------------------------------------------

class BatFlix():
    def __init__(self):
        super().__init__()
        self.url = 'https://ww2.batflix.org'
    
    def get_page(self, name, media_type, year):
        query = name.replace(':', '').replace(' ', '-').replace('.', '').lower() + '-' + year
        full_url = self.url + '/' + media_type + 's/' + query
        req = requests.get(full_url)
        soup = BeautifulSoup(req.text, features="lxml")
        return soup

    def iframe_to_hls(self, iframe):
        req = requests.get(iframe)
        soup = BeautifulSoup(req.text, features="lxml")
        strings = soup.text.split('"')
        for s in strings: 
            if ('master.m3u8' in s): return s
        return None

    def get_episodes(self, show, episodes=None, season=None):
        result = []
        soup = self.get_page(show['name'], 'tvshow', show['year'])
        seasons = soup.findAll('li', {'itemprop':'containsSeason'})
        seasons.reverse()
        for i in range(0, len(seasons)):
            actual_season = int(seasons[i].find('span', {'itemprop':'name'}).text.replace('Season ', ''))
            for e in reversed(seasons[i].findAll('li', {'itemprop':'episode'})):
                number = e.find('meta', {'itemprop':'episodeNumber'}).attrs['content']
                iframe = e.find('a', {'class':'direct-stream'}).attrs['data-src']
                episodeString = 's{}e{}'.format(str(actual_season) if i >= 10 else '0' + str(actual_season), str(number) if int(number) >= 10 else '0' + str(number))
                newEpisode = { 'season': actual_season, 'number': number, 'name': episodeString }
                if (episodes == None and season != None and season == actual_season) or (season == None and episodes != None and episodeString in episodes):
                    newEpisode['url'] = self.iframe_to_hls(iframe)
                    result.append(newEpisode)
        return result

    def get_movie(self, movie):
        soup = self.get_page(movie['name'], 'movie', movie['year'])
        iframes = soup.find_all('iframe')
        iframe = iframes[0].attrs['src']
        result = {'name': '{}_({})'.format(movie['name'].replace(' ', '_'), str(movie['year'])), 'url': self.iframe_to_hls(iframe)}
        return result

b = BatFlix()

# ----------------------------------------------------------------------------
# -- Search TMDB api ---------------------------------------------------------
# ----------------------------------------------------------------------------

def search(query, max_results):
    results = []
    url = 'https://api.themoviedb.org/3'
    api_key = 'ff3fe82dec538fa2777cb85d3b2a0637'
    response = requests.get(url + '/search/multi', { 'api_key': api_key, 'query': query }).json()
    count = 0
    for result in response['results']:
        if (count == max_results): break
        media_type = result['media_type']
        if (media_type != 'movie' and media_type != 'tv'): continue
        is_movie = media_type == 'movie'
        item = {
            'name': result['title' if is_movie else 'name'],
            'media_type': media_type,
            'year': result['release_date' if is_movie else 'first_air_date'][0:4]
        }
        if (not is_movie):
            url = url + '/tv/' + str(result['id'])
            response = requests.get(url, {'api_key' : api_key}).json()
            if ('seasons' in response):
                item['seasons'] = response['seasons']
                for s in item['seasons']:
                    del s['overview'], s['poster_path'], s['id'], s['air_date']
                item['seasons'] = [x for x in item['seasons'] if x['season_number'] is not 0]
        results.append(item)
        count += 1
    return results

# ----------------------------------------------------------------------------
# -- Download ----------------------------------------------------------------
# ----------------------------------------------------------------------------

def download(videos):
    commands = ['python -m ffpb -i "{}" -c copy -bsf:a aac_adtstoasc "{}.mp4"'.format(video['url'], video['name']) for video in videos]
    execute(commands, 3)

def execute(commands, max_processes):
    timeout = 0.1 # seconds
    to_process = commands
    processes = []
    for i in range(0, max_processes):
        if not to_process: break
        command = to_process.pop(0)
        processes.append(Popen(shlex.split(command), stdout=PIPE))
    while processes:
        for p in processes[:]:
            if p.poll() is not None: # process ended
                print(p.stdout.read(), end='') # read the rest
                p.stdout.close()
                processes.remove(p)
                if (to_process):
                    command = to_process.pop(0)
                    processes.append(Popen(shlex.split(command), stdout=PIPE))
        # wait until there is something to read
        rlist = select([p.stdout for p in processes], [],[], timeout)[0]
        # read a line from each process that has output ready
        for f in rlist:
            print('\r' + f.readline(), end='') #NOTE: it can block

# ----------------------------------------------------------------------------
# -- Menu shit ---------------------------------------------------------------
# ----------------------------------------------------------------------------

def option_download_season(show):
    season = input('Season (1-'+str(len(show['seasons']))+'): ')
    if (season == ''): return select_result(show)
    episodes = b.get_episodes(show, season=int(season))
    download(episodes)

def option_download_episode(show):
    episode = input('Episode: ')
    if (episode == ''): return select_result(show)
    episodes = b.get_episodes(show, episodes=[episode])
    download(episodes)

def option_download_movie(movie):
    movie = b.get_movie(movie)
    download([movie])

def option_go_back(r): return

def select_result(result):
    menu = [{'name':'<< Back', 'callback':option_go_back}]
    if (result['media_type'] == 'movie'):
        menu.insert(0, {'name':'Download', 'callback':option_download_movie})
    else:
        menu.insert(0, {'name':'Download Episode', 'callback':option_download_episode})
        menu.insert(0, {'name':'Download Season', 'callback':option_download_season})
    terminal_menu = TerminalMenu(title='\n- '+result['name']+':\n', 
                menu_entries=[x['name'] for x in menu])
    os.system('clear')
    option = terminal_menu.show()
    menu[option]['callback'](result)

def parse_results(results):
    r = []
    for result in results:
        r.append(result['name'] + ' (' + result['year'] + ') (' + result['media_type'] + ')')
    return r

def show_results(results):
    while True:
        menu = parse_results(results)
        menu.append('<< Back')
        terminal_menu = TerminalMenu(title='\n- Resultados:\n', 
                menu_entries=menu)
        os.system('clear')
        option = terminal_menu.show()
        if (option == len(menu) - 1): break
        select_result(results[option])

# ----------------------------------------------------------------------------
# -- Main --------------------------------------------------------------------
# ----------------------------------------------------------------------------

def main():
    while True:
        os.system('clear')
        query = input('Busqueda: ')
        if (query.strip() == ''): break
        if (len(query) < 3): continue
        results = search(query, 5)
        if len(results) == 0:
            input('No se encontraron resultados.')
        else: 
            show_results(results)

main()