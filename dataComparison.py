# to get a better grasp at the correlation between followers and popularity percentage
# and whether or not it is viable to use followers as an accurate data metric

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
import Queue as q
import matplotlib.pyplot as plt

client_credentials_manager = SpotifyClientCredentials(client_id='6710b9d22bac42729693c4910cc56649', client_secret='e44f7d7a7a6f4a059a4bdda329193b41')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artistName = raw_input("enter artist: ")

result = sp.search(q='artist:' + artistName, type='artist', limit=5)
artist_arr = []
for artist in result['artists']['items']:
    artist_arr.append((artist['name'], artist['id']))

i = 1
for artist in artist_arr:
    print "",i,":",artist[0]
    i += 1
print("\n")
sel = input("choose artist: ")

target_artist = artist_arr[sel - 1]

fringe = q.Queue()
visited = set()
fringe.put(target_artist)
followers = []
popularity = []

while(len(visited) < 1000):
    current_artist = fringe.get()
    similar_results = sp.artist_related_artists(current_artist[1])
    for a in similar_results['artists']:
        if not(a['id'] in visited):
            visited.add(a['id'])
            print a['name'],"| POPULARITY PERCENTAGE:",a['popularity'],"| FOLLOWERS:",a['followers']['total']
            followers.append(a['followers']['total'])
            popularity.append(a['popularity'])
            fringe.put((a['name'], a['id']))


plt.xlabel('Popularity %')
plt.ylabel('Followers')
plt.title('Followers vs Popularity %')
plt.grid(True)
plt.scatter(popularity, followers)
plt.show()
