//
//  SpotifyClient.c
//  Lo-Key
//
//  Created by Dilraj Devgun on 5/14/18.
//  Copyright © 2018 Dilraj Devgun. All rights reserved.
//
// #include "SpotifyClient.h"
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
struct spotify_artist_result* get_search_results(char *name, uint32_t temp, struct spotify_artist_result *result, uint64_t max_results);
struct spotify_artist_result* json_parser(char *jsonBytes, uint64_t length);


int main() {
  printf("hello\n");
  struct spotify_artist_result *result = malloc(sizeof(struct spotify_artist_result));
  get_search_results("kanye west", 10, result, 1);
  free(result);
  return 0;
}

struct spotify_artist_result *get_search_results(char *name, uint32_t name_length, struct spotify_artist_result *result, uint64_t max_results) {
    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd < 0) {
        return NULL;
    }

    // Connect to the remote server
    struct sockaddr_in remoteaddr;
    remoteaddr.sin_family = AF_INET;
    remoteaddr.sin_port = htons(50000);

    if(inet_pton(AF_INET, "127.0.0.1", &remoteaddr.sin_addr.s_addr)<=0)
    {
        printf("\nInvalid address/ Address not supported \n");
        return NULL;
    }

    printf("trying to connect\n");
    if (connect(socket_fd, (struct sockaddr *)&remoteaddr, sizeof(remoteaddr)) < 0) {
        return NULL;
    }
    printf("connected...\n");

    // send primer for message type
    char* buffer = "0\n";
    printf("%ld\n",sizeof(*buffer));
    if (send_data_over_socket(socket_fd, buffer, sizeof(*buffer) + 1) == -1) {
        return NULL;
    }

    // send 64 bits representing the size of the artist name
    char *data = (char*)&name_length;
    if (send_data_over_socket(socket_fd, data, sizeof(uint32_t)) == -1) {
        return NULL;
    }

    // send the actual artist name
    if (send_data_over_socket(socket_fd, name, name_length) == -1) {
        return NULL;
    }

    // wait for results
    // return result
    char buf[10] = {0};
    uint64_t buf_size = recv_data_until_termination_string(socket_fd, buf, 10);
    if (buf_size == -1) {
        return NULL;
    }

    int num_result_bytes = atoi(buf);
    printf("%d\n", num_result_bytes);
    uint64_t standardized_size = num_result_bytes;
    char jsonBytes[standardized_size];
    if (recv_data_over_socket(socket_fd, jsonBytes, standardized_size) == -1) {
        return NULL;
    }
    printf("%s\n", jsonBytes);

    struct spotify_artist_result *results = json_parser(jsonBytes, standardized_size);
    return results;
}

struct spotify_artist_result* json_parser(char *jsonBytes, uint64_t length) {
    char *data = jsonBytes + 6;
    char data_copy[length - 6];
    strcpy(data_copy, data);

    int num_results = 0;
    printf("-------\n");
    char *item = strtok(data, "[");
    while (item != NULL) {
        printf("%s\n", item);
        item = strtok(NULL, "[");
        num_results++;
    }
    printf("-------\n");

    struct spotify_artist_result *results = malloc(sizeof(struct spotify_artist_result) * num_results);

    char *save_ptr1;//, *save_ptr2;
    item = strtok_r(data_copy, "[", &save_ptr1);
    while (item != NULL) {
        char *artist_data = strtok(item, ",");
        results->name = artist_data;
        printf("artist name: %s\n", artist_data);
        artist_data = strtok(NULL, ",");
        results->artist_id = artist_data;
        printf("artist id: %s\n", artist_data);
        item = strtok_r(NULL, "[", &save_ptr1);
        results++;
    }
    return results;
}

uint64_t recv_data_until_termination_string(int socket, char *buffer, uint64_t max_size) {
    uint64_t bytes_recv = 0;
    do {
        char tempBuf[1];
        ssize_t n = recv(socket, tempBuf, 1, 0);
        if (n == -1 && errno != EAGAIN) {
            printf("%s\n", strerror(errno));
            return -1;
        }
        printf("bytes recieved [%s]\n", tempBuf);
        for (int i = 0; i < 1; i++) {
            buffer[bytes_recv + i] = tempBuf[i];
        }
        bytes_recv += n;
        if (bytes_recv >= 1 && strncmp((buffer + bytes_recv - 1), "\n", 1) == 0) {
            return bytes_recv;
        }
    } while (bytes_recv < max_size);
    if (bytes_recv > max_size) {
        return -1;
    }
    return bytes_recv;
}

uint64_t recv_data_over_socket(int socket, char *buffer, uint64_t buffer_size) {
    // send primer for message type
    uint64_t bytes_recv = 0;
    do {
        ssize_t n = recv(socket, buffer + bytes_recv, buffer_size - bytes_recv, 0);
        if (n == -1 && errno != EAGAIN) {
            printf("%s\n", strerror(errno));
            return -1;
        }
        bytes_recv += n;
    } while (bytes_recv < buffer_size);
    return bytes_recv;
}

uint64_t send_data_over_socket(int socket, void *buffer, uint64_t buffer_size) {
    // send primer for message type
    uint64_t bytes_sent = 0;
    do {
        ssize_t n = send(socket, buffer + bytes_sent, buffer_size - bytes_sent, 0);
        if (n == -1 && errno != EAGAIN) {
            printf("%s\n", strerror(errno));
            return -1;
        }
        bytes_sent += n;
    } while (bytes_sent != buffer_size);
    return bytes_sent;
}
