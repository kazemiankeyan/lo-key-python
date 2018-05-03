import os
import sys
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
        print artist['genres']
        artist_arr.append((artist['name'], artist['id'], artist['genres']))
        i += 1

    print("\n")
    sel = input("Please enter the number of the artist you'd like to find similarities to: ")


    artist_genres = artist_arr[sel - 1][2]
    targest_artist_profile = gen_artist_profile(artist_arr[sel - 1])
    searchForArtistsInGenres(artist_genres)

    # print("\n<-- TESTING DATA -->")
    #
    # undiscovered_results = set()
    # getRelatedArtists(artist_arr[sel - 1], undiscovered_results, {artist_arr[sel - 1][1]})
    #
    # print("<!-- TESTING DATA --!>\n")
    #
    # print "\nHere are a list of similar \"Lo-Key Artists\" to",artist_arr[sel - 1][0],":\n"
    # for i in undiscovered_results:
    #     print(i[0])

def searchForArtistsInGenres(genres):
    underrated = []
    for genre in genres:
        results = sp.search(q='genre:' + genre, type='artist', limit=50)
        for result in results['artists']['items']:
            print results
            if result['popularity'] < 85:
                print result['name']
                underrated.append((result['name'], result['id'], result['genres']))
            # if (result['followers']['total'] < 850000 and result['popularity'] < 80) and (result['followers']['total'] > 100 and result['popularity'] > 5):
            #     print result['name']
            #     underrated.add((result['name'], result['id'], result['genres']))
    print()
    print()
    print(underrated)

def getRelatedArtists(artist, list, visited):
    if len(list) >= 10:
        return

    similar_results = sp.artist_related_artists(artist[1])
    for a in similar_results['artists']:
        if not(a['id'] in visited):
            visited.add(a['id'])
            print a['name'],"| POPULARITY PERCENTAGE:",a['popularity'],"| FOLLOWERS:",a['followers']['total']
            if (a['followers']['total'] < 150000 and a['popularity'] < 60) and (a['followers']['total'] > 100 and a['popularity'] > 5):
                list.add((a['name'], a['id']))
            getRelatedArtists((a['name'], a['id']), list, visited)

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


if __name__ == '__main__':
    main()
