from cffi import FFI

ffi = FFI()
ffi.cdef("int main(int argc, char **argv);")
C = ffi.dlopen("./lst3")
argv_keepalive = [ffi.new("char[]", "arg0")]
argv = ffi.new("char *[]", argv_keepalive)
C.main(1, argv)
