CC=mipsel-linux-gnu-gcc-5
OBJCOPY=mipsel-linux-gnu-objcopy
AS=mipsel-linux-gnu-as
LD=mipsel-linux-gnu-ld

# TODO: is -G0 necessary?
CFLAGS=-fPIE  -nostdlib -march=4kc -mno-mips16 -mno-gpopt -mcode-readable=yes -fno-builtin -G0 -Os -fno-toplevel-reorder -mgp32 -mabi=32 -mabicalls
ASFLAGS=-march=m4k -KPIC -G0

all: test.bin

test.elf: test.o eken.ld apploader.o eken_api.o
	$(LD) -T eken.ld -o test.elf test.o

test.bin: test.elf
	$(OBJCOPY) -O binary --only-section=.text test.elf test.bin

upload: test.bin
	curl -T $^ ftp://192.168.1.1

clean:
	rm -f *.bin *.o *.elf

info: test.elf
	mipsel-linux-gnu-readelf -a $^
	mipsel-linux-gnu-size $^
	mipsel-linux-gnu-objdump -d --reloc $^


.PHONY: all info clean upload
