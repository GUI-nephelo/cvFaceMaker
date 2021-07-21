# CMakeList.txt: cvFaceMaker 的 CMake 项目，在此处包括源代码并定义
# 项目特定的逻辑。
#
cmake_minimum_required (VERSION 3.8)

project ("cvFaceMaker")

# 将源代码添加到此项目的可执行文件。
add_executable (cvFaceMaker "src/cvFaceMaker.cpp" "src/cvFaceMaker.h" "src/dlibHelper.cpp")

# TODO: 如有需要，请添加测试并安装目标。
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY PROJECT_BINARY_DIR)
set(OpenCV_DIR "D:\\opencv\\build")
set(dlib_DIR "D:\\dlib-19.22\\build\\dlib\\config")

# find required opencv
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(cvFaceMaker ${OpenCV_LIBS})


#find_package(dlib REQUIRED)
include_directories(D:\\dlib-19.22)
#aux_source_directory(. SRC_LIST)
#ink_libraries("C:\\Users\\Thinkpad\\source\\repos\\cvFaceMaker\\lib\\dlib_release.lib")
target_link_libraries(${PROJECT_NAME} C:\\Users\\Thinkpad\\source\\repos\\cvFaceMaker\\lib\\dlib_release.lib)

#MESSAGE(${dlib_LIBS})