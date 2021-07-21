// cvFaceMaker.h: 标准系统包含文件的包含文件
// 或项目特定的包含文件。

#pragma once

#include <iostream>

#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <dlib/image_io.h>
using namespace std;
//using namespace cv;
void init();
std::vector<cv::Point> getMarks(string);

cv::Mat* blink(string);
cv::Mat* mouthOpen(string);
cv::Mat* nodHead(string);
cv::Mat* shakeHead(string);


// TODO: 在此处引用程序需要的其他标头。
/*
chin : 0-16


*/