#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

// basically from: https://clang.llvm.org/docs/MemorySanitizer.html
void memory(int n) {
  int *a = new int[10];
  a[n] = 0; // uninitialized
}

void *p;
int leak() {
  p = malloc(7);
  p = 0; // The memory is leaked here.
  return 0;
}

int Global;
void *Thread1(void *x) {
  Global = 42; // race
  return x;
}
int thread() {
  pthread_t t;
  pthread_create(&t, NULL, Thread1, NULL);
  Global = 43; // race
  pthread_join(t, NULL);
  return Global;
}

int address(int n) {
  int *array = new int[100];
  delete[] array;
  return array[n]; // BOOM
}

int main(int argc, char **argv) {
  memory(3);
  leak();
  thread();
  address(101);
}
