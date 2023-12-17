#include <iostream>
using namespace std;

int main() {

  cout << "addr:checksum\n";
  for (int i = 1; i < 12; i++) {
    int res =
        0x4500 + 0x0040 + 0x0000 + 0x4000 + 0x3c06 + 0x0a00 + 0x0a0a + 0x0b01;
    for (int j = 0; j < 2; j++) {
      int bytes = (i << 8) + 100 + j;

      cout << dec << "10.0." << i << "." << 100 + j << ":";
      res += bytes;
      if (res > 0xffff) {
        res = (res & 0xffff) + (res >> 16);
      }
      cout << hex << (~res & 0xffff) << "\n";
    }
  }
}
