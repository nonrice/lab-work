#include <iostream>
#include <functional>

#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

#include "GrabCutTool.hpp"
#define GRABCUTTOOL_HIGHGUI
GrabCutTool::GrabCutTool(std::string path){
    _img = cv::imread(path);
    if (_img.empty()){
        std::cout << "Error: Image not found\n";
        return;
    }
    _img_disp = _img.clone();
    _mask_disp = _img.clone(); 

#ifdef GRABCUTTOOL_HIGHGUI 
    cv::namedWindow("Editor", cv::WINDOW_AUTOSIZE);
    cv::imshow("Editor", _img_disp);
    cv::namedWindow("Mask Preview", cv::WINDOW_AUTOSIZE);
    cv::imshow("Mask Preview", _mask_disp);

    cv::setMouseCallback("Editor", _mouseHandlerWrapper, this);

    while (true){
        cv::imshow("Editor", _img_disp);
        if (cv::waitKey(30) == 27){
            break;
        } else if (cv::waitKey(30) == 'g'){
            _grabcut_iter();
        }
    }
#endif
}

void GrabCutTool::_mouseHandlerWrapper(int event, int x, int y, int flags, void* params){
    reinterpret_cast<GrabCutTool*>(params)->_mouseHandler(event, x, y, flags);
}

void GrabCutTool::_mouseHandler(int event, int x, int y, int flags){
    if (event == cv::EVENT_LBUTTONDOWN){
        _mouseDown(x, y);
    } else if (event == cv::EVENT_MOUSEMOVE && (flags & cv::EVENT_FLAG_LBUTTON)){
        _mouseDrag(x, y);
    } else if (event == cv::EVENT_LBUTTONUP){
        _mouseUp(x, y);
    }
}

void GrabCutTool::_mouseDown(int x, int y){
    if (_rect_stage){
        _rect = cv::Rect(x, y, 0, 0);
    } else {
    }
}
void GrabCutTool::_mouseDrag(int x, int y){
    if (_rect_stage){
        _rect.width = std::max(0, x - _rect.x);
        _rect.height = std::max(0, y - _rect.y);

        _img_disp = _img.clone();
        cv::rectangle(_img_disp, _rect, cv::Scalar(0, 255, 0), 1);
    } else {
    }
}

void GrabCutTool::_mouseUp(int x, int y){
    if (_rect_stage){
        _rect_stage = false;
    }
}

void GrabCutTool::_setColor(uint8_t color){
    _color = color;
}

void GrabCutTool::_grabcut_iter(){
    if (_rect_stage){
        std::cout << "Error: Please select a region of interest\n";
        return;
    }
    if (!_first_iter){
        _bg_model = cv::Mat::zeros(1, 65, CV_64FC1);
        _fg_model = cv::Mat::zeros(1, 65, CV_64FC1);
        _mask = cv::Mat::zeros(_img.size(), CV_8UC1);
        cv::grabCut(_img, _mask, _rect, _bg_model, _fg_model, 1, cv::GC_INIT_WITH_RECT);
        _first_iter = true;
    } else {
        cv::grabCut(_img, _mask, _rect, _bg_model, _fg_model, 1, cv::GC_INIT_WITH_MASK);
    }
#ifdef GRABCUTTOOL_HIGHGUI
    for (int i = 0; i < _mask.rows; i++){
        for (int j = 0; j < _mask.cols; j++){
            if (_mask.at<uint8_t>(i, j) == cv::GC_PR_FGD){
                _mask_disp.at<cv::Vec3b>(i, j) = _img.at<cv::Vec3b>(i, j);
            } else {
                _mask_disp.at<cv::Vec3b>(i, j) = cv::Vec3b(0, 0, 0);
            }
        }
    }
    cv::imshow("Mask Preview", _mask_disp);
#endif
}
