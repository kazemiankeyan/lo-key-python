import sys
import struct
import socket
import thread
import time
import os
import spotipy
import Queue as q
import multiprocessing as mp
from multiprocessing import Process, Queue
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from Queue import PriorityQueue


client_credentials_manager = SpotifyClientCredentials(client_id='9e1915c12f364fc599912bafb773ab28', client_secret='5155e553917b4dccafe00786c41692e7')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def main():
    try :
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 50000)
        listening_socket.bind(server_address)
        listening_socket.listen(1000)
        print("Proxy listening on " + str(server_address))

        while True:
            connection, client_address = listening_socket.accept()
            thread.start_new_thread(handle_connection, (connection, client_address))
        listening_socket.close()
    except socket.error, e:
        print "Error creating socket: %s" %e
        sys.exit(1)

def handle_connection(connection, client_address):
    unpacker = struct.Struct('I I')
    artist_length_data = ''
    try:
        artist_length_data = connection.recv(unpacker.size)
    except socket.error, e:
            print "Error getting artist name length: %s" %e
            sys.exit(1)
    artist_length_data = unpacker.unpack(artist_length_data)
    artist_name_length = artist_length_data[0]
    artist_id_length = artist_length_data[1]

    artistData = ""
    unpacker = struct.Struct(str(artist_name_length) + 's' + str(artist_id_length) + 's I I')
    while True:
        try:
            data = connection.recv(unpacker.size + 2)
        except socket.error, e:
                break
        if len(data) != 0:
            artistData += data
            if artistData[-2:].decode("ascii") == '\r\n':
                break
        else:
            break
    artistData = artistData[:-2]
    artist = unpacker.unpack(artistData)

    targest_artist_profile = gen_artist_profile(artist)
    search(targest_artist_profile, artist, connection)
    connection.send('\r\n')
    connection.close()

def search(targest_artist_profile, ogartist, connection):
    underrated = PriorityQueue()
    lokey = set()
    fringe = q.Queue()
    fringe.put(ogartist)
    getRelatedArtists_bfs(ogartist, lokey, {ogartist[1]}, fringe, [])

    quadrant_size = len(lokey)/4
    lokey_list = list(lokey)
    processes = []
    qu = mp.Queue()
    for i in range(0, 4):
        process = Process(target=generateProfilePriority, args=(lokey_list[0+(quadrant_size*i):(quadrant_size*i)+quadrant_size], targest_artist_profile, qu))
        process.start()
        processes += [process]

    for process in processes:
        process.join()

    print '-------------results--------------'
    while not qu.empty():
        item = qu.get()
        print item
        underrated.put(item)
    while not underrated.empty():
        item = underrated.get()
        print item
        connection.send(str(item) + '\n')

def generateProfilePriority(artists, targest_artist_profile, qu):
    for artist in artists:
        current_profile = gen_artist_profile(artist)
        priority = generate_profile_diff(targest_artist_profile, current_profile)
        qu.put((priority, artist[0], artist[2], artist[3]))

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
                if (a['followers']['total'] < 150000 and a['popularity'] < 55) and (a['followers']['total'] > 100 and a['popularity'] > 5):
                    print a['name'],"| POPULARITY PERCENTAGE:",a['popularity'],"| FOLLOWERS:",a['followers']['total']
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

if __name__ == '__main__':
    main()
