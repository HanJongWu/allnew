<<<<<<< HEAD
#include <stdio.h>
#include "libcheckprime.h"

void main() {
  while (1) {
    int n;
    printf("\ninput integer => ")
    scanf("%d", &n);
    if (n == 0) break;
    if (checkprime(n) == n)
     printf("%d is a prime number \n", n);
    else
     printf("%d is not prime number \n", n);
  }
}
=======
#include <stdio.h>
#include "libcheckprime.h"

void main() {
  while (1) {
    int n;
    printf("\ninput integer => ")
    scanf("%d", &n);
    if (n == 0) break;
    if (checkprime(n) == n)
     printf("%d is a prime number \n", n);
    else
     printf("%d is not prime number \n", n);
  }
}
>>>>>>> 79422af022d2b1c781b80b59661ac4111fab851c
