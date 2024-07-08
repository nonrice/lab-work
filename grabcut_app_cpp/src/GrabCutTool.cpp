#include <iostream>
#include <functional>

#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

#include "GrabCutTool.hpp"

GrabCutTool::GrabCutTool(std::string path){
    _img = cv::imread(path);
    if (_img.empty()){
        std::cout << "Error: Image not found\n";
        return;
    }
}

void GrabCutTool::runHighgui(){
    cv::namedWindow("Mask Preview", cv::WINDOW_AUTOSIZE);
    cv::namedWindow("Editor", cv::WINDOW_AUTOSIZE);
    cv::moveWindow("Mask Preview", 50, 50);

    cv::setMouseCallback("Editor", _mouseHandlerWrapper, this);

    while (true){
        cv::imshow("Editor", getImgDisp());
        cv::imshow("Mask Preview", getMaskDisp());
        switch (cv::waitKey(1)){
            case 'g':
                grabcutIter();
                std::cout << "GrabCut iteration\n";
                break;
            case 'q':
                cv::destroyAllWindows();
                std::cout << "Quit\n";
                return;
            case '.':
                increaseBrushThickness();
                std::cout << "Brush thickness: " << _brush_thickness << "\n";
                break;
            case ',':
                decreaseBrushThickness();
                std::cout << "Brush thickness: " << _brush_thickness << "\n";
                break;
            case '1':
                setColor(cv::GC_BGD);
                std::cout << "Drawing background\n";
                break;
            case '2':
                setColor(cv::GC_FGD);
                std::cout << "Drawing foreground\n";
                break;
            case '3':
                setColor(cv::GC_PR_BGD);
                std::cout << "Drawing probable background\n";
                break;
            case '4':
                setColor(cv::GC_PR_FGD);
                std::cout << "Drawing probable foreground\n";
                break;
        }
    }

    cv::destroyAllWindows();
}

void GrabCutTool::_mouseHandlerWrapper(int event, int x, int y, int flags, void* params){
    reinterpret_cast<GrabCutTool*>(params)->_mouseHandler(event, x, y, flags);
}

void GrabCutTool::_mouseHandler(int event, int x, int y, int flags){
    if (event == cv::EVENT_LBUTTONDOWN){
        mouseDown(x, y);
    } else if (event == cv::EVENT_MOUSEMOVE){
        mouseMove(x, y);
    } else if (event == cv::EVENT_LBUTTONUP){
        mouseUp(x, y);
    }
}

void GrabCutTool::mouseDown(int x, int y){
    _drawing = true;
    if (_rect_stage){
        _rect = cv::Rect(x, y, 0, 0);
    } else {
        _mouse_prev = cv::Point(x, y);
        cv::circle(_mask, _mouse_prev, _brush_thickness, _color, -1);
    }
}
void GrabCutTool::mouseMove(int x, int y){
    _mouse_cur = cv::Point(x, y);
    if (_drawing){
        if (_rect_stage){
            _rect.width = std::max(0, x - _rect.x);
            _rect.height = std::max(0, y - _rect.y);
        } else {
            cv::line(_mask, _mouse_prev, _mouse_cur, _color, 2*_brush_thickness);
            _mouse_prev = _mouse_cur;
        }
    }
}

void GrabCutTool::mouseUp(int x, int y){
    _drawing = false;
    if (_rect_stage){
        _rect_stage = false;
    }
}

void GrabCutTool::setColor(uint8_t color){
    _color = color;
}

void GrabCutTool::setBrushThickness(int thickness){
    _brush_thickness = thickness;
}

void GrabCutTool::increaseBrushThickness(){
    _brush_thickness++;
}

void GrabCutTool::decreaseBrushThickness(){
    _brush_thickness = std::max(1, _brush_thickness-1);
}

void GrabCutTool::grabcutIter(){
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
}

void GrabCutTool::_brushOutline(cv::Mat& img){
    for (int y = std::max(_mouse_cur.y - _brush_thickness, 0); y < std::min(_mouse_cur.y + _brush_thickness, img.rows); ++y) {
        for (int x = std::max(_mouse_cur.x - _brush_thickness, 0); x < std::min(_mouse_cur.x + _brush_thickness, img.cols); ++x) {
            double dist = cv::norm(_mouse_cur - cv::Point(x, y));
            if (dist <= _brush_thickness && dist >= _brush_thickness - 2){
                img.at<cv::Vec3b>(y, x) = cv::Vec3b(255, 255, 255) - img.at<cv::Vec3b>(y, x);
            }
        }
    }
}

cv::Mat GrabCutTool::getImgDisp(){
    cv::Mat img_disp = _img.clone();

    // Show rectangle if it exists
    if ((_drawing && _rect_stage) || !_rect_stage){
        cv::rectangle(img_disp, _rect, cv::Scalar(0, 255, 0), 1);
    }

    // Show brush region 
    if (!_rect_stage){
        _brushOutline(img_disp);
    }
    return img_disp;
}

cv::Mat GrabCutTool::getMaskDisp(){
    // Show foreground mask multiplied with image
    cv::Mat mask_disp = cv::Mat::zeros(_img.size(), CV_8UC3);
    for (int i = 0; i < _mask.rows; i++){
        for (int j = 0; j < _mask.cols; j++){
            if (_mask.at<uint8_t>(i, j) == cv::GC_PR_FGD || _mask.at<uint8_t>(i, j) == cv::GC_FGD){
                mask_disp.at<cv::Vec3b>(i, j) = _img.at<cv::Vec3b>(i, j);
            } else {
                mask_disp.at<cv::Vec3b>(i, j) = cv::Vec3b(0, 0, 0);
            }
        }
    }
    _brushOutline(mask_disp);
    return mask_disp;
}

cv::Mat GrabCutTool::getMask(){
    return _mask;
}