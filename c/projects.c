#include <stdio.h>
#include <dirent.h>
#include <sys/dirent.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <errno.h>
#include <limits.h>
#include <unistd.h>

FILE* fzf_pipe;
char* base = "/Users/faustofusse/Documents";
char c;

void find_repos (const char * dir_name) {
    DIR* d = opendir (dir_name);
    struct dirent* entry;
    if (!d) {
        fprintf (stderr, "Cannot open directory '%s': %s\n", dir_name, strerror (errno));
        exit (EXIT_FAILURE);
    }
    while ((entry = readdir(d)) != NULL) {
        const char * d_name = entry->d_name;
        if (strcmp(d_name, ".git") != 0) continue;
        fprintf(fzf_pipe, "%s\n", dir_name); 
        return;
    }
    rewinddir(d);
    while ((entry = readdir(d)) != NULL) {
        const char * d_name = entry->d_name;
        if (entry->d_type & DT_DIR) {
            if (strcmp (d_name, "..") != 0 && strcmp (d_name, ".") != 0) {
                char path[PATH_MAX];
                int path_length = snprintf (path, PATH_MAX, "%s/%s", dir_name, d_name);
                if (path_length >= PATH_MAX) {
                    fprintf (stderr, "Path length has got too long.\n");
                    exit (EXIT_FAILURE);
                }
                find_repos(path);
            }
        }
    }
    closedir(d);
}

int main(int argc, char *argv[]) {
    if (argc > 1) base = argv[1];
    fzf_pipe = popen("fzf --reverse", "r+");
    find_repos(base);
    while ((c = fgetc(fzf_pipe)) != EOF) printf("%c", c);
    return pclose(fzf_pipe);
}
