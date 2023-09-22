.code16
.global start

.text
start:
	ljmp $0x0, $real_start

real_start:
	movw $0, %ax
	movw %ax, %ds
	movw %ax, %ss

	movw $0x7c00, %sp
	addw $0x0400, %sp

	movw $0xB800, %ax
	movw %ax, %es
	movw $data, %si
	movw $0, %di
	movw size, %cx
	call memcpy

loop:
	jmp loop

memcpy:
	testw %cx, %cx
	jz out

again:
	movb (%si), %ah
	movb %ah, %es:(%di)
	incw %si
	incw %di
	decw %cx
	jnz again
out:
	ret

data:
	.asciz "H\017e\017l\017l\017o\017!\017"
size:
	.short . - data
