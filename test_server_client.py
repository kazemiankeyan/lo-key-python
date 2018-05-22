import sys
import socket
import struct
import thread
import time
import os
import Queue as q
import json
from Queue import PriorityQueue


def main():


    # result = sp.search(q='artist:' + artist, type='artist', limit=50)
    # print("\n")
    # artist_arr = []
    # i = 1
    # for artist in result['artists']['items']:
    #     print "",i,":",artist['name']
    #     print artist['genres']
    #     artist_arr.append((artist['name'], artist['id'], artist['followers']['total'], artist['popularity']))
    #     i += 1
    # print("\n")
    # sel = input("Please enter the number of the artist you'd like to find similarities to: ")
    # print "searching for similarities to", str(artist_arr[sel - 1][0]), "...\n"

    try :
        s = socket.socket()
        port = 50000
        s.connect(('127.0.0.1', port))
        artist = raw_input("Hello! Welcome to Lo-Key.\n \nPlease search an artist: ")
        s.send(struct.Struct('I').pack(len(artist)))
        s.send(artist)
        
        while True:
            try:
                data = s.recv(1024)
            except socket.error, e:
                break

        data = json.loads(data.decode())
        artist_search_data = data.get("a")

        i = 1
        for artist in artist_search_data:
            print "",i,":",artist['name']
            i += 1
        print("\n")
        sel = input("Please enter the number of the artist you'd like to find similarities to: ")
        print "searching for similarities to", str(artist_search_data[sel - 1][0]), "...\n"


        target_artist = artist_search_data[sel - 1]
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
        print '-------------results--------------\n'
        print results
        print '-------------results--------------'
        s.close()
    except socket.error, e:
        sys.exit(1)

if __name__ == '__main__':
    main()
