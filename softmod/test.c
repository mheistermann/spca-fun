#include "eken.h"
int test_bss;

char helloworld_static[] = "hello world static %u!\n";

void _test_printf(int arg) {
    for(int i=0;i<arg;i++) {
        uart_printf(helloworld_static, i);
    }
}
DEFINE_ENTRYPOINT(ep_test_printf, _test_printf);

void _test_printf_ro(int arg) {
    for(int i=0;i<arg;i++) {
        uart_printf("hello world #%u!\n", i);
    }
}
DEFINE_ENTRYPOINT(ep_test_printf_ro, _test_printf_ro);

void _test_putchar(int arg) {
    for(int i=0;i<arg;i++) {
        uart_putchar('A');
    }
}
DEFINE_ENTRYPOINT(EP_test_putchar, _test_putchar);
