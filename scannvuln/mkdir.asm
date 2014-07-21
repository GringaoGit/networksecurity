section	.text
    global _start

_start:
	pop ebx				;argc
	pop ebx				; prog name
	pop ebx  			; dir name
	pop ecx  			; chmod number ex : 666

	push ecx			;  save rule string address ( ex : 666)
	xor edx, edx 		;  count var to 0
	call string_size

	pop ecx 			; reinit ecx to string address
	push ecx			; save rule string address
	push ebx			; save dir name string address
	xor ebx, ebx  		; count var to 0
	call atoi

	sub ecx, ebx 		; return adress on string converted
	mov eax, 60
	int 80h

	pop ebx
 	mov eax, 39
	int 80h

	call exit

exit:

	mov eax, 1
	int 0x80

string_size:

	mov al, byte [ecx] 
	inc ecx	; offset on string
	inc edx ; count
	or eax, eax
	jnz string_size
	ret


; before calling this function :
; edx is strlen()
; ecx is pointer on string to convert into int
; ebx must be saved 
atoi:
	sub byte [ecx], 48
	inc ebx		; count+1
	inc ecx 	; offset on string
	cmp ebx, edx
	jne atoi
	ret
