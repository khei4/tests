#include <stdio.h>

extern int my_function(int a, int b);

int main() {
   int a = 4;
   int b = 7;
   printf("After calling my_function, the values of both a and b are now %d\n", my_function(a, b));
   return(0);
}
