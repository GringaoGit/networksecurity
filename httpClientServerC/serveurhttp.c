int cfd,fd=socket(PF_INET,SOCK_STREAM,IPPROTO_TCP);
struct sockaddr_in si;
si.sin_family=PF_INET;
inet_aton("127.0.0.1",&si.sin_addr);
si.sin_port=htons(80);
bind(fd,(struct sockaddr*)si,sizeof si);
listen(fd);
while ((cfd=accept(fd,(struct sockaddr*)si,sizeof si)) != -1) {
read_request(cfd); /* read(cfd,...) until "\r\n\r\n" */
write(cfd,"200 OK HTTP/1.0\r\n\r\n"
"That’s it. You’re welcome.",19+27);
close(cfd);
}