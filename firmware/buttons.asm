; ========================================
; BUTTON BYTE 1
; ========================================
; Bit0 = UP
; Bit1 = DOWN
; Bit2 = LEFT
; Bit3 = RIGHT
; Bit4 = A
; Bit5 = B
; Bit6 = X
; Bit7 = Y
; ========================================

READ_BUTTONS_1:

    MOV A, #00H

CHECK_UP:
    JB UP_BTN, CHECK_DOWN
    ORL A, #01H

CHECK_DOWN:
    JB DOWN_BTN, CHECK_LEFT
    ORL A, #02H

CHECK_LEFT:
    JB LEFT_BTN, CHECK_RIGHT
    ORL A, #04H

CHECK_RIGHT:
    JB RIGHT_BTN, CHECK_A
    ORL A, #08H

CHECK_A:
    JB A_BTN, CHECK_B
    ORL A, #10H

CHECK_B:
    JB B_BTN, CHECK_X
    ORL A, #20H

CHECK_X:
    JB X_BTN, CHECK_Y
    ORL A, #40H

CHECK_Y:
    JB Y_BTN, END_B1
    ORL A, #80H

END_B1:
    RET


; ========================================
; BUTTON BYTE 2
; ========================================
; Bit0 = L1
; Bit1 = R1
; Bit2 = L2
; Bit3 = R2
; Bit4 = START
; Bit5 = SELECT
; Bit6 = HOME
; ========================================

READ_BUTTONS_2:

    MOV A, #00H

CHECK_L1:
    JB L1_BTN, CHECK_R1
    ORL A, #01H

CHECK_R1:
    JB R1_BTN, CHECK_L2
    ORL A, #02H

CHECK_L2:
    JB L2_BTN, CHECK_R2
    ORL A, #04H

CHECK_R2:
    JB R2_BTN, CHECK_START
    ORL A, #08H

CHECK_START:
    JB START_BTN, CHECK_SELECT
    ORL A, #10H

CHECK_SELECT:
    JB SELECT_BTN, CHECK_HOME
    ORL A, #20H

CHECK_HOME:
    JB HOME_BTN, END_B2
    ORL A, #40H

END_B2:
    RET
