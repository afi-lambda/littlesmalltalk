from __future__ import print_function
from build_lst3_def import ffibuilder
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
