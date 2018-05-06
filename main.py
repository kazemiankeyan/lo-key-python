import os
import sys
import spotipy
import Queue as q
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from Queue import PriorityQueue

client_credentials_manager = SpotifyClientCredentials(client_id='9e1915c12f364fc599912bafb773ab28', client_secret='5155e553917b4dccafe00786c41692e7')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def main():

    artist = raw_input("Hello! Welcome to Lo-Key.\n \nPlease search an artist: ")
    result = sp.search(q='artist:' + artist, type='artist', limit=50)
    print("\n")
    artist_arr = []
    i = 1
    for artist in result['artists']['items']:
        print "",i,":",artist['name']
        print artist['genres']
        artist_arr.append((artist['name'], artist['id'], artist['followers']['total'], artist['popularity']))
        i += 1
    print("\n")
    sel = input("Please enter the number of the artist you'd like to find similarities to: ")

    artist_genres = artist_arr[sel - 1][2]
    targest_artist_profile = gen_artist_profile(artist_arr[sel - 1])
    search(targest_artist_profile, artist_arr[sel - 1])

def search(targest_artist_profile, ogartist):
    underrated = PriorityQueue()
    lokey = set()
    fringe = q.Queue()
    fringe.put(ogartist)
    getRelatedArtists_bfs(ogartist, lokey, {ogartist[1]}, fringe, [])
    for artist in lokey:
        current_profile = gen_artist_profile(artist)
        priority = generate_profile_diff(targest_artist_profile, current_profile)
        underrated.put((priority, artist[0], artist[2], artist[3]))

    while not underrated.empty():
        print(underrated.get())

def generate_profile_diff(base_profile, comp_profile):
    diff = 0
    for key in base_profile:
        diff += abs(base_profile[key] - comp_profile[key])
    return diff

def getRelatedArtists_bfs(artist, list, visited, fringe, genres):
    while not(fringe.empty()) and len(list) < 100:
        current_artist = fringe.get()
        similar_results = sp.artist_related_artists(current_artist[1])
        for a in similar_results['artists']:
            if not(a['id'] in visited):
                visited.add(a['id'])
                print a['name'],"| POPULARITY PERCENTAGE:",a['popularity'],"| FOLLOWERS:",a['followers']['total']
                if (a['followers']['total'] < 150000 and a['popularity'] < 55) and (a['followers']['total'] > 100 and a['popularity'] > 5):
                    list.add((a['name'], a['id'], a['followers']['total'], a['popularity']))
                    genres += a['genres']
                fringe.put((a['name'], a['id']))

def gen_artist_profile(artist):
    top_tracks = sp.artist_top_tracks(artist[1])
    profile = {}
    for track in top_tracks['tracks']:
        track_feature = sp.audio_features(str(track['id']))[0]
        for feature in track_feature:
            if type(track_feature[feature]) == int or type(track_feature[feature]) == float:
                if feature in profile:
                    profile[feature] += track_feature[feature]
                else:
                    profile[feature] = track_feature[feature]
    for feature in profile:
        profile[feature] /= len(top_tracks['tracks'])

    print(profile)
    print(len(top_tracks['tracks']))

    return profile

'''
-------------------------------------------------------------
#MARK :- Old Code:
-------------------------------------------------------------
'''
def getRelatedArtists_dfs(artist, list, visited, genres):
    if len(list) >= 100:
        return

    similar_results = sp.artist_related_artists(artist[1])
    for a in similar_results['artists']:
        if not(a['id'] in visited):
            visited.add(a['id'])
            if (a['followers']['total'] < 150000 and a['popularity'] < 60) and (a['followers']['total'] > 100 and a['popularity'] > 5):
                print(a['name'], "| POPULARITY: ", a['popularity'], "| FOLLOWERS:", a['followers']['total'])
                list.add((a['name'], a['id'], a['followers']['total'], a['popularity']))
                genres += a['genres']
            getRelatedArtists((a['name'], a['id']), list, visited, genres)

def searchForArtistsInGenres(genres, targest_artist_profile, artist):
    underrated = PriorityQueue()
    if genres.empty():
        getRelatedArtists
    for genre in genres:
        offset = 0
        limit = 50
        while underrated.qsize() < 1000 and limit*offset < 10000:
            results = sp.search(q='genre:' + genre, type='artist', limit=50, offset=limit*offset)
            offset+=1
            if not results['artists']['items']:
                break
            for result in results['artists']['items']:
                if (result['followers']['total'] < 150000 and result['popularity'] < 60) and (result['followers']['total'] > 100 and result['popularity'] > 5):
                    print result['name']
                    current_profile = gen_artist_profile((result['name'], result['id']))
                    priority = generate_profile_diff(targest_artist_profile, current_profile)
                    underrated.put((priority, result['name'], result['id'], result['genres']))

    while not underrated.empty():
        next_item = underrated.get()
        print(next_item)


if __name__ == '__main__':
    main()
