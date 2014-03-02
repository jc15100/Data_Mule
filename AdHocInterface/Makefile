CXX := g++
SRCDIR :=.
BUILDDIR := Release
CFLAGS := -O3
EXTRA_CFLAGS :=
LIBFLAGS :=

TARGET := $(BUILDDIR)/AdHocInterface

SOURCES := $(wildcard $(SRCDIR)/*.cpp)
OBJECTS := $(patsubst $(SRCDIR)/%,$(BUILDDIR)/%,$(SOURCES:.cpp=.o))

$(TARGET): $(OBJECTS)
	@echo " Linking..."; $(CXX) $^ $(LIBFLAGS) -o $(TARGET)

$(BUILDDIR)/%.o: $(SRCDIR)/%.cpp
	@mkdir -p $(BUILDDIR)
	@echo " $(CXX) $<"; $(CXX) -c $(CFLAGS) $(EXTRA_CFLAGS) -o $@ $< 	

run: $(TARGET)
	./$(TARGET) $(option)

clean:
	@echo " Cleaning..."
	@rm -fr $(BUILDDIR) $(TARGET) 2>/dev/null || true

.PHONY: clean
