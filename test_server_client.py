import sys
import socket
import struct
import thread
import time
import os
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
    print "searching for similarities to", str(artist_arr[sel - 1][0]), "..."

    try :
        s = socket.socket()
        port = 50000
        s.connect(('127.0.0.1', port))
        target_artist = artist_arr[sel - 1]
        artist_name_length = len(target_artist[0])
        artist_id_length = len(target_artist[1])
        length_metadata = (artist_name_length, artist_id_length)
        s.send(struct.Struct('I I').pack(*length_metadata))
        packer = struct.Struct(str(artist_name_length) + 's' + str(artist_id_length) + 's I I')
        packet = packer.pack(str(target_artist[0]), str(target_artist[1]), target_artist[2], target_artist[3])
        s.send(packet)
        s.send('\r\n')

        results = ""
        while True:
            try:
                data = s.recv(2)
            except socket.error, e:
                    break
            if len(data) != 0:
                results += data
                if results[-2:].decode("ascii") == '\r\n':
                    break
            else:
                break
        results = results[:-2]
        print '-------------results--------------'
        print results
        print '-------------results--------------'
        s.close()
    except socket.error, e:
        sys.exit(1)

if __name__ == '__main__':
    main()
