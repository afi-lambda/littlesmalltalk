CC = gcc
LIBS = -lm
default:
	cd source && $(CC) -fPIC  -Wno-nonnull -c memory.c names.c news.c interp.c primitive.c filein.c lex.c parser.c unixio.c st.c initial.c tty.c
	cd source && $(CC) memory.o names.o news.o interp.o primitive.o filein.o lex.o parser.o unixio.o st.o tty.o -o ../liblst3.so -pie -Wl,--export-dynamic
	cd source && $(CC) memory.o names.o news.o interp.o primitive.o filein.o lex.o parser.o unixio.o initial.o tty.o -o ../buildImage
	cd bootstrap && ../buildImage basic.st mag.st collect.st file.st mult.st tty.st
	mv bootstrap/systemImage .

clean:
	rm -f source/*.o liblst3.so buildImage systemImage
	rm -rf *.pyc __pycache__ _initial.* lst3_def.py
	rm -f `find . | grep \~`

install:
	mkdir -p /usr/share/lst3
	cp systemImage /usr/share/lst3
	cp lst3 /usr/bin
