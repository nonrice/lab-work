.PHONY: all orofacial_module grabcut_app_cpp

all: orofacial_module grabcut_app_cpp

orofacial_module: orofacial/orofacial/grabcut_app.py orofacial/orofacial/jaw_tracking_convert.py orofacial/orofacial/tongue_mask_processing.py orofacial/orofacial/tongue_tip_track_2D.py

orofacial/orofacial/grabcut_app.py: workspace/grabcut_app/grabcut_app.py
	cp workspace/grabcut_app/grabcut_app.py orofacial/orofacial/grabcut_app.py

orofacial/orofacial/jaw_tracking_convert.py: workspace/jaw_tracking_convert/jaw_tracking_convert.py
	cp workspace/jaw_tracking_convert/jaw_tracking_convert.py orofacial/orofacial/jaw_tracking_convert.py

orofacial/orofacial/tongue_mask_processing.py: workspace/tongue_mask_processing/tongue_mask_processing.py
	cp workspace/tongue_mask_processing/tongue_mask_processing.py orofacial/orofacial/tongue_mask_processing.py

orofacial/orofacial/tongue_tip_track_2D.py: workspace/tongue_tip_tracking/tongue_tip_track_2D.py
	cp workspace/tongue_tip_tracking/tongue_tip_track_2D.py orofacial/orofacial/tongue_tip_track_2D.py

grabcut_app_cpp: grabcut_app_cpp/src/GrabCutTool.cpp grabcut_app_cpp/src/GrabCutTool.hpp grabcut_app_cpp/README.md

grabcut_app_cpp/src/GrabCutTool.cpp: workspace/grabcut_app/cpp/src/GrabCutTool.cpp
	mkdir -p grabcut_app_cpp/src && cp workspace/grabcut_app/cpp/src/GrabCutTool.cpp grabcut_app_cpp/src/GrabCutTool.cpp

grabcut_app_cpp/src/GrabCutTool.hpp: workspace/grabcut_app/cpp/src/GrabCutTool.hpp
	mkdir -p grabcut_app_cpp/src && cp workspace/grabcut_app/cpp/src/GrabCutTool.hpp grabcut_app_cpp/src/GrabCutTool.hpp

grabcut_app_cpp/README.md: workspace/grabcut_app/cpp/README.md
	cp workspace/grabcut_app/cpp/README.md grabcut_app_cpp/README.md