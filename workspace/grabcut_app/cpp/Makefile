CXX = /usr/bin/clang++
CXXFLAGS = -std=c++17 -Wall -Wextra $(shell pkg-config --cflags opencv4)
LDFLAGS = $(shell pkg-config --libs opencv4)
SRCS = src/main.cpp src/GrabCutTool.cpp
PROG = main

$(PROG): $(SRCS) 
	$(CXX) $(SRCS) $(CXXFLAGS) $(LDFLAGS) -o $(PROG)