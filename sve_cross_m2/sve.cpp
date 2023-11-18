#include "arm_sve.h"
#include <iostream>

int main() {
  // Vector length
  const int N = 16;

  // Input vectors
  int32_t a[N] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
  int32_t b[N] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160};

  // Output vector
  int32_t c[N];

  // Perform vector addition
  svbool_t pg = svptrue_b32();
  svint32_t va = svld1(pg, a);
  svint32_t vb = svld1(pg, b);
  svint32_t vc = svadd_s32_z(pg, va, vb);
  svst1(pg, c, vc);

  // Print the result
  for (int i = 0; i < N; i++) {
    std::cout << c[i] << " ";
    printf("%d ", c[i]);
  }
  printf("\n");

  return 0;
}