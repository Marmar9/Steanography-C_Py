CXX := c++

CXXFLAGS := -O3 -Wall -std=c++11 -fPIC $(shell python3 -m pybind11 --includes)

SRCDIR := src/cpp

SRCS := $(wildcard $(SRCDIR)/*.cpp)
BINDIR := bin

OBJS := $(SRCS:$(SRCDIR)/%.cpp=$(BINDIR)/%.o)

TARGET := src/steanography.so

.PHONY: debug
all: $(TARGET)


$(OBJS): $(SRCS)
	$(CXX) -c $(CXXFLAGS) $< -o $@

$(TARGET): $(OBJS)
	$(CXX) -shared $(CXXFLAGS) $< -o $@

debug:
	@echo $(SRCS)
	@echo $(OBJS)

