
PYTHON_CONFIG=python2.7-config
PYTHON_CXXFLAGS = $(shell $(PYTHON_CONFIG) --includes)
PYTHON_LIBRARIES = $(shell $(PYTHON_CONFIG) --ldflags)

LLVM_CONFIG = llvm-config
LLVM_CXXFLAGS = $(shell $(LLVM_CONFIG) --cppflags)
LLVM_LIBRARIES = $(shell $(LLVM_CONFIG) --ldflags --libs core jit native)

BOOST_PYTHON_LIBRARIES = -lboost_python-mt

CXXFLAGS = -g $(LLVM_CXXFLAGS) $(PYTHON_CXXFLAGS)
LDFLAGS = -g
LIBRARIES = $(LLVM_LIBRARIES) $(PYTHON_LIBRARIES) $(BOOST_PYTHON_LIBRARIES)

CXX = clang++
LD = clang++

BUILDDIR=build

default: python

python: $(BUILDDIR)/arithmetic.so

clean:
	rm -rf $(BUILDDIR)/* > /dev/null || true

$(BUILDDIR)/%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

$(BUILDDIR)/arithmetic: $(BUILDDIR)/arithmetic.o $(BUILDDIR)/main.o
	$(LD) $(LDFLAGS) -shared -o $@ $+ $(LIBRARIES)

$(BUILDDIR)/arithmetic.so: $(BUILDDIR)/arithmetic.o $(BUILDDIR)/python_interface.o
	$(LD) $(LDFLAGS) -shared -o $@ $+ $(LIBRARIES)
