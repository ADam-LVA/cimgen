
DIR := $(shell pwd)

all: build-cpp cimpp run

cimpp:
	mkdir cimpp

cimpy:
	mkdir cimpy

build-cpp:
	docker build -t cim-codebase-generator . -f Dockerfile.cpp

build-python: cimpy
	docker build -t cim-codebase-generator-python -f Dockerfile.python .
	docker run -v ${DIR}/cimpy:/cim-codebase-generator/main/cgmes_v2_4_15 \
		   -v ${DIR}/cgmes_schema/cgmes_v2_4_15_schema:/cgmes_schema/cgmes_v2_4_15_schema \
	           cim-codebase-generator-python

clean:
	find cimpp -type f -exec rm -f {} \;

run:
	cp -a cached_files/* cimpp
	docker run -v ${DIR}/cimpp:/cim-codebase-generator/main/cgmes_v2_4_15 -v ${DIR}/cgmes_schema/cgmes_v2_4_15_schema:/cgmes_schema/cgmes_v2_4_15_schema cim-codebase-generator
	cd cimpp && echo "#ifndef IEC61970_H\n#define IEC61970_H" > IEC61970.hpp
	cd cimpp && find . -iname "*.hpp" | grep -v Folders | grep -v Task | grep -v IEC61970 | grep -v ConformLoad | sed "s/\.\///" | sed "s/\(.*\)/#include \"\1\"/" >> IEC61970.hpp
	cd cimpp && echo "\n#endif" >> IEC61970.hpp
	cd cimpp && echo "\nstatic std::unordered_map<std::string, BaseClass* (*)()> initialize() {" >> CIMFactory.cpp
	cd cimpp && echo "\n    std::unordered_map<std::string, BaseClass* (*)()> map;" >> CIMFactory.cpp
	cd cimpp && find . -iname "*.hpp" | grep -v assignments | grep -v Folders | grep -v "./Task" | grep -v IEC61970 | grep -v ConformLoad | grep -v Factory | grep -v String | grep -v BaseClass | sort | sed "s/\.\///" | sed "s/\.hpp//" | sed "s/\(.*\)/    map.insert(std::make_pair(\"\1\", \&&_factory));/" >> CIMFactory.cpp
	cd cimpp && echo "    return map;" >> CIMFactory.cpp
	cd cimpp && echo "};" >> CIMFactory.cpp

.PHONY:
	build-cpp build-python clean run

