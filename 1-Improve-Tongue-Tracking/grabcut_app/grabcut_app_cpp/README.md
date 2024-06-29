# GrabCutTool

GrabCut GUI interface using C++

The end goal is to integrate it into [WhiskerToolbox](https://github.com/paulmthompson/WhiskerToolbox). As such, typical GUI handlers such as `mouseDrag` are implemented. It's intended that they are bound to Qt callbacks for keypresses and the like. However uncommenting `-DGRABCUTTOOL_HIGHGUI` allows direct usage of a gui from OpenCV. 