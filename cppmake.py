#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

TEMPL = '''# Makefile

LIBPATH = -L./
INC = {inc}
LIBS = -lpthread
TARGET_BIN = "{out}"
TARGET_PATH = "{__oup}"
COMMFLAG = -pipe -Wall -Wno-trigraphs -Werror
CXX = g++ -std=gnu++1y
CC = gcc -std=c11

CXXFLAGS = $(COMMFLAG) -g3 -ggdb3 -O0 -D_DEBUG
OBJPATH = {tmp}/

all : $(TARGET_BIN)

clean :
	rm -rf {tmp}
	rm -rf $(TARGET_BIN)

.PHONY: clean


AllDirs := {src}
SRCS_LIB := $(foreach n,$(AllDirs) , $(wildcard $(n)/*.cpp))
SRCS_LIB_C := $(foreach n,$(AllDirs) , $(wildcard $(n)/*.c))
SRCS_LIB_CC := $(foreach n,$(AllDirs) , $(wildcard $(n)/*.cc))
OBJS_BIN = $(SRCS_LIB:%.cpp=$(OBJPATH)/%.o) $(SRCS_LIB_C:%.c=$(OBJPATH)/%.o) $(SRCS_LIB_CC:%.cc=$(OBJPATH)/%.o)
#$(warning $(OBJS_BIN))

ifneq "$(MAKECMDGOALS)" "clean"
-include $(SRCS_LIB:%.cpp=$(OBJPATH)/%.d)
-include $(SRCS_LIB_CC:%.cc=$(OBJPATH)/%.d)
-include $(SRCS_LIB_C:%.c=$(OBJPATH)/%.d)
endif

$(TARGET_BIN) : $(OBJS_BIN)
	@mkdir -p $(TARGET_PATH)
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

dirtempl = r'''$(shell ls -R %s|grep '^\./.*:$$'|awk '{gsub(":","");print}')'''
inctempl = '''-I%s'''
deftempl = '%s'

src = []
inc = []
tmp = ['./build/temp']
out = ['a.out']
outpath = ['./']

import_files = []

templ_table = (
    ('src', dirtempl, src, 0),
    ('inc', inctempl, inc, 0),
    ('tmp', deftempl, tmp, 1),
    ('out', deftempl, out, 1),
    ('add', deftempl, import_files, 0),
    ('__oup', deftempl, outpath, 1),
)

proced_files = set()

templ_map = {}
for tr in templ_table: 
    templ_map[tr[0]+':'] = (len(tr[0])+1, tr[1], tr[2])


def getfilename():
    if len(sys.argv) == 1:
        return "cppmake.txt"
    elif len(sys.argv) == 2:
        return sys.argv[1]
    else:
        quit()

def addtoArr(arr, templ, s):
    dirs = s.split(',')
    for d in dirs:
        arr.append(templ % d.strip())


def replaceTempl(templ, flag, arr):
    return templ.replace('{%s}' % flag, ' '.join(arr))


def getparam(line):
    line = line.strip()
    for k, v in templ_map.items():
        kl, tmpl, arr = v
        key = line[:kl]
        if key == k:
            addtoArr(arr, tmpl, line[kl:])

def proc_cppmake(fn):
    if fn in proced_files:
        return

    fd = open(fn, "rb")
    if not fd:
        print("no inputfile")
        quit()

    txt = fd.read()
    fd.close()
    cmdlines = txt.split('\n')

    for line in cmdlines:
        line = line.strip()
        getparam(line)

    proced_files.add(fn)

    proc_import()

def proc_import():
    global import_files
    temp = import_files
    import_files = []
    
    while True:
        for fn in temp:
            #print('proc import %s' % fn)
            proc_cppmake(fn)
        if not import_files:
            break

def proc_something():
    arr = out[-1:][0]
    oup = arr.split('/')
    oup.pop()
    outpath.append('/'.join(oup))


def export_Makefile():
    fd = open("Makefile", "wb+")
    result = TEMPL
    for tr in templ_table:
        if tr[3] == 0:
            result = replaceTempl(result, tr[0], tr[2])
        else:
            result = replaceTempl(result, tr[0], tr[2][-1:])

    fd.write(result)
    fd.close()

if __name__ == "__main__":
    fn = getfilename()
    proc_cppmake(fn)
    proc_something()
    export_Makefile()
