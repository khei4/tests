# memory sanitizer is unavailable on M2
memory:
	clang++ -fsanitize=memory sanitizers.cpp -g

thread:
	clang++ -fsanitize=thread sanitizers.cpp -g

address:
	clang++ -fsanitize=address sanitizers.cpp -g

undefined:
	clang++ -fsanitize=undefined sanitizers.cpp -g

leak:
	clang++ -fsanitize=leak sanitizers.cpp -g