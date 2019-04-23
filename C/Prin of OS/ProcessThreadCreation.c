/**
 * CSC 562-01 Assignment 4 - Spring 2019
 * UNCG - Dr. Somya D. Mohanty
 *
 * Process and thread creation
 * Thread creation taken from IBM pthread_create() example
 * https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.1.0/com.ibm.zos.v2r1.bpxbd00/ptcrea.htm
 *
 * @author James Knox Polk <jkpolk@uncg.edu>
 * Last Updated 4/5/2019
 */

#include <sys/types.h>
#include <unistd.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void *thread(void *arg) {
    char *ret;
    printf("'%s' created\n", arg);
    if ((ret = (char*) malloc(20)) == NULL) {
        perror("malloc() error");
        exit(2);
    }
    sleep(15);
    strcpy(ret, "child thread");
    pthread_exit(ret);
}

void thread_create () {
    pthread_t thid;
    void *ret;

    if (pthread_create(&thid, NULL, thread, "child thread") != 0) {
        perror("pthread_create() error");
        exit(1);
    }

    if (pthread_join(thid, &ret) != 0) {
        perror("pthread_create() error");
        exit(3);
    }

    printf("'%s' exited\n", ret);
}



int  main(int argc, char *argv[]){
    pid_t pid;

    pid = fork();
    if (pid < 0) { /* Error Occurred */
        fprintf(stderr, "Fork Failed");
    }

    else (pid == 0) { /* child process */
        fork();
        thread_create();
    }

    fork();
    sleep(30);
    return 0;
}







