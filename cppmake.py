#!/usr/bin/python
# -*- coding: utf-8 -*-

def addtoArr(arr, templ, s):
    dirs = s.split(',')
    for d in dirs:
        arr.append(templ % d.strip())

def replaceTempl(templ, flag, arr):
    return templ.replace('{%s}' % flag, ' '.join(arr))

TEMPL = '''# Makefile
#
# usage :
#     make
#     make BUILD=release
#	  make clean
#

LIBPATH = -L./
INC = {inc}
LIBS = -lpthread
TARGET_BIN = "{out}"
COMMFLAG = -pipe -Wall -Wno-trigraphs -Werror
CXX = ccache g++ -std=gnu++1y
CC = ccache gcc -std=c11

CXXFLAGS = $(COMMFLAG) -g3 -ggdb3 -O0 -D_DEBUG
OBJPATH = {tmp}/

all : $(TARGET_BIN)

clean :
	rm -rf {tmp}
	rm -rf $(TARGET_BIN)

.PHONY: clean


AllDirs := {src}
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

'''

src = []
inc = []
tmp = ['./build/temp']
out = ['a.out']

dirtempl = r'''$(shell ls -R %s | grep '^\./.*:$$' | awk '{gsub(":","");print}')'''
inctempl = '''-I%s'''
deftempl = '%s'

templ_table = (
    ('src', dirtempl, src),
    ('inc', inctempl, inc),
    ('tmp', deftempl, tmp),
    ('out', deftempl, out),
)

templ_map = {}
for tr in templ_table: 
    templ_map[tr[0]+':'] = (len(tr[0])+1, tr[1], tr[2])


def getparam(line):
    line = line.strip()
    for k, v in templ_map.items():
        kl, tmpl, arr = v
        key = line[:kl]
        if key == k:
            addtoArr(arr, tmpl, line[kl:])

import sys, os

if len(sys.argv) == 1:
    arg = "cppmake.txt"
else:
    arg = sys.argv[1]

fd = open(arg, "rb")
if not fd:
    print("no inputfile")
    quit()

txt = fd.read()
fd.close()
cmdlines = txt.split('\n')

for line in cmdlines:
    line = line.strip()
    getparam(line)

fd = open("Makefile", "wb+")
result = replaceTempl(TEMPL, 'src', src)
result = replaceTempl(result, 'inc', inc)
result = replaceTempl(result, 'tmp', tmp[-1:])
result = replaceTempl(result, 'out', out[-1:])
fd.write(result)
fd.close()
