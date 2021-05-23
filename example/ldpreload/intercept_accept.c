#define _GNU_SOURCE

#include <stdio.h>
#include <dlfcn.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/socket.h>

int accept4(int sockfd, struct sockaddr *addr, socklen_t *addrlen, int flags)
{
    printf("accept4 intercept\n");

    int (*original_accept4)(int sockfd, struct sockaddr *addr, socklen_t *addrlen, int flags);
    original_accept4 = dlsym(RTLD_NEXT, "accept4");
    return (*original_accept4)(sockfd, addr, addrlen, flags);
}

int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen)
{
    printf("accept intercept\n");

    int (*original_accept)(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
    original_accept = dlsym(RTLD_NEXT, "accept");
    return (*original_accept)(sockfd, addr, addrlen);
}
