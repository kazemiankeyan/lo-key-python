//
//  SpotifyClient.h
//  Lo-Key
//
//  Created by Dilraj Devgun on 5/14/18.
//  Copyright © 2018 Dilraj Devgun. All rights reserved.
//

#ifndef SpotifyClient_h
#define SpotifyClient_h

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>

struct spotify_artist_result {
    char *name;
    char *artist_id;
};

// Gets and populates the
uint64_t send_data_over_socket(int socket, void *buffer, uint64_t buffer_size);
uint64_t recv_data_over_socket(int socket, char *buffer, uint64_t buffer_size);
uint64_t recv_data_until_termination_string(int socket, char *buffer, uint64_t max_size);
struct spotify_artist_result* get_search_results(char *name, uint32_t name_length, uint64_t max_results, int *num_results);
struct spotify_artist_result* json_parser(char *jsonBytes, uint64_t length, int *num_results);

#endif /* SpotifyClient_h */
