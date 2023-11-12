#include <iostream>
#include <nlohmann/json.hpp>

int main() {
    nlohmann::json jsonInput;
    try {
        std::cin >> jsonInput;
        std::cout << jsonInput.dump() << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
