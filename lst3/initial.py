from _initial import ffi, lib

def makeInitialImage():
    # first create the table, without class links
    lib.symbols = lib.allocObject(1)
    lib.incr_w(lib.symbols)
    hashTable = lib.allocObject(3 * 53)
    lib.basicAtPut_w(lib.symbols, 1, hashTable)
    # next create #Symbol, Symbol and Class
    symbolObj = lib.newSymbol(b"Symbol")
    symbolClass = lib.newClass(b"Symbol")
    lib.setClass_w(symbolObj, symbolClass)
    classClass = lib.newClass(b"Class")
    lib.setClass_w(symbolClass, classClass)
    lib.setClass_w(classClass, classClass)
    # now fix up classes for symbol table */
    # and make a couple common classes, just to hold their places */
    lib.newClass(b"Link")
    lib.newClass(b"ByteArray")
    lib.setClass_w(hashTable, lib.newClass(b"Array"))
    lib.setClass_w(lib.symbols, lib.newClass(b"Dictionary"))
    lib.setClass_w(lib.nilobj, lib.newClass(b"UndefinedObject"))
    lib.newClass(b"String")
    lib.nameTableInsert(lib.symbols, lib.strHash(b"symbols"), 
    				    lib.newSymbol(b"symbols"), lib.symbols)
    # finally at least make true and false to be distinct */
    lib.trueobj = lib.newSymbol(b"true")
    lib.nameTableInsert(lib.symbols, lib.strHash(b"true"), lib.trueobj, lib.trueobj)
    lib.falseobj = lib.newSymbol(b"false")
    lib.nameTableInsert(lib.symbols, lib.strHash(b"false"), lib.falseobj, lib.falseobj)


if __name__ == "__main__":
	lib.initMemoryManager()
	makeInitialImage()
	lib.initCommonSymbols();

