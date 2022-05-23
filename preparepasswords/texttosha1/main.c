#include "sha1.h"
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define PBSTR "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
#define PBWIDTH 100

void printProgress(double percentage) {
    int val = (int) (percentage * 100);
    int lpad = (int) (percentage * PBWIDTH);
    int rpad = PBWIDTH - lpad;
    printf("\e[?25l\r%3d%% [%.*s%*s]", val, lpad, PBSTR, rpad, "");
    fflush(stdout);
}

int processPasswordFile(char * passwordFile) {
  clock_t start, end;
  double cpu_time_used;

  int MAXLINELEN = 45;
  char * line = malloc(sizeof(char) * MAXLINELEN);

  struct stat st = {
    0
  };

  char flag = 'F'; // Set this as T if proceessing from start

  FILE * writePasswordAndHashFile;
  FILE * writeHashFile;

  start = clock();

  FILE * ptr;

  if ((ptr = fopen(passwordFile, "r")) == NULL) {
    printf("no such file as %s \n", passwordFile);
    return 0;
  }

  char * aline;
  int count = 0;
  int totalCount = 14344355;

  while ((aline = fgets(line, MAXLINELEN, ptr)) != NULL) {
    if (strcmp(aline, "TheBull27\n") == 0) // Last Line Which Has Been Processed, put inside "" and \n in the end.
    {
      //printf("STANDBY MODE : %s", aline);
      flag = 'T';
      count++;
      printProgress((double) count / totalCount);
    } else if (flag == 'F') {
      //printf("STANDBY MODE : %s", aline);
      count++;
      printProgress((double) count / totalCount);
    } else {

      char * filePathWithCommand = "mkdir -p ../../Passwords/rockyou/";

      if (stat(filePathWithCommand, & st) == -1) {
        system(filePathWithCommand);
      }

      aline[strcspn(aline, "\n")] = 0;

      Sha1Digest computed = Sha1_get(aline, strlen(aline));
      char cStr[41];
      Sha1Digest_toStr( & computed, cStr);

      char * fileName;

      fileName = "../../Passwords/rockyou/rockyouhashwithpassword.txt";
      writePasswordAndHashFile = fopen(fileName, "a+");

      fileName = "../../Passwords/rockyou/rockyouhash.txt";
      writeHashFile = fopen(fileName, "a+");

      fprintf(writePasswordAndHashFile, "%s:%s\n", cStr, aline);
      //printf("WORKING MODE : %s:%s\n", cStr,aline);
      fclose(writePasswordAndHashFile);

      fprintf(writeHashFile, "%s\n", cStr);
      //printf("WORKING MODE : %s\n", cStr);
      fclose(writeHashFile);

      count++;
      printProgress((double) count / totalCount);

    }
  }

  fclose(ptr);

  end = clock();
  cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
  printf("\nTime taken for fgets: %f \n", cpu_time_used);

  return 1;
}

int main(int argc, char * argv[]) {
  char * passwordFile = "../../Passwords/rockyou/rockyouunique.txt";
  processPasswordFile(passwordFile);

  return 0;
}