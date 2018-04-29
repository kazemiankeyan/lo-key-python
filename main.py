import os
import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='9e1915c12f364fc599912bafb773ab28', client_secret='5155e553917b4dccafe00786c41692e7')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def main():
    if len(sys.argv) > 1:
        # username = sys.argv[1]
        artist = sys.argv[1]
    else:
        print "Usage: %s [username]" % (sys.argv[0],)
        sys.exit()

    # playlists = sp.user_playlists(username)
    # for playlist in playlists['items']:
    #     print playlist['tracks']

    # results = sp.search(q=artist, limit=20)
    # for i, t in enumerate(results['tracks']['items']):
    #     print ' ', i, t['name']

    result = sp.search(q='artist:' + artist, type='artist', limit=50)

    artist_arr = []
    i = 1
    for artist in result['artists']['items']:
        print "",i,":",artist['name'], artist['id']
        artist_arr.append((artist['name'], artist['id']))
        i += 1

    sel = input("Please select the number of the artist you'd like to find similarities to: ")
    #print(artist_arr[sel - 1])

    undiscovered_results = getRelatedArtists(artist_arr[sel - 1])
    for artist in undiscovered_results:
        undiscovered_results = undiscovered_results.union(getRelatedArtists(artist))


    print("Here are a list of similar \"Lowkey Artists\":)
    for i in undiscovered_results:
        print(i[0])

def getRelatedArtists(artist):
    similar_results = sp.artist_related_artists(artist[1])
    undiscovered_results = set()

    for artist in similar_results['artists']:
        # print(artist['genres'])
        if artist['followers']['total'] < 100000 and artist['popularity'] < 50:
            undiscovered_results.add((artist['name'], artist['id']))
    return undiscovered_results


if __name__ == '__main__':
    main()
