P0      EQU 080H
P1      EQU 090H
P2      EQU 0A0H
P3      EQU 0B0H

TMOD    EQU 089H
TH1     EQU 08DH
SCON    EQU 098H
SBUF    EQU 099H
TCON    EQU 088H

TR1     BIT 08EH
TI      BIT 099H

; =========================
; D-PAD
; =========================

UP_BTN         BIT 090H
DOWN_BTN       BIT 091H
LEFT_BTN       BIT 092H
RIGHT_BTN      BIT 093H

; =========================
; FACE BUTTONS
; =========================

A_BTN          BIT 0A0H
B_BTN          BIT 0A1H
X_BTN          BIT 0A2H
Y_BTN          BIT 0A3H

; =========================
; SHOULDER BUTTONS
; =========================

L1_BTN         BIT 0B0H
R1_BTN         BIT 0B1H
L2_BTN         BIT 0B2H
R2_BTN         BIT 0B3H

; =========================
; SYSTEM BUTTONS
; =========================

START_BTN      BIT 0B4H
SELECT_BTN     BIT 0B5H
HOME_BTN       BIT 0B6H
