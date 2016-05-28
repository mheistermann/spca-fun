#include "eken.h"

// Firmware version H9.05.10.2015
_API_CALL(uart_putchar, 0x804e4958);
_API_CALL(uart_printf, 0x804e4b54);
//_API_CALL(snprintf, 0x804e48f0);
_API_CALL(malloc, 0x804d2cc4);
_API_CALL(system, 0x8021b1f0);

#define DEBUG_PUTCHAR(x) \
    "   li $t9, 0x804e4958 #uart_putchar\n" \
    "   jalr $t9 # putchar\n" \
    "   li $a0, " #x "\n" 

