import re
import requests

from malrec import watchlists, recpull, finallist
from customlist import pullcustomlist

if __name__ == '__main__':
    site = 'https://myanimelist.net'
    if requests.head(site).status_code == 200:

        initq = input('MAL or user input?')
        if re.match(r'(?i)MAL', initq):
            user  = input('username: ')

            while requests.head(site + '/animelist/' + user).status_code == 404:
                user = input('User name not valid. Please try again: ')

            score = float(input('minimum score: '))
            compcurr, idlst = watchlists(user, score)

        else:
            compcurr, idlst = pullcustomlist()

        recs = recpull(compcurr, idlst)
        final = finallist(recs, compcurr)

        print(f'{user}\'s recommendations:\n')
        for x in final:
            print(x, '\n')

    else:
        print('MAL is down, please try later')