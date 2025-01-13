cmake_minimum_required(VERSION 3.28)
project(Info_Stealer_Algorithm__Naive_Bayes_)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXE_LINKER_FLAGS "-static")
include_directories(include)

add_executable(parser parser.cpp)
add_executable(calculation_algorithm calculation_algorithm.cpp)
add_executable(backup backup.cpp)

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,--stack,209715200")
endif()
