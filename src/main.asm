%define MAGIC_NUMBER 0x7C00
%define ENDL 0x0D, 0x0A

org MAGIC_NUMBER
bits 16

start:
    jmp main

;
; Вывод строки на экран
; Параметры:
; - ds:si указывает на строку
;
puts:
    ; Сохранение модифицируемого регистра
    push si
    push ax
    push bx

.loop
    lodsb
    or al, al
    jz .done

    mov ah, 0x0E
    mov bh, 0
    int 0x10

    jmp .loop

.done
    pop bx
    pop ax
    pop si
    ret

main:
    ; Настройка сегмента данных
    mov ax, 0
    mov ds, ax
    mov es, ax

    ; Настройка стека
    mov ss, ax
    mov sp, MAGIC_NUMBER

    ; Вывод сообщения
    mov si, msg_hello
    call puts

    hlt

.halt:
    jmp .halt

msg_hello: db 'Hello, World!', ENDL, 0

times 510 - ($ - $$) db 0
dw 0AA55h
