from __future__ import print_function
import cffi

ffibuilder = cffi.FFI()
ffibuilder.set_source('lst3_def', None)
ffibuilder.cdef("void initMemoryManager();")
ffibuilder.cdef("FILE *fopen(char*, char*);")
ffibuilder.cdef("size_t fread(void*, size_t, size_t, FILE*);")
ffibuilder.cdef("void imageRead(FILE*);")
ffibuilder.cdef("void initCommonSymbols();")
ffibuilder.cdef("typedef int object;")
ffibuilder.cdef("object symbols;")
ffibuilder.cdef("object nameTableLookup(object, char*);")
ffibuilder.cdef("typedef int boolean;")
ffibuilder.cdef("boolean execute(object, int);")
ffibuilder.cdef("struct dummy {int di; object cl; short ds;} dummyObject;")
ffibuilder.cdef("""struct objectStruct {
    object cl;
    short referenceCount;
    short size;
    object *memory;};""")
ffibuilder.cdef("struct objectStruct objectTable[6500];")
ffibuilder.cdef("object *mBlockAlloc(int);")
ffibuilder.cdef("void visit(object);")
ffibuilder.cdef("void setFreeLists();")
ffibuilder.cdef("")
ffibuilder.cdef("")
ffibuilder.cdef("")
ffibuilder.compile()

from lst3_def import ffi

def image_read(fp):
    addressof_symbols = ffi.addressof(lst3, "symbols")
    sizeof_object = ffi.sizeof("object")
    lst3.fread(addressof_symbols, sizeof_object, 1, fp)
    addressof_dummy_object = ffi.addressof(lst3, "dummyObject")
    sizeof_dummy_object = ffi.sizeof("struct dummy")
    loop_count = 0
    while lst3.fread(addressof_dummy_object, sizeof_dummy_object, 1, fp):
        index = lst3.dummyObject.di
        cl = lst3.dummyObject.cl
        read_size = lst3.dummyObject.ds
        #print("{:4d} {:4d} {:4d} ".format(index << 1, cl, read_size))
        assert 0 <= index < 6500, "reading index out of range: {}".format(index)
        assert 0 <= cl >> 1 < 6500, "reading class out of range: {}".format(cl)
        lst3.objectTable[index].cl = cl
        lst3.objectTable[index].size = read_size
        size = read_size
        if size < 0:
            size = (-size + 1) // 2
        if size > 0:
            addressof_memory = lst3.mBlockAlloc(size)
            lst3.objectTable[index].memory = addressof_memory
            lst3.fread(addressof_memory, size * sizeof_object, 1, fp)
        else:
            lst3.objectTable[index].memory = ffi.cast("object *", 0)
    lst3.visit(lst3.symbols)
    lst3.setFreeLists()

lst3 = ffi.dlopen("./lst3")
lst3.initMemoryManager()
fp = lst3.fopen(b"systemImage", b"r")
image_read(fp)
lst3.initCommonSymbols()
firstProcess = lst3.nameTableLookup(lst3.symbols, b"systemProcess");

while True:
    lst3.execute(firstProcess, 15000)
