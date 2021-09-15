cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(antlr4 CONFIG REQUIRED)

add_executable(example HelloParser.cpp HelloListener.cpp HelloLexer.cpp HelloBaseListener.cpp)
target_link_libraries(example antlr4::antlr4)
