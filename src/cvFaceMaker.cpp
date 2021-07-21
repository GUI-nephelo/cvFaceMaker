// cvFaceMaker.cpp: 定义应用程序的入口点。
//

#include "cvFaceMaker.h"
#include <time.h>

#define IMGPATH "C:\\Users\\Thinkpad\\PycharmProjects\\gaokaoData\\机考运河\\21110112101513.JPG"

using namespace cv;


Mat* blink(Mat img) {
	Mat* r = 
}

int main()
{
	Mat a=imread(IMGPATH);
	if (!a.data) {
		cout << "load error" << endl;
		return -1;
	}
	int t1 = time(NULL);
	init();
	std::vector<Point> pts = getMarks(IMGPATH);
	int t2 = time(NULL);
	int i = 0;
	for (Point &p : pts) {
		circle(a, p, 2, Scalar(0, 0, 0));
		putText(a, cv::String(to_string(i)),p,cv::FONT_HERSHEY_PLAIN,1,Scalar(0,0,0));
		i++;
	}
	putText(a, cv::String(to_string(t2 - t1)),Point(20,40),cv::FONT_HERSHEY_PLAIN,2,Scalar(0,0,0));
	namedWindow("as");
	imshow("as",a);
	waitKey(0);
	//cout << a << endl;
	return 0;
}
