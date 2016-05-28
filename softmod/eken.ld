OUTPUT_FORMAT("elf32-tradlittlemips")
OUTPUT_ARCH(mips)

STARTUP(apploader.o)
INPUT(eken_api.o)
ENTRY(EP_apploader)
SECTIONS
{
  . = 0x0;
  .text : {
    *(.text.apploader)
    *(.text)
    *(.data)
    *(.rodata)
    *(.rodata.*)
  /*.got :*/
      . = ALIGN(4);
      *(.got)
      __got_end = .;

  /*.bss : */
      . = ALIGN(4);
      __bss_start = .;
      *(.sbss.*)
      *(.bss.*)
      *(COMMON)
      . = ALIGN(4);
      __bss_end = .;
    }

  /DISCARD/ : {
      *(.reginfo)
      *(.pdr)
      *(.comment)
      *(.MIPS.abiflags)
      *(.gnu.attributes)
  }
}
