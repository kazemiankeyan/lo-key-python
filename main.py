import os
import sys
import Queue
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='9e1915c12f364fc599912bafb773ab28', client_secret='5155e553917b4dccafe00786c41692e7')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def main():
    # if len(sys.argv) > 1:
    #     # username = sys.argv[1]
    #     artist = sys.argv[1]
    # else:
    #     print "Usage: %s [username]" % (sys.argv[0],)
    #     sys.exit()

    # playlists = sp.user_playlists(username)
    # for playlist in playlists['items']:
    #     print playlist['tracks']

    # results = sp.search(q=artist, limit=20)
    # for i, t in enumerate(results['tracks']['items']):
    #     print ' ', i, t['name']

    artist = raw_input("Hello! Welcome to Lo-Key.\n \nPlease search an artist: ")
    result = sp.search(q='artist:' + artist, type='artist', limit=50)
    print("\n")
    artist_arr = []
    i = 1
    for artist in result['artists']['items']:
        print "",i,":",artist['name']
        artist_arr.append((artist['name'], artist['id']))
        i += 1

    print("\n")
    sel = input("Please enter the number of the artist you'd like to find similarities to: ")
    #print(artist_arr[sel - 1])

    print("\n<-- TESTING DATA -->")

    undiscovered_results = set()
    fringe = Queue.Queue()
    fringe.put(artist_arr[sel - 1])
    getRelatedArtists(artist_arr[sel - 1], undiscovered_results, {artist_arr[sel - 1][1]}, fringe)

    print("<!-- TESTING DATA --!>\n")

    print "\nHere are a list of similar \"Lo-Key Artists\" to",artist_arr[sel - 1][0],":\n"
    for i in undiscovered_results:
        print(i[0])

def getRelatedArtists(artist, list, visited, fringe):
    while not(fringe.empty()) and len(list) < 15:
        current_artist = fringe.get()
        similar_results = sp.artist_related_artists(current_artist[1])
        for a in similar_results['artists']:
            if not(a['id'] in visited):
                visited.add(a['id'])
                print a['name'],"| POPULARITY PERCENTAGE:",a['popularity'],"| FOLLOWERS:",a['followers']['total']
                if (a['followers']['total'] < 150000 and a['popularity'] < 55) and (a['followers']['total'] > 100 and a['popularity'] > 5):
                    list.add((a['name'], a['id']))
                fringe.put((a['name'], a['id']))

    # similar_results = sp.artist_related_artists(artist[1])
    # for a in similar_results['artists']:
    #     if not(a['id'] in visited):
    #         visited.add(a['id'])
    #         print a['name'],"| POPULARITY PERCENTAGE:",a['popularity'],"| FOLLOWERS:",a['followers']['total']
    #         if (a['followers']['total'] < 150000 and a['popularity'] < 55) and (a['followers']['total'] > 100 and a['popularity'] > 5):
    #             list.add((a['name'], a['id']))
    #         getRelatedArtists((a['name'], a['id']), list, visited)


if __name__ == '__main__':
    main()
