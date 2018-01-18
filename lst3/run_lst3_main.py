from cffi import FFI

ffi = FFI()
ffi.cdef("int main(int argc, char **argv);")
C = ffi.dlopen("./liblst3.so")
argv_keepalive = [ffi.new("char[]", b"arg0")]
argv = ffi.new("char *[]", argv_keepalive)
C.main(1, argv)
