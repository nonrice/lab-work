#ifndef GRABCUTTOOL_HPP
#define GRABCUTTOOL_HPP

#include <opencv2/imgcodecs.hpp>

class GrabCutTool
{
public:
    GrabCutTool(std::string img_path);

private:
    cv::Mat _img, _img_disp, _mask_disp;

    // State variables
    bool _rect_stage = true;
    cv::Rect _rect;
    bool _drawing = false;
    int _mouse_prev_x, _mouse_prev_y;
    uint8_t _color = 0;
    bool _first_iter = false;

    // Mouse event handlers
    void _mouseDown(int x, int y);
    void _mouseDrag(int x, int y);
    void _mouseUp(int x, int y);

    void _setColor(uint8_t color);

    // grabCut specific
    void _grabcut_iter();
    cv::Mat _mask;
    cv::Mat _bg_model, _fg_model;

    // Testing with OpenCV highlevel GUI
    static void _mouseHandlerWrapper(int event, int x, int y, int flags, void* params);
    void _mouseHandler(int event, int x, int y, int flags);
};

#endif // GRABCUTTOOL_HPP
