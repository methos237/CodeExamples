#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
/**
 * Assignment 3: Process Forking
 * For CSC 562-01, Spring 2019, Dr. Somya D. Mohanty
 * University of North Carolina at Greensboro
 *
 * @author James Knox Polk <jkpolk@uncg.edu>
 * @date 3/7/2019
 *
 * Usage:  Runs six processes altogether. With the following requirements:
 *      At most three fork() function calls are allowed.
 *      No for() loops, no do while loops, etc.
 *
 */

int main() {
    pid_t pid;

    pid = fork();
    fork();
    if (pid > 0)
        fork();

    printf("Hello, World!\n");
    sleep(30);
    return 0;
}