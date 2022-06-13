cmake_minimum_required(VERSION 3.17)

set (CMAKE_CXX_STANDARD 17)

project(backend VERSION 1 DESCRIPTION "fractals backend")

include(GNUInstallDirs)

add_library(backend SHARED src/Backend.cpp)

set_target_properties(backend PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    PUBLIC_HEADER include/Backend.hpp)

target_include_directories(backend PRIVATE .)

install(TARGETS backend
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(FILES ${CMAKE_BINARY_DIR}/backend.pc
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)
