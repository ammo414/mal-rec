from jikanpy import Jikan
import requests
from bs4 import BeautifulSoup as bs
import re
from math import sqrt
from time import sleep

jikan = Jikan()


def watchlists(user, score):

    animelst = jikan.user(username = user, request = 'animelist')
    compcurr = {}

    for a in animelst['anime']:
        if a['watching_status'] <= 2 and a['score'] >= score:
            compcurr[a['title']] = [a['url'] + '/userrecs', a['score']]

    idlst = [a['mal_id'] for a in animelst['anime']]

    return compcurr, idlst


def recpull(compcurr, idlst):

    recs = {}
    recs2check = {1:7, 2:5, 3:3, 4:2, 5:2}

    lim = recs2check[len(str(len(compcurr)))]

    for x in compcurr:
        print('Pulling recs for', x)
        recstemp = []
        page = requests.get(compcurr[x][0])
        soup = bs(page.content, features = 'html.parser')
        temp = re.findall(r'https://myanimelist.net/anime/\d+/\w+"', str(soup))
        [recstemp.append(i) for i in temp if i not in recstemp]
        recstemp.pop(0)
        recstemp = recstemp[:lim]

        for y in recstemp:
            atitle = re.findall(r'/\w+', y)[3]
            atitle = re.sub(r'[^0-9a-zA-Z ]', '', atitle.replace('_', ' '))
            print('Evaluating', atitle)
            aid = int(re.findall(r'\d+', y)[0])

            if aid in idlst:
                print('        Already in MAL')

            else:
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

    return recs


def finallist(recs, compcurr):

    finallst = []
    scorethreshold = {1:6.9, 2:7.4, 3:7.9, 4:8.4, 5:8.9}
    st = scorethreshold[len(str(len(compcurr)))]
    urllst = [recs[x][2] for x in recs]

    for i, x in enumerate(recs):

        if recs[x][0] >= max(int(sqrt(len(compcurr))), 2):
            finallst.append((x, urllst[i], f'Recommended {recs[x][0]} times'))
        elif recs[x][1] >= st:
            finallst.append((x, urllst[i], f'Rating of {recs[x][1]}'))

    return finallst
