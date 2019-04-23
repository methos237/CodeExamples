#include <stdio.h>
#include<sys/types.h>
#include<unistd.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int check_int (char *arg) {
    for (int i = 0; i < strlen(arg); ++i) {
        if (!isdigit(arg[i]))
            return 1;
    }

    return 0;
}

int main(int argc, char **argv) {
    int print_int;
    int print_times;

    //check number of arguments. This number includes the program name.  And check for type errors.
    if (argc != 3 || check_int(argv[1]) != 0|| check_int(argv[2]) != 0) {
        printf("Usage: %s print_int print_times (both must be an integers) \n", argv[0]);
        return 1;
    }
    print_int = atoi(argv[1]);
    print_times = atoi(argv[2]);

    for (int i = 0; i < print_times; ++i) {
        printf("%d\n", print_int);
    }
    //printf("print_int=%d\n", print_int);

    return 0;
}

