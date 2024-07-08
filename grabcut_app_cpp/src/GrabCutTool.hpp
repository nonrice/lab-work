#ifndef GRABCUTTOOL_HPP
#define GRABCUTTOOL_HPP

#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>

class GrabCutTool
{
public:
    GrabCutTool(std::string img_path);

    void runHighgui();

    cv::Mat getImgDisp();
    cv::Mat getMaskDisp();
    cv::Mat getMask();

    // Mouse event handlers
    void mouseDown(int x, int y);
    void mouseMove(int x, int y);
    void mouseUp(int x, int y); 

    // Painting
    void setColor(uint8_t color);
    void setBrushThickness(int thickness);
    void increaseBrushThickness();
    void decreaseBrushThickness();

    // GrabCut specific
    void grabcutIter();

private:
    cv::Mat _img;

    // State variables
    bool _rect_stage = true;
    cv::Rect _rect;
    bool _drawing = false;
    cv::Point _mouse_prev, _mouse_cur;
    int _brush_thickness = 5;
    uint8_t _color = cv::GC_PR_FGD;
    bool _first_iter = false;

    // grabCut specific
    cv::Mat _mask;
    cv::Mat _bg_model, _fg_model;

    void _brushOutline(cv::Mat& img);

    // Testing with OpenCV highlevel GUI
    static void _mouseHandlerWrapper(int event, int x, int y, int flags, void* params);
    void _mouseHandler(int event, int x, int y, int flags);
};

#endif // GRABCUTTOOL_HPP
