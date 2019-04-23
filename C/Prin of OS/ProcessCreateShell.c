/* ----------------------------------------------------------------- */
/* my_shell_CSC562_2.c 								   */
/*    This program reads in an input line, parses the input line     */
/* into tokens, and use execvp() to execute the command.             */
/* ----------------------------------------------------------------- */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <errno.h>

/* ----------------------------------------------------------------- */
/* FUNCTION  parse:                                                  */
/*    This function takes an input line and parse it into tokens.    */
/* It first replaces all white spaces with zeros until it hits a     */
/* non-white space character which indicates the beginning of an     */
/* argument.  It saves the address to argv[], and then skips all     */
/* non-white spaces which constitute the argument.                   */
/* ----------------------------------------------------------------- */

void  parse(char *line, char **argv)
{
    while (*line != '\0') {       /* if not the end of line ....... */
        while (*line == ' ' || *line == '\t' || *line == '\n')
            *line++ = '\0';     /* replace white spaces with 0    */
        *argv++ = line;          /* save the argument position     */
        while (*line != '\0' && *line != ' ' &&
               *line != '\t' && *line != '\n')
            line++;             /* skip the argument until ...    */
    }
    *argv = '\0';                 /* mark the end of argument list  */
}

/* ----------------------------------------------------------------- */
/* FUNCTION execute_cp:                                                 */
/*    This function receives a commend line argument list with the   */
/* first one being a file name followed by its arguments.  Then,     */
/* this function forks a child process to execute the command using  */
/* system call execvp().                                             */
/* ----------------------------------------------------------------- */

void  execute_cp(char **argv)
{
    pid_t  pid;
    int    status;

    pid = fork();

    if (pid < 0) {     /* fork a child process           */
        printf("*** ERROR: forking child process failed\n");
        exit(1);
    }
    else if (pid == 0) {          /* for the child process:         */
        if (execvp(*argv, argv) < 0) {     /* execute the command  */
            printf("*** ERROR: exec failed\n");
            exit(1);
        }
    }
    else {                                  /* for the parent:      */
        while (wait(&status) != pid)       /* wait for completion  */
            ;
    }
}

/* ----------------------------------------------------------------- */
/* FUNCTION execute_cd:                                                 */
/*    This function receives a commend line argument list with the   */
/* the first argument being cd and the next argument being the       */
/* directory to change. You can implement this using chdir().        */
/* ----------------------------------------------------------------- */

void  execute_cd(char **argv)
{
    if (chdir(argv[1]) < 0) {
        printf("*** ERROR: chdir failed\n");
        exit(1);
    }
}

/* ----------------------------------------------------------------- */
/*                  The main program starts here                     */
/* ----------------------------------------------------------------- */

int  main(void)
{
    char  line[1024];             /* the input line                 */
    char  *argv[64];              /* the command line argument      */
    char cwd[4096];      /* current working directory */
    getcwd(cwd, sizeof cwd);


    while (1) {                   /* repeat until done ....         */
        printf("Current Directory: %s> ", cwd);     /*   display the current directory */
        gets(line);              /*   read in the command line     */
        printf("\n");
        parse(line, argv);       /*   parse the line               */
        if (strcmp(argv[0], "exit") == 0)  /* is it an "exit"?     */
            exit(0);            /*   exit if it is                */
        else if (strcmp(argv[0], "cd") == 0)
            execute_cd(argv);
        else
            execute_cp(argv);           /* otherwise, execute the command */
        getcwd(cwd, sizeof cwd);

    }
    return 1;
}
