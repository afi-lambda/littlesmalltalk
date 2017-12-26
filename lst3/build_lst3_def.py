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
ffibuilder.cdef("object allocObject(int);")
ffibuilder.cdef("object newSymbol(char*);")
ffibuilder.cdef("object newClass(char*);")
ffibuilder.cdef("")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)