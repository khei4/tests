#include <stdint.h>
int main() {
  int s = 0;
  alignas(128) int arr1[4096];
  alignas(128) int arr1i[4096] = {0};
  int arr2[2][3];

  int8_t l_962[1][4][4] = {{{0x75L, 1L, 0x75L, 1L},
                            {0x75L, 1L, 1L, 0x75L},
                            {(-1L), 1L, 0x11L, 1L},
                            {1L, 1L, 0x11L, 0x11L}}};
  int arr3[4096][4096][4096];
  for (int j = 0; j < 1024; j++)
    for (int i = 0; i < 1024; i++) {
      {
        s++;
      }
      return 13;
    }
}
