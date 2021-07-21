#include "cvFaceMaker.h"

using namespace dlib;

frontal_face_detector detector;
shape_predictor pose_model;

void init() {
	detector = get_frontal_face_detector();
	deserialize("C:\\Users\\Thinkpad\\source\\repos\\cvFaceMaker\\models/shape_predictor_68_face_landmarks.dat") >> pose_model;
}

std::vector<cv::Point> getMarks(string imgPath) {
	std::vector<cv::Point> landmarks;
	array2d<rgb_pixel> img;
	load_image(img, imgPath);
	std::vector<dlib::rectangle> faces = detector(img);
	std::vector<dlib::full_object_detection> shapes;
	for (unsigned long i = 0; i < faces.size(); ++i) {
		dlib::full_object_detection shape = pose_model(img, faces[i]);
		shapes.push_back(shape);
		for (int j = 0; j < 68; ++j) {
			cv::Point p = cv::Point(shapes[i].part(j).x(), shapes[i].part(j).y());
			landmarks.push_back(p);
		}
	}
	return landmarks;
}