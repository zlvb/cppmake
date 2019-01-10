# Makefile
#
# usage :
#     make
#     make BUILD=release
#	  make clean
#

LIBPATH = -L./
INC = -I./include
LIBS = -lpthread
TARGET_BIN = "./bin/app"
COMMFLAG = -pipe -Wall -Wno-trigraphs -Werror
CXX = ccache g++ -std=gnu++1y
CC = ccache gcc -std=c11

CXXFLAGS = $(COMMFLAG) -g3 -ggdb3 -O0 -D_DEBUG
OBJPATH = ./build/

all : $(TARGET_BIN)

clean :
	rm -rf ./build
	rm -rf $(TARGET_BIN)

.PHONY: clean


AllDirs := $(shell ls -R ./dir1 | grep '^\./.*:$$' | awk '{gsub(":","");print}') $(shell ls -R ./dir2 | grep '^\./.*:$$' | awk '{gsub(":","");print}')
$(warning $(AllDirs))
SRCS_LIB := $(foreach n,$(AllDirs) , $(wildcard $(n)/*.cpp))
SRCS_LIB_C := $(foreach n,$(AllDirs) , $(wildcard $(n)/*.c))
SRCS_LIB_CC := $(foreach n,$(AllDirs) , $(wildcard $(n)/*.cc))
OBJS_BIN = $(SRCS_LIB:%.cpp=$(OBJPATH)/%.o) $(SRCS_LIB_C:%.c=$(OBJPATH)/%.o) $(SRCS_LIB_CC:%.cc=$(OBJPATH)/%.o)
$(warning $(OBJS_BIN))

ifneq "$(MAKECMDGOALS)" "clean"
-include $(SRCS_LIB:%.cpp=$(OBJPATH)/%.d)
-include $(SRCS_LIB_CC:%.cc=$(OBJPATH)/%.d)
-include $(SRCS_LIB_C:%.c=$(OBJPATH)/%.d)
endif

$(TARGET_BIN) : $(OBJS_BIN)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LIBS)

$(OBJPATH)/%.o : %.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(INC) -o $@ -c $<

$(OBJPATH)/%.d : %.cpp
	@echo $(CXX) -MM -o $@ -c $<
	@rm -f $@
	@mkdir -p $(dir $@)
	@$(CXX) $(CXXFLAGS) -pipe $(INC) -MM -MT '$@ $(basename $@).o' $< -o $@

$(OBJPATH)/%.o : %.c
	@mkdir -p $(dir $@)
	$(CC) $(CXXFLAGS) $(INC) -o $@ -c $<

$(OBJPATH)/%.d : %.c
	@echo $(CC) -MM -o $@ -c $<
	@rm -f $@
	@mkdir -p $(dir $@)
	@$(CC) $(CXXFLAGS) -pipe $(INC) -MM -MT '$@ $(basename $@).o' $< -o $@

$(OBJPATH)/%.o : %.cc
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(INC) -o $@ -c $<

$(OBJPATH)/%.d : %.cc
	@echo $(CC) -MM -o $@ -c $<
	@rm -f $@
	@mkdir -p $(dir $@)
	@$(CXX) $(CXXFLAGS) -pipe $(INC) -MM -MT '$@ $(basename $@).o' $< -o $@

