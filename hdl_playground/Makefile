run-wave-sim:
	iverilog tmp.v -o tmp.vvp -g 2012
	vvp tmp.vvp
	gtkwave tmp.vcd

vg-docker:
	docker run -w /src -v $(PWD):/src --name veriloggen4 -i -t user/veriloggen /usr/bin/fish

build:
	docker build -t user/veriloggen .

clean:
	rm -rf *.vcd *.vvp *.out parsetab.py .pytest_cache __pycache__