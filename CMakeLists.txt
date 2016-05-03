cmake_minimum_required(VERSION 3.3)
project(chymera-vis)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(READER_SOURCE_FILES binaryReader.cpp binaryReader.h)

add_executable(reader ${READER_SOURCE_FILES})