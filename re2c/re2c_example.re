// re2c $INPUT -o $OUTPUT -i --case-ranges
#include <cassert>
#include <iostream>
using namespace std;
#define YYDEBUG(s, c) cout << "state: " << s << " char: " << c << '\n'
bool lex(const char *s) {
    const char *YYCURSOR = s;
    /*!re2c
        re2c:yyfill:enable = 0;
        re2c:define:YYCTYPE = char;

        number = [1-9][0-9]*;

        number { return true; }
        *      { return false; }
    */
}

int main() {
    assert(lex("abd"));
    return 0;
}