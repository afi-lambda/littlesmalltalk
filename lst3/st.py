from __future__ import print_function
import cffi

ffi = cffi.FFI()
ffi.set_source('lst3_def', None)
ffi.cdef("void initMemoryManager();")
ffi.cdef("FILE *fopen(char*, char*);")
ffi.cdef("size_t fread(void*, size_t, size_t, FILE*);")
ffi.cdef("void imageRead(FILE*);")
ffi.cdef("void initCommonSymbols();")
ffi.cdef("typedef int object;")
ffi.cdef("object symbols;")
ffi.cdef("object nameTableLookup(object, char*);")
ffi.cdef("typedef int boolean;")
ffi.cdef("boolean execute(object, int);")
ffi.cdef("struct dummy {int di; object cl; short ds;} dummyObject;")
ffi.cdef("""struct objectStruct {
    object cl;
    short referenceCount;
    short size;
    object *memory;};""")
ffi.cdef("struct objectStruct objectTable[6500];")
ffi.cdef("object *mBlockAlloc(int);")
ffi.cdef("void visit(object);")
ffi.cdef("void setFreeLists();")
ffi.cdef("")
ffi.cdef("")
ffi.cdef("")
ffi.compile()

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
            size = (-size + 1) / 2
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
fp = lst3.fopen("systemImage", "r")
image_read(fp)
lst3.initCommonSymbols()
firstProcess = lst3.nameTableLookup(lst3.symbols, "systemProcess");

while True:
    lst3.execute(firstProcess, 15000)
