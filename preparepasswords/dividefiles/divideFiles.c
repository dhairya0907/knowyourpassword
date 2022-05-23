#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>

#define PBSTR "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
#define PBWIDTH 100

void printProgress(double percentage) {
    int val = (int) (percentage * 100);
    int lpad = (int) (percentage * PBWIDTH);
    int rpad = PBWIDTH - lpad;
    printf("\e[?25l\r%3d%% [%.*s%*s]", val, lpad, PBSTR, rpad, "");
    fflush(stdout);
}

char * genrateFilePath(char * string1, char char1) {
  char * result = NULL;
  asprintf( & result, "%s%c", string1, char1);
  return result;
}

char * genrateFileName(char * string1, char * string2, char char1, char char2, char * string3) {
  char * result = NULL;
  asprintf( & result, "%s%s%c%c%s", string1, string2, char1, char2, string3);
  return result;
}

char * appendTwoChar(char char1, char char2) {
  char * result = NULL;
  asprintf( & result, "%c%c", char1, char2);
  return result;
}

int processPasswordFile(char * passwordFile) {
  clock_t start, end;
  double cpu_time_used;

  // If only hashes then keep below line to 45
  int MAXLINELEN = 100; // Change this to increase the maximum line length(if file has both hash and password)
  char * line = malloc(sizeof(char) * MAXLINELEN);

  struct stat st = {
    0
  };

  char flag = 'T'; // Set this as T if proceessing from start

  char pointerMainArray[16] = {
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F'
  };
  char pointerSubArray[16] = {
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F'
  };
  int mainCounter = 0; // Main Folder Counter
  int subCounter = 0; // Sub File Counter

  FILE * writePasswordFile;

  start = clock();

  FILE * ptr;

  if ((ptr = fopen(passwordFile, "r")) == NULL) {
    printf("no such file as %s \n", passwordFile);
    return 0;
  }

  char * aline;
  int count = 0;
  int totalCount = 14346081;

  while ((aline = fgets(line, MAXLINELEN, ptr)) != NULL) {
    if (strcmp(aline, "") == 0) // Last Line Which Has Been Processed, put inside "" and \n in the end.
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

      char * currentPotinter = appendTwoChar(aline[0], aline[1]);
      char * nextPointer = appendTwoChar(pointerMainArray[mainCounter], pointerSubArray[subCounter]);
      
      if (strcmp(currentPotinter, nextPointer) == 0) {
        fclose(writePasswordFile);

        char * filePathWithCommand = genrateFilePath("mkdir -p ../../Passwords/rockyou/hasheswithpasswords/", aline[0]);

        if (stat(filePathWithCommand, & st) == -1) {
          system(filePathWithCommand);
        }

        char * filePath = genrateFilePath("../../Passwords/rockyou/hasheswithpasswords/", aline[0]);
        char * fileName = genrateFileName(filePath, "/passwords-starting-with-", aline[0], aline[1], ".txt");

        writePasswordFile = fopen(fileName, "a+");
        nextPointer = appendTwoChar(pointerMainArray[mainCounter], pointerSubArray[subCounter]);

        subCounter++;
        if (subCounter >= 16) {
          subCounter = 0;
          mainCounter++;
        }

        fprintf(writePasswordFile, "%s", aline);
      //  printf("WORKING MODE : %s", aline);
      } else {
        fprintf(writePasswordFile, "%s", aline);
      //  printf("WORKING MODE : %s", aline);
      }
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
  char * passwordFile = "../../Passwords/rockyou/rockyouhashwithpassword.txt";
  processPasswordFile(passwordFile);

  return 0;
}