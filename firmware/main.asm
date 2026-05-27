INCLUDE REG51.INC

ORG 0000H

MAIN:

    ACALL UART_INIT

MAIN_LOOP:

; ======================================
; SEND BUTTON BYTE 1
; ======================================

    ACALL READ_BUTTONS_1
    ACALL UART_SEND

; ======================================
; SEND BUTTON BYTE 2
; ======================================

    ACALL READ_BUTTONS_2
    ACALL UART_SEND

; ======================================
; SEND JOYSTICK VALUES
; ======================================

    ACALL READ_LX
    ACALL UART_SEND

    ACALL READ_LY
    ACALL UART_SEND

    ACALL READ_RX
    ACALL UART_SEND

    ACALL READ_RY
    ACALL UART_SEND

; ======================================
; SMALL DELAY
; ======================================

    ACALL DELAY

    SJMP MAIN_LOOP

END
