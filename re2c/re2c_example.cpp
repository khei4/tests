/* Generated by re2c 3.0 */
#line 1 "re2c_example.re"
// re2c $INPUT -o $OUTPUT -i --case-ranges
#include <cassert>
#include <iostream>
using namespace std;
#define YYDEBUG(s, c) cout << "state: " << s << " char: " << c << '\n'
bool lex(const char *s) {
    const char *YYCURSOR = s;
    
#line 12 "re2c_example.cpp"
{
	char yych;
	static const unsigned char yybm[] = {
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		128, 128, 128, 128, 128, 128, 128, 128, 
		128, 128,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
		  0,   0,   0,   0,   0,   0,   0,   0, 
	};
	YYDEBUG(0, *YYCURSOR);
	yych = *YYCURSOR;
	if (yych <= '0') goto yy1;
	if (yych <= '9') goto yy2;
yy1:
	YYDEBUG(1, *YYCURSOR);
	++YYCURSOR;
#line 15 "re2c_example.re"
	{ return false; }
#line 58 "re2c_example.cpp"
yy2:
	YYDEBUG(2, *YYCURSOR);
	yych = *++YYCURSOR;
	if (yybm[0+yych] & 128) {
		goto yy2;
	}
#line 14 "re2c_example.re"
	{ return true; }
#line 67 "re2c_example.cpp"
}
#line 16 "re2c_example.re"

}

int main() {
    assert(lex("abd"));
    return 0;
}