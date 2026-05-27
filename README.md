# DualShock Series X

> A fully custom breadboard gaming controller built using the 8051 microcontroller, pure assembly language, UART serial communication, and several terrible engineering decisions.

![Controller](hardware/DualShockSeriesX.png)

---

# Overview

DualShock Series X is a homemade gaming controller architecture designed entirely around the classic 8051 microcontroller platform.
Unlike modern controllers that rely on dedicated USB controller ICs, high-speed ARM processors, or prebuilt firmware libraries, this project directly interfaces physical hardware with low-level assembly firmware running on an AT89S52.

The controller handles:
- 13 digital inputs
- Dual analog joystick support
- Real-time UART packet transmission
- Custom serial protocol
- Expandable embedded firmware structure

The entire system was intentionally designed using:
- raw GPIO polling
- software timing delays
- manual packet construction
- direct register manipulation
- zero abstraction layers

---

# Project Goals

This project was built to explore:
- low-level embedded systems
- hardware-software interfacing
- serial communication protocols
- assembly-level firmware architecture
- controller input systems
- real-time polling systems

The goal was not efficiency.

The goal was making an actual working controller using one of the oldest microcontroller architectures still alive in engineering labs.

---

# Hardware Architecture

## Core Microcontroller

| Component | Description |
|---|---|
| MCU | AT89S52 / 8051 |
| Architecture | 8-bit |
| Clock Speed | 11.0592 MHz |
| RAM | 256 bytes |
| Flash | 8 KB |
| Communication | UART Serial |

The AT89S52 was selected because:
- native UART support
- extremely simple architecture
- direct register-level access
- huge educational value
- absurdly funny choice for a controller

---

# Controller Layout

## Digital Inputs

### D-Pad
- Up
- Down
- Left
- Right

### Face Buttons
- A
- B
- X
- Y

### Shoulder Buttons
- L1
- R1
- L2
- R2

### System Controls
- Start
- Select
- Home

Total:
- 13 physical buttons

---

# Analog Joystick System

The controller supports:
- Left Analog Stick (X/Y)
- Right Analog Stick (X/Y)

Each joystick outputs:
- horizontal axis
- vertical axis

The 8051 does not contain an internal ADC.

Because of this, external ADC hardware is required.

---

## Planned ADC Configuration

| Component | Purpose |
|---|---|
| ADC0804 | Analog to digital conversion |
| Joystick Module | Analog axis generation |
| 8051 | Digital packet transmission |

The firmware architecture already contains placeholder routines for:
- LX
- LY
- RX
- RY

Current test firmware uses:
```asm
MOV A, #080H
```

as a centered joystick value.

---

# Firmware Architecture

The firmware is split into modular assembly files.

```txt
firmware/
│
├── REG51.INC
├── buttons.asm
├── delay.asm
├── joystick.asm
├── macros.inc
├── main.asm
├── uart.asm
└── vectors.asm
```

---

# Firmware Modules

## `main.asm`

Main controller loop.

Responsible for:
- initializing UART
- reading inputs
- transmitting packets
- timing control

Main execution loop:

```asm
MAIN_LOOP:

    ACALL READ_BUTTONS_1
    ACALL UART_SEND

    ACALL READ_BUTTONS_2
    ACALL UART_SEND

    ACALL READ_LX
    ACALL UART_SEND

    ACALL READ_LY
    ACALL UART_SEND

    ACALL READ_RX
    ACALL UART_SEND

    ACALL READ_RY
    ACALL UART_SEND

    ACALL DELAY

SJMP MAIN_LOOP
```

The controller continuously transmits state packets in real time.

---

## `buttons.asm`

Handles all digital button polling.

The firmware uses:
- direct GPIO reads
- bit masking
- manual packet encoding

Example:

```asm
JB UP_BTN, CHECK_DOWN
ORL A, #01H
```

If the button is pressed:
- the corresponding bit is enabled
- the packet is updated

---

## `uart.asm`

Handles serial communication.

The UART module:
- configures timer mode
- sets baud rate
- enables serial transmission
- transmits packets

Configuration:

```asm
MOV TMOD, #20H
MOV TH1, #0FDH
MOV SCON, #50H
SETB TR1
```

This initializes:
- UART Mode 1
- 9600 baud communication
- 8-bit serial transfer

---

## `delay.asm`

Implements software timing delays using nested decrement loops.

No hardware timers are used for delays.

Because using software loops felt more authentic.

---

## `joystick.asm`

Contains joystick reading routines.

Current implementation:
- placeholder analog values
- centered axis simulation

Planned upgrade:
- ADC0804 integration
- real analog reads
- dynamic axis calibration

---

# UART Communication Protocol

The controller transmits 6 bytes continuously.

| Byte | Purpose |
|---|---|
| 1 | D-pad + face buttons |
| 2 | shoulder + system buttons |
| 3 | Left Stick X |
| 4 | Left Stick Y |
| 5 | Right Stick X |
| 6 | Right Stick Y |

---

# Packet Structure

## Byte 1

| Bit | Function |
|---|---|
| 0 | UP |
| 1 | DOWN |
| 2 | LEFT |
| 3 | RIGHT |
| 4 | A |
| 5 | B |
| 6 | X |
| 7 | Y |

---

## Byte 2

| Bit | Function |
|---|---|
| 0 | L1 |
| 1 | R1 |
| 2 | L2 |
| 3 | R2 |
| 4 | START |
| 5 | SELECT |
| 6 | HOME |

---

# PC Receiver

The project also includes:
```txt
pc_receiver/serial_reader.py
```

This Python script:
- reads UART packets
- decodes controller state
- prints active buttons
- displays joystick values

Communication pipeline:

```txt
8051 -> UART -> USB Serial Adapter -> Python Receiver
```

---

# Timing System

The controller currently uses:
- polling-based input scanning
- software delay loops
- sequential packet transmission

Advantages:
- simple debugging
- predictable execution
- easy firmware analysis

Disadvantages:
- inefficient CPU usage
- blocking delays
- no interrupt prioritization

Future firmware versions may include:
- timer interrupts
- buffered transmission
- interrupt-driven polling
- packet synchronization

---

# Assembly Design Philosophy

This project intentionally avoids:
- C firmware
- external frameworks
- abstraction layers
- optimization-heavy code

The goal was readability and low-level control.

The firmware is intentionally:
- verbose
- modular
- easy to follow
- beginner readable
- hardware focused

This is closer to how older embedded systems were actually developed.

## Analog Input on 8051

The original 8051 architecture has:
- no ADC
- limited RAM
- limited registers

Adding dual analog sticks required:
- external ADC planning
- packet expansion
- multi-byte synchronization

---

## Real-Time Input Polling

The controller must:
- scan inputs
- build packets
- transmit serial data
- maintain timing consistency

all while running on:
- 8-bit architecture
- minimal RAM
- assembly-only firmware


---

# Build Tools

| Tool | Purpose |
|---|---|
| Keil uVision | Assembly compilation |
| ProgISP | Firmware flashing |
| Python | Packet monitoring |
| UART Adapter | Serial communication |

---



# Made by C.Kumaran
