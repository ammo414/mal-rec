from jikanpy import Jikan
import re

jikan = Jikan()


def pullcustomlist():
    idlst = []
    compcurr = {}
    query = input('Name of Anime: ')

    while not re.match(r'(?i)done', query):
        anime = jikan.search('anime', query)['results'][0]
        print(anime['title'])
        idlst.append(anime['mal_id'])
        compcurr[anime['title']] = [anime['url']+'/userrecs', anime['score']]
        query = input('Name of Anime(type "done" when done): ')

    malq = input('Do you have an MAL? ')
    if re.match(r'(?i)yes', malq):
        user = input('Username: ')
        animelst = jikan.user(username=user, request='animelist')
        idlst = idlist + [a['mal_id'] for a in animelst['anime']]

    return compcurr, idlst