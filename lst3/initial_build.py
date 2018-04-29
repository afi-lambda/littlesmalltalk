from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("_initial", """
    // passed to the real C compiler
    #include "source/env.h"
    #include "source/memory.h"
    #include "source/names.h"
    static void incr_w(object o) { incr(o); }
    static void basicAtPut_w(object x, int i,object y) { basicAtPut(x, i, y); }
    static void setClass_w(object o, object c) { setClass(o, c); }
    void setInstanceVariables(object);
    int parse(object, char*, int);
    object newInteger_w(int i) { return newInteger(i); }
    void fileIn(FILE*, int);
    """,
    libraries=['lst3'],
    library_dirs=['.'])   

ffibuilder.cdef("""     // lst3 declaration
    void initMemoryManager(void);
    typedef int object;
    object allocObject(int);
    object symbols;
    void incr_w(object o);
    void basicAtPut_w(object x, int i,object y);
    object newSymbol(char*);
    object newClass(char*);
    void setClass_w(object, object);
    #define nilobj ...
    void nameTableInsert(object, int, object, object);
    int strHash(char*);
    object trueobj;
    object falseobj;
    void initCommonSymbols(void);
    object newMethod(void);
    void setInstanceVariables(object);
    int parse(object, char*, int);
    #define processSize ...
    #define stackInProcess ...
    #define stackTopInProcess ...
    #define linkPtrInProcess ...
    object newInteger_w(int);
    int execute(object, int);
    FILE *fopen(char*, char*);
    int fclose(FILE*);
    void fileIn(FILE*, int);
""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)