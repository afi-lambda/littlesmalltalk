from _initial import ffi, lib
from glob import glob

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

def goDoIt(method_text):
    print(method_text)
    method = lib.newMethod()
    lib.incr_w(method)
    lib.setInstanceVariables(lib.nilobj)
    lib.parse(method, method_text, False)
    # create process and stack
    process = lib.allocObject(lib.processSize)
    lib.incr_w(process)
    stack = lib.allocObject(50)
    lib.incr_w(stack)
    # make a process
    lib.basicAtPut_w(process, lib.stackInProcess, stack)
    lib.basicAtPut_w(process, lib.stackTopInProcess, lib.newInteger_w(10))
    lib.basicAtPut_w(process, lib.linkPtrInProcess, lib.newInteger_w(2))
    # put argument on stack
    lib.basicAtPut_w(stack, 1, lib.nilobj)   # argument
    # now make a linkage area in stack
    lib.basicAtPut_w(stack, 2, lib.nilobj)            # previous link
    lib.basicAtPut_w(stack, 3, lib.nilobj)            # context object (nil = stack)
    lib.basicAtPut_w(stack, 4, lib.newInteger_w(1))   # return point
    lib.basicAtPut_w(stack, 5, method)                # method
    lib.basicAtPut_w(stack, 6, lib.newInteger_w(1))   # byte offset
    # now go execute it
    while (lib.execute(process, 15000)):
        print("...")

if __name__ == "__main__":
	lib.initMemoryManager()
	makeInitialImage()
	lib.initCommonSymbols();
	bootstrap_files = glob("bootstrap/*.st")
	for each in bootstrap_files:
		method = "x <120 1 '{}' 'r'>. <123 1>. <121 1>".format(each)
		goDoIt(method)
	goDoIt("x nil initialize")