from glob import glob
from random import random
import os
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--random", help="Play random episode")
parser.add_argument("-e", "--episode", help="Play specific episode (format: s(season)e(episode))")
parser.add_argument("-s", "--set", help="Set actual episode (format: s(season)e(episode))")
args = parser.parse_args()

folder = '/Users/faustofusse/Documents/Movies/HIMYM'
pickleFile = '/Users/faustofusse/Documents/Software/scripts/python/himym.pickle'
# folder = '/Users/faustofusse/Documents/Movies/How I Met Your Mother (2005)'

actual = pickle.load(open(pickleFile, 'rb'))

season_dirs = glob(folder+'/*/')
season_dirs.sort()

def r(min, max):
    return int(min + (random() * (max - min)))

def play_random():
    season = season_dirs[r(0,len(season_dirs))]
    episodes = glob(season+'*') # +'*.mp4'
    episode = episodes[r(0,len(episodes))]
    episode = episode.replace(' ', '\ ').replace('(', '\(').replace(')','\)')
    os.system('open ' + episode)

def get_episode_number(episode):
    return int(episode.rsplit('x')[-1].rsplit(')')[0])

def play_next():
    season = actual['season']
    episode = actual['episode']
    season_dir = season_dirs[season - 1]
    episode_files = glob(season_dir+'*') # +'*.mp4'
    if (episode == len(episode_files)):
        episode = 1
        season = season + 1 if season is not len(season_dirs) else 1
        season_dir = season_dirs[season - 1]
        episode_files = glob(season_dir+'*') # +'*.mp4'
    else:
        episode += 1
    episode_files.sort(key=get_episode_number)
    episode_file = episode_files[episode - 1]
    episode_file = episode_file.replace(' ', '\ ').replace('(', '\(').replace(')','\)')
    pickle.dump({'season': season, 'episode': episode}, open(pickleFile, 'wb'))
    print(episode_file)
    os.system('open ' + episode_file)

def find_episode(episodes, episode):
    for e in episodes:
        if get_episode_number(e) == episode: return e

def play_episode(e):
    season = int(e[1] + e[2])
    episode = int(e[4] + e[5])
    season_dir = season_dirs[season - 1]
    episode_files = glob(season_dir+'*') # +'*.mp4'
    episode_file = find_episode(episode_files, episode)
    episode_file = episode_file.replace(' ', '\ ').replace('(', '\(').replace(')','\)')
    os.system('open ' + episode_file)

def set_episode(e):
    season = int(e[1] + e[2])
    episode = int(e[4] + e[5])
    pickle.dump({'season': season, 'episode': episode}, open(pickleFile, 'wb'))

def main():
    if (args.random): play_random()
    elif (args.episode): play_episode(args.episode)
    elif (args.set): set_episode(args.set)
    else: play_next()

main()
