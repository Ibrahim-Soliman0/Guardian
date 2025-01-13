cmake_minimum_required(VERSION 3.28)
project(Add_Data)

set(CMAKE_CXX_STANDARD 17)
include_directories(include)

add_executable(Add_Data main.cpp)

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,--stack,524288000")
endif()
