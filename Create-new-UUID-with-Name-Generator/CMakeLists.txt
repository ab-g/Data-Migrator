cmake_minimum_required(VERSION 3.22)
project(CreateNewUUIDWithNameGenerator)

set(CMAKE_CXX_STANDARD 17)

add_executable(${PROJECT_NAME} main.cc)

target_include_directories(${PROJECT_NAME} PRIVATE "${PROJECT_SOURCE_DIR}/ThirdParty/inc/")

set_target_properties(
    ${PROJECT_NAME}
    PROPERTIES
        OUTPUT_NAME "CreateUUIDFromString"
)
