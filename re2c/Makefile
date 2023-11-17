all: gen
	g++ re2c_example.cpp -o re2c_example
gen:
	re2c -d -b -T --no-generation-date re2c_example.re -o re2c_example.cpp