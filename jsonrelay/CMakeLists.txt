cmake_minimum_required(VERSION 3.1)
project(JsonRelay LANGUAGES CXX)

# If you only include this third party in PRIVATE source files, you do not need to install it
# when your main project gets installed.
set(JSON_Install OFF CACHE INTERNAL "")

add_subdirectory(nlohmann_json)

add_executable(json-relay main.cpp)
target_link_libraries(json-relay PRIVATE nlohmann_json::nlohmann_json)
