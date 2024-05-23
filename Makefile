CXX := c++

CXXFLAGS := -O3 -Wall -std=c++11 -fPIC $(shell python3 -m pybind11 --includes)

SRCDIR := src/cpp

SRCS := $(wildcard $(SRCDIR)/*.cpp)
BINDIR := bin

OBJS := $(SRCS:$(SRCDIR)/%.cpp=$(BINDIR)/%.o)

TARGET := bin/steanography.so

.PHONY: debug run
all: $(TARGET)

#Wrong solution
# $(OBJS): $(SRCS)
# 	$(CXX) -c $(CXXFLAGS) $< -o $@

$(BINDIR)/%.o: $(SRCDIR)/%.cpp
	$(CXX) -c $(CXXFLAGS) $< -o $@


$(TARGET): $(OBJS)
	$(CXX) -shared $(CXXFLAGS) $^ -o $@

debug:
	@echo $(SRCS)
	@echo $(OBJS)

run: $(TARGET)
	source venv/bin/activate && \
	pip install -r requirements.txt && \
	export PYTHONPATH="$(PWD)/bin" && \
	python src/api.py
