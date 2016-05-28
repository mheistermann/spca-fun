#ifndef EKEN_H_BKCRZZLW
#define EKEN_H_BKCRZZLW

#include <stddef.h>
#include <stdint.h>

int uart_putchar(char c);
int uart_printf(char* format, ...);
int snprintf(char *str, size_t size, char* format, ...);
void *malloc(size_t len);
void system(char *cmd);

struct FILE;
typedef struct FILE FILE;
FILE* posix_open(char *path, unsigned char mode);
FILE* posix_read(FILE *fp, void *buf, size_t len);
FILE* posix_write(FILE *fp, void *buf, size_t len);

struct __attribute__((packed)) file_info {
    unsigned char unk0[0x420];
    uint32_t size; 
    unsigned char unk422[0x34];
};
FILE* posix_finfo(FILE *fp, struct file_info *buf);

#define EKEN_GP 0x806445e0
#define INT2STR(i) #i

// can't figure out how to make it find the 'NAME' symbol if this was
// defined before NAME. gives this error:
// /tmp/cco3HM5e.s:21: Error: operand 3 must be constant `add $t9,$ra,OFF'
// use -fno-toplevel-reorder

#define DEFINE_ENTRYPOINT(NAME, IMPL) _DEFINE_ENTRYPOINT(NAME, IMPL , EKEN_GP)
#define _DEFINE_ENTRYPOINT(NAME, IMPL, _EKEN_GP) \
asm ( \
    ".set push\n" \
    ".section .text\n" \
    "__ra_" #NAME ": nop #this is actually a storage locaton, .word 0xdeadbeef makes gcc fail\n" \
    ".global " #NAME "\n" \
    ".global " #IMPL "\n" \
    ".ent " #NAME "\n" \
    ".type " #NAME ", @function\n" \
    ".set noreorder\n" \
    #NAME ":\n" \
    "   move $t0, $ra\n" \
    "   bal .L_" #NAME "\n" \
    "   nop\n" \
    ".L_" #NAME ":\n" \
    ".set OFF_" #NAME ", " #IMPL "-.\n" \
    ".set RA_" #NAME ",__ra_" #NAME "-.\n" \
    "   addu $t9, $ra, OFF_" #NAME "\n" \
    "   addu $t1, $ra, RA_" #NAME "\n" \
    "   sw $t0, ($t1)\n" \
    "   move $ra, $t0\n" \
    "   jalr $t9\n" \
    "   nop\n" \
    "   bal .L2_" #NAME "\n" \
    "   nop\n" \
    ".L2_" #NAME ":\n" \
    ".set RA2_" #NAME ",__ra_" #NAME "-.\n" \
    "   addu $t1, $ra, RA2_" #NAME "\n" \
    "   lw $ra, ($t1)\n" \
    "   li $gp, " INT2STR(_EKEN_GP) "\n" \
    "   j $ra\n" \
    "   nop\n" \
    ".end " #NAME "\n" \
    ".size " #NAME ", .-" #NAME "\n" \
    "after_" #NAME ":\n" \
    ".set pop\n" \
    "\n" \
)

#define _API_CALL(NAME, ADDRESS) __API_CALL(NAME, ADDRESS, EKEN_GP)
#define __API_CALL(NAME, ADDRESS, _EKEN_GP) \
asm ( \
        ".set push\n" \
        ".section .text\n" \
        ".global " #NAME "\n" \
        ".ent " #NAME "\n" \
        ".type " #NAME ", @function\n" \
        ".set noreorder\n" \
        "" #NAME ":\n" \
        "li $t0, " INT2STR(ADDRESS) "\n" \
        "li $gp, " INT2STR(_EKEN_GP) "\n" \
        "jr $t0\n" \
        "nop\n" \
        ".end " #NAME "\n" \
        ".size " #NAME ", .-" #NAME "\n" \
        ".set pop\n" \
        )



#endif /* end of include guard: EKEN_H_BKCRZZLW */
