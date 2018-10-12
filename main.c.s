.globl _main
_main:
	movl	$2, %eax
	pushl	%eax
	movl	$3, %eax
	popl	%ecx
	addl	%ecx, %eax
	pushl	%eax
	movl	$3, %eax
	pushl	%eax
	movl	$10, %eax
	popl	%ecx
	movl	$0, %edx
	idivl	%ecx
	pushl	%eax
	movl	$6, %eax
	pushl	%eax
	movl	$3, %eax
	popl	%ecx
	imul	%ecx, %eax
	popl	%ecx
	addl	%ecx, %eax
	popl	%ecx
	subl	%ecx, %eax
	pushl	%eax
	movl	$1, %eax
	pushl	%eax
	movl	$5, %eax
	popl	%ecx
	subl	%ecx, %eax
	popl	%ecx
	addl	%ecx, %eax
	pushl	%eax
	movl	$1, %eax
	popl	%ecx
	addl	%ecx, %eax
	pushl	%eax
	movl	$1, %eax
	popl	%ecx
	addl	%ecx, %eax
	ret
	
