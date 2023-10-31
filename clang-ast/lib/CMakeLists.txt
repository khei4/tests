add_library(kast
            KAST.cpp)
target_include_directories(kast SYSTEM PUBLIC ${CLANG_INCLUDE_DIRS} ${LLVM_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})

if(CLANG_LINK_CLANG_DYLIB)
    target_link_libraries(kast PUBLIC LLVM)
    clang_target_link_libraries(kast PUBLIC)
else()
    llvm_map_components_to_libnames(llvm_libs support core)
    target_link_libraries(kast PUBLIC ${llvm_libs}
                                                   clangASTMatchers
                                                   clangTransformer
                                                   clangTooling)
endif(CLANG_LINK_CLANG_DYLIB)