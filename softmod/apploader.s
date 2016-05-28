.set push
.section .text.apploader
.global EP_apploader
.ent EP_apploader
.type EP_apploader, @function
.set noreorder
EP_apploader:
   subu $sp, $sp, 64
   sw $ra, 16($sp)
   sw $s0, 20($sp)
   sw $s1, 24($sp)
   sw $s2, 28($sp)
   sw $s3, 32($sp)
   bal .Lgetpc
   nop
.Lgetpc:
   subu $s0, $ra, .-EP_apploader # assume EP_apploader @ 0, trust linker script
   li $s1, _GLOBAL_OFFSET_TABLE_+2*4 # skip first 2 reserved entries
   addu $s1, $s0, $s1
   li $s2, __got_end
   addu $s2, $s0, $s2
.Lnext:
   beq $s1, $s2, .Lfinished
   nop
   lw $a0, ($s1)
   addu $a0, $a0, $s0
   sw $a0, ($s1)
   b .Lnext
   addu $s1, $s1, 4
   
.Lfinished:
.Lzero_bss:
   li $s1, __bss_start
   li $s2, __bss_end
   addu $s1, $s1, $s0
   addu $s2, $s2, $s0
.Lzero_loop:
   sw $zero, ($s1)
   bne $s1, $s2, .Lzero_loop
   addu $s1, $s1, 4
.Lout:
   lw $ra, 16($sp)
   lw $s0, 20($sp)
   lw $s1, 24($sp)
   lw $s2, 28($sp)
   lw $s3, 32($sp)
   jr $ra
   addu $sp, $sp, 64
   nop
.end EP_apploader
.size EP_apploader, .-EP_apploader
.set pop



