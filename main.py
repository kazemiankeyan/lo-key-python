import os
import sys
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

def main():
    client_credentials_manager = SpotifyClientCredentials(client_id='9e1915c12f364fc599912bafb773ab28', client_secret='5155e553917b4dccafe00786c41692e7')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlists = sp.user_playlists('kaaazemian')

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

if __name__ == '__main__':
    main()
