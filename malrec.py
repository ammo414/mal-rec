from jikanpy import Jikan
import requests
from bs4 import BeautifulSoup as bs
import re
from math import sqrt
from time import sleep

jikan = Jikan()


def watchlists(user, score):
    # create watch list of completed and currently watching anime to seed rec generation
    # user : MAL username
    # score : score threshold; only consider anime at or above score value when generating recs

    animelst = jikan.user(username = user, request = 'animelist')
    compcurr = {}

    for a in animelst['anime']:
        if a['watching_status'] <= 2 and a['score'] >= score:
            compcurr[a['title']] = [a['url'] + '/userrecs', a['score']]

    idlst = [a['mal_id'] for a in animelst['anime']]

    # compcurr: completed and currently watching anime list
    # idlst : list of MAL IDs for all anime in watchlist (includes dropped, plan to watch, on hold)
    return compcurr, idlst


def recpull(compcurr, idlst):
    # scrape recs from mal.net
    # records recs's score and how often its been recommended across compcurr list

    lim = max(3, 10 - round(sqrt(len(compcurr))))

    recs = {}
    for i, x in enumerate(compcurr):
        print('Pulling recs for', x, f'{i+1}/{len(compcurr)}')
        page = requests.get(compcurr[x][0])
        soup = bs(page.content, features = 'html.parser')
        recstemp = re.findall(r'https://myanimelist.net/anime/\d+/\w+"', str(soup))  # all recommended anime for x

        filtedrecs = []
        [filtedrecs.append(i) for i in recstemp if i not in filtedrecs and int(re.findall(r'\d+', i)[0]) not in idlst]
        filtedrecs = filtedrecs[:lim]  # filtered if already in filtedrecs or if already in MAL account

        for y in filtedrecs:
            atitle = re.findall(r'/\w+', y)[3]
            atitle = re.sub(r'[^0-9a-zA-Z ]', '', atitle.replace('_', ' '))
            print('Evaluating', atitle)

            aid = int(re.findall(r'\d+', y)[0])
            anime = jikan.anime(aid)

            if anime['title'] in recs:
                print(f'        Already evaluated { recs[anime["title"]][0]} times')
                recs[anime['title']][0] += 1
            elif anime['score'] >= 6.9:
                print('        Might recommend')
                recs[anime['title']] = [1, anime['score'], y]
            else:
                print('        Not recommend')
            sleep(2)

    # recs: dict of {anime title: [total number of times recommended, anime score, anime url]}
    return recs


def finallist(recs, compcurr):
    # filters recs one last time to find top recommendations based on score and frequency of recommendation

    finallst = []
    scorethreshold = 6.4 + 0.5*len(str(len(compcurr)))
    urllst = [recs[x][2] for x in recs]

    for i, x in enumerate(recs):
        
        if recs[x][0] >= max(round(sqrt(len(compcurr))), 2):
            finallst.append((x, urllst[i], f'Recommended {recs[x][0]} times'))
            # if x was recommended at least a certain number of times, it'll be recommended
        elif recs[x][1] >= scorethreshold:
            finallst.append((x, urllst[i], f'Score of {recs[x][1]}'))
            # if x's score is above a threshold, it'll be recommended

    return finallst
