find_package(Z3 REQUIRED CONFIG)

set(CMAKE_CXX_FLAGS "-Wall -fPIC ${CMAKE_CXX_FLAGS}")
set(CMAKE_CXX_STANDARD 20)

include_directories(Z3_CXX_INCLUDE_DIRS)
add_executable(main example.cpp)
target_link_libraries(main ${Z3_LIBRARIES})