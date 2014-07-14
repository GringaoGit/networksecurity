#include <stdio.h> // printf()
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <sys/types.h> // socket() connect()
#include <sys/socket.h> // socket() connect() AF_INET
#include <arpa/inet.h> // inet_addr() htons()
#include <unistd.h> // close()
#include <netdb.h> // gethostbyname()
#include <netinet/in.h>

#define MAX 100

int help(){
  printf("-h host -p port -m http method [-d payload] path\n");
}

int client(char *_host, int _port, char *_method, char *_payload, char *_path) {

  int sockfd;
  char buffer[MAX];
  struct hostent *host;
  struct sockaddr_in wood;

  if ((host=gethostbyname(_host)) == NULL){
      printf("[-] Erreur: Resolution de l'host impossible.\n");
      return -1;
  }

  if((sockfd=socket(AF_INET, SOCK_STREAM, 0)) == -1){
      printf("[-] Erreur: Impossible de créer le socket.\n");
      return -1;
  }

  wood.sin_addr = *((struct in_addr *)host->h_addr);
  wood.sin_family = AF_INET;
  wood.sin_port = htons(_port);
  memset(&(wood.sin_zero),'\0',8);

  char path[5];
  while(1){

      if (connect(sockfd, (struct sockaddr*)&wood, sizeof(wood))!=0){
          printf("[-] Erreur: Impossible de se connecter à %s sur %d.\n", _host, _port);
          perror("Erreur :");
          return -1;
      }

      while(1)
      {
          memset(buffer,0,MAX);

          sprintf(buffer, "%s %s HTTP/1.1", _method, _path);

          send(sockfd, buffer, sizeof(buffer),0);

          memset(buffer,0,MAX);
          recv(sockfd,buffer,MAX,0);
          printf("%s",buffer);

      }
      printf("[+] Requete connection envoyée.\n");

  }

close(sockfd);

}

int main(int argc, char **argv){

  int port = 80;
  char *host = NULL;
  char *method = NULL;
  char *payload = NULL;
  char *path = NULL;
  int index;
  int c;

  opterr = 0;

  while ((c = getopt (argc, argv, "h:m:p:d:")) != -1){
    switch (c){
      case 'h':
        host = optarg;
        break;
      case 'd':
        payload = optarg;
        break;
      case 'm':
        method = optarg;
        break;
      case 'p':
        port = atoi(optarg);
        break;
      case '?':
        if (optopt == 'h' || optopt == 'm' || optopt == 'd' || optopt == 'p'){
          fprintf (stderr, "Option -%c requires an argument ", optopt);
          help();
        } else if (isprint (optopt)) {
          fprintf (stderr, "Unknown option `-%c'.\n", optopt);
          help();
        } else {
          help();
        }
        exit(1);
      default:
        exit(1);
    }
  }

  if(argc < 8){
    help();
    exit(1);
  }

  path = argv[argc - 1];

  printf ("method = %s, port = %d, host = %s, path = %s\n",
         method, port, host, path);

  client(host, port, method, payload, path);

  return 0;

}
