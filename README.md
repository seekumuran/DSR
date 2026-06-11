# Dual Shock Series X (DSSX)

> An experimental embedded input systems platform built on the 8051 microcontroller architecture.

---

## Table of Contents

1. [Overview](#overview)
2. [Why This Exists](#why-this-exists)
3. [Repository Layout](#repository-layout)
4. [System Architecture](#system-architecture)
5. [Hardware Architecture](#hardware-architecture)
6. [Firmware Design](#firmware-design)
   - [Scheduler System](#scheduler-system)
   - [Interrupt Architecture](#interrupt-architecture)
   - [Watchdog Infrastructure](#watchdog-infrastructure)
   - [Task Dispatch & Runtime Balancing](#task-dispatch--runtime-balancing)
   - [ADC Pipeline & Joystick Subsystem](#adc-pipeline--joystick-subsystem)
   - [Haptic Engine](#haptic-engine)
   - [Diagnostics Tracing](#diagnostics-tracing)
7. [DSSX Transport Protocol](#dssx-transport-protocol)
   - [Why a Custom Protocol](#why-a-custom-protocol)
   - [Packet Structure](#packet-structure)
   - [Fragmentation & Reassembly](#fragmentation--reassembly)
   - [CRC & Packet Validation](#crc--packet-validation)
   - [Retransmission Logic](#retransmission-logic)
   - [Runtime Recovery & Protocol Recovery](#runtime-recovery--protocol-recovery)
8. [UART Transport Layer](#uart-transport-layer)
9. [FPGA Acceleration Modules](#fpga-acceleration-modules)
   - [UART RX/TX Modules](#uart-rxtx-modules)
   - [FIFO Subsystem](#fifo-subsystem)
   - [CRC Engine](#crc-engine)
   - [Scheduler Timers](#scheduler-timers)
   - [PWM Engine](#pwm-engine)
   - [Hardware Filtering](#hardware-filtering)
10. [Middleware Architecture](#middleware-architecture)
    - [Runtime Management](#runtime-management)
    - [Packet Routing](#packet-routing)
    - [Stream Scheduling](#stream-scheduling)
    - [HID Translation Layer](#hid-translation-layer)
    - [Diagnostics Dashboard](#diagnostics-dashboard)
    - [Runtime Synchronization](#runtime-synchronization)
    - [Transport Layer Abstraction](#transport-layer-abstraction)
11. [Diagnostics Infrastructure](#diagnostics-infrastructure)
12. [Simulation Systems](#simulation-systems)
    - [Protocol Fuzzer](#protocol-fuzzer)
    - [Interrupt Storm Simulation](#interrupt-storm-simulation)
    - [Runtime Overload Tests](#runtime-overload-tests)
    - [Packet Corruption Scenarios](#packet-corruption-scenarios)
    - [Recovery Simulation](#recovery-simulation)
13. [SDK Ecosystem](#sdk-ecosystem)
    - [C SDK](#c-sdk)
    - [C++ SDK](#c-sdk-1)
    - [Python SDK](#python-sdk)
    - [Rust SDK](#rust-sdk)
14. [Benchmarking](#benchmarking)
15. [Design Tradeoffs](#design-tradeoffs)
16. [Future Roadmap](#future-roadmap)
17. [Engineering Notes](#engineering-notes)
18. [License](#license)

---

## Overview

**Dual Shock Series X** (DSSX) is an experimental platform for building, testing, and studying embedded input systems on constrained hardware. The project centers on the Intel MCS-51 (8051) microcontroller family — not because it's modern, but because working within its constraints forces discipline that higher-abstraction platforms often paper over.

The core of the project is a custom transport protocol (the DSSX protocol), a bare-metal assembly firmware runtime, and a layered middleware stack that bridges the firmware to host-side software. On top of that sits a small SDK ecosystem (C, C++, Python, Rust), a simulation suite for protocol and runtime stress testing, and an FPGA acceleration layer that handles latency-sensitive work the 8051 cannot do efficiently in firmware alone.

This is not a product. It's an engineering platform for studying how real embedded input systems behave under pressure — packet corruption, interrupt floods, runtime overloads, hardware noise on joystick lines, haptic timing drift. The goal is to understand these failure modes well enough to design around them.

The architecture has grown incrementally over time. Some decisions made early have caused downstream pain; those tradeoffs are documented honestly throughout this README and in `docs/`.

---

## Why This Exists

Most embedded input system tutorials operate at a comfortable abstraction level: use an Arduino library, call `analogRead()`, done. That's fine for prototypes. It doesn't prepare you for what happens when your ADC samples are jittered by PWM noise, your UART FIFO overruns under interrupt load, and your host-side HID driver starts dropping packets because the framing byte slipped.

DSSX was started to study exactly those problems — not simulate them in theory, but reproduce them deliberately and build the infrastructure to survive them.

The 8051 was chosen for several reasons:

- Its architecture is simple enough that firmware can be fully understood without a datasheet the size of a dictionary
- Its limited RAM (256 bytes on the base variant, expandable) forces genuine memory discipline
- Its interrupt model is straightforward but unforgiving under load
- It is still used in embedded peripherals, USB controllers, and industrial I/O — so lessons learned here translate

The FPGA layer exists because some timing requirements (CRC computation at line speed, clean PWM for haptic motors, hardware-level FIFO buffering) simply cannot be met by firmware alone on this class of microcontroller. Rather than switching to a more capable MCU and losing the constraint discipline, the platform offloads specific tasks to a small FPGA fabric sitting alongside the 8051.

---

## Repository Layout

```
dual-shock-series-x/
│
├── firmware/               # 8051 assembly + C firmware
│   ├── scheduler/          # Cooperative task scheduler
│   ├── watchdog/           # Watchdog timer management
│   ├── runtime/            # Runtime balancing, guards, task slots
│   ├── dispatch/           # Task dispatch tables and ISR routing
│   ├── protocol/           # DSSX packet builders, fragmentation, transport
│   ├── drivers/
│   │   ├── adc/            # ADC driver, sample averaging, noise floor
│   │   ├── joystick/       # Joystick normalization, deadzone, calibration
│   │   ├── haptic/         # PWM haptic output, pattern engine
│   │   └── uart/           # UART TX/RX, buffering, framing
│   ├── diagnostics/        # Firmware-side trace ring buffer, error codes
│   └── isr/                # Interrupt service routines
│
├── fpga/                   # HDL modules (Verilog)
│   ├── uart/               # UART RX and TX modules
│   ├── fifo/               # Synchronous FIFO, depth-configurable
│   ├── crc/                # CRC-16 CCITT engine
│   ├── timers/             # Scheduler heartbeat timers
│   ├── pwm/                # PWM generator for haptic output
│   └── filter/             # Hardware low-pass filter approximation
│
├── middleware/             # Host-side runtime (C, runs on Linux/Windows)
│   ├── runtime/            # Process and thread management
│   ├── router/             # Packet routing between layers
│   ├── stream/             # Stream scheduler, backpressure handling
│   ├── hid/                # HID translation, descriptor generation
│   ├── diagnostics/        # Dashboard, log ingestion, alert rules
│   ├── sync/               # Runtime synchronization primitives
│   └── transport/          # Transport abstraction (UART, simulated, mock)
│
├── sdk/
│   ├── c/                  # C SDK, low-level bindings
│   ├── cpp/                # C++ SDK, RAII wrappers, typed packets
│   ├── python/             # Python SDK, asyncio-based
│   └── rust/               # Rust SDK, async/await, strong typing
│
├── simulation/
│   ├── fuzzer/             # Protocol fuzzer, mutation engine
│   ├── storm/              # Interrupt storm injector
│   ├── overload/           # Runtime overload scenarios
│   ├── corruption/         # Packet corruption injection
│   └── recovery/           # Recovery path simulation and validation
│
├── diagnostics/            # Standalone diagnostics tools
│   ├── trace_viewer/       # Real-time firmware trace viewer
│   ├── packet_inspector/   # Packet capture and decode
│   └── runtime_profiler/   # Host-side runtime profiling
│
├── benchmarks/             # Benchmark suites
│   ├── latency/            # End-to-end latency benchmarks
│   ├── throughput/         # Packet throughput under load
│   ├── scheduler/          # Scheduler overhead measurement
│   └── recovery_time/      # Recovery latency benchmarks
│
├── hardware/               # Schematics, board notes, pin maps
│   ├── schematics/
│   ├── pinout/
│   └── bom/
│
├── docs/                   # Design documents, protocol specs, ADRs
│   ├── protocol_spec.md
│   ├── scheduler_design.md
│   ├── fpga_integration.md
│   ├── adr/                # Architecture Decision Records
│   └── tradeoffs.md
│
└── tools/                  # Build tools, flash utilities, helpers
    ├── flash/
    ├── codegen/
    └── lint/
```

---

## System Architecture

The platform is layered. Each layer has a defined responsibility and communicates with adjacent layers through explicit interfaces. Cross-layer shortcuts exist in a few places (mostly in the diagnostics path) and they are marked as technical debt in `docs/adr/`.

```
┌─────────────────────────────────────────────────────────────-┐
│                        HOST SOFTWARE                         │
│                                                              │
│   ┌───────────┐  ┌───────────┐  ┌──────────┐  ┌─────────┐    │
│   │  SDK      │  │   HID     │  │ Diag     │  │  Bench  │    │
│   │(C/C++/    │  │Translation│  │ Dashboard│  │  Suite  │    │
│   │ Py/Rust)  │  │           │  │          │  │         │    │
│   └─────┬─────┘  └─────┬─────┘  └────┬─────┘  └────┬────┘    │
│         │              │             │              │        │
│   ┌─────▼──────────────▼─────────────▼──────────────▼─────┐  │
│   │                 MIDDLEWARE RUNTIME                    │  │
│   │   Packet Router │ Stream Scheduler │ Transport Layer  │  │
│   └──────────────────────────┬────────────────────────────┘  │ 
└─────────────────────────────-┼───────────────────────────────┘
                               │  UART (physical or emulated)
┌─────────────────────────────-┼───────────────────────────────┐
│                    FPGA BOUNDARY                             │
│                             │                                │
│   ┌─────────┐  ┌─────────┐  │  ┌──────────┐  ┌──────────┐    │
│   │  UART   │  │  FIFO   │◄─┘  │   CRC    │  │   PWM    │    │
│   │ RX/TX   │  │ Buffer  │     │  Engine  │  │  Engine  │    │
│   └────┬────┘  └────┬────┘     └────┬─────┘  └────┬─────┘    │
│        └────────────┴──────────────┴──────────────┘          │
│                             │                                │
└─────────────────────────────┼───────────────────────────────-┘
                              │  Internal bus (SFR-mapped)
┌─────────────────────────────┼───────────────────────────────┐
│                    8051 FIRMWARE                            │
│                             │                               │
│  ┌──────────┐  ┌──────────┐ │ ┌──────────┐  ┌────────────┐  │
│  │ Scheduler│  │  ISR     │ │ │  DSSX    │  │  ADC /     │  │
│  │  + Tasks │  │  Handler │ │ │ Protocol │  │  Joystick  │  │
│  └──────────┘  └──────────┘ │ └──────────┘  └────────────┘  │
│  ┌──────────┐  ┌────────────▼───────────────────────────┐   │
│  │ Watchdog │  │           Runtime Guards               │   |
│  └──────────┘  └────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────-┼───────────────────────────────┐
│                    HARDWARE                                  │
│  Dual analog sticks │ Haptic motors │ Buttons │ Power rail   │
└──────────────────────────────-───────────────────────────────┘
```

Data flows upward from physical hardware through the 8051 firmware, across the FPGA boundary (which handles buffering and compute-intensive framing work), over UART to the host middleware, and finally up to the SDK or HID layer. Control flows downward: host sends configuration, haptic commands, and calibration data back into the firmware.

---

## Hardware Architecture

The hardware design is intentionally minimal. The goal is to keep the BOM small and the schematic readable.

```
Hardware Block Diagram

 ┌───────────────────────────────────────────────────────┐
 │                    Main PCB                           │
 │                                                       │
 │  [Analog Stick L]──┐                                  │
 │  [Analog Stick R]──┼──► [MUX] ──► [ADC Input / P1.x]  │
 │  [Buttons]─────────┘                                  │
 │                                                       │
 │  [8051 MCU]────────────────────────────────────────┐  │
 │      │ TXD/RXD (UART)                              │  │
 │      ▼                                             │  │
 │  [FPGA Module] ──► UART out ──► [USB-UART Bridge]  │  │
 │      │ PWM Out                                     │  │
 │      ▼                                             │  │
 │  [Haptic Driver] ──► [Motor L] [Motor R]           │  │
 │                                                    │  │
 │  [3.3V LDO] ──► MCU / FPGA / Peripherals           │  │
 └───────────────────────────────────────────────────────┘
```

Hardware files live in `hardware/`. Schematics are in KiCad format. The BOM is in `hardware/bom/bom.csv`.

**Key hardware choices and their reasoning:**

- **8051 at 11.0592 MHz**: This clock frequency divides evenly for standard UART baud rates (9600, 38400, 115200). This matters. An 8051 running at 12 MHz produces baud rate errors that cause intermittent framing failures, which are extremely tedious to debug. See `docs/adr/001-clock-selection.md`.

- **Analog mux before ADC**: The base 8051 has limited ADC inputs. A 74HC4051 analog multiplexer in front of the ADC lets both joystick axes (X and Y for each stick) be sampled sequentially through a single ADC channel. The switching time and settling time are accounted for in the ADC driver timing.

- **FPGA as co-processor, not replacement**: The FPGA does not run the application logic. It handles time-critical peripheral work (UART buffering, CRC, PWM generation) so the 8051 firmware stays in control of system behavior. This boundary is important to maintain.

- **USB-UART bridge for host connectivity**: A CP2102 or CH340 bridge converts the FPGA's UART output to USB CDC for the host. This keeps the FPGA design simple (standard UART, not USB) while giving the host a standard serial device to talk to.

---

## Firmware Design

The firmware lives in `firmware/` and is written in a mix of 8051 assembly (timing-critical paths, interrupt handlers, scheduler core) and C (higher-level logic, protocol building, diagnostics).

The toolchain is SDCC for C compilation and a custom assembler wrapper. Build scripts are in `tools/`.

### Scheduler System

> `firmware/scheduler/`

The scheduler is cooperative, not preemptive. On the 8051, implementing true preemption is possible but it requires careful stack management and the gains are limited on a single-core, no-MMU architecture. A cooperative model is simpler, more predictable, and easier to reason about under failure conditions.

Each task is defined by a `TaskDescriptor`:

```c
typedef struct {
    uint8_t  task_id;
    uint8_t  priority;         // 0 = highest
    uint16_t period_ms;        // how often to run
    uint16_t deadline_ms;      // soft deadline
    void     (*handler)(void); // function pointer
    uint8_t  flags;            // ACTIVE, SUSPENDED, OVERRUN
} TaskDescriptor;
```

The scheduler maintains a fixed-size task table (currently 16 slots — a deliberate constraint that keeps the table in internal RAM). At each scheduler tick (driven by Timer 0 overflow), it walks the table, decrements period counters, and marks tasks ready. The main loop drains the ready queue in priority order.

```
Scheduler Execution Flow

  Timer 0 Overflow ISR
         │
         ▼
  ┌─────────────┐
  │ Tick all    │
  │ task timers │
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐       Main Loop
  │ Mark tasks  │◄──────────────────────────┐
  │ ready       │                           │
  └──────┬──────┘                           │
         │                                  │
         ▼                                  │
  ┌─────────────────────┐                   │
  │  Ready Queue        │                   │
  │  (sorted by pri)    │                   │
  └──────────┬──────────┘                   │
             │                              │
             ▼                              │
  ┌─────────────────────┐                   │
  │  Dispatch highest   ├───────────────────┘
  │  priority task      │
  └─────────────────────┘
```

If a task exceeds its soft deadline, the watchdog increments an overrun counter for that task. Three consecutive overruns flag the task as degraded and emit a trace event. The task continues to run — this is a monitoring mechanism, not a kill switch. Killing a task unilaterally tends to cause worse problems than a slow task.

Task definitions are in `firmware/scheduler/task_table.c`. The scheduler core is in `firmware/scheduler/sched.asm` — it's assembly because the tick handler runs in ISR context and needs to be fast.

### Interrupt Architecture

> `firmware/isr/`

The 8051 has a two-level interrupt priority system: high and low. DSSX uses this as follows:

| Interrupt Source    | Priority | Purpose                              |
|---------------------|----------|--------------------------------------|
| Timer 0 Overflow    | High     | Scheduler tick (1ms)                 |
| UART RX             | High     | Receive byte into RX ring buffer     |
| UART TX             | Low      | Drain TX ring buffer                 |
| Timer 1 Overflow    | Low      | UART baud rate generator (not used as ISR in most configs) |
| External INT0       | High     | FPGA interrupt line (FIFO threshold) |
| External INT1       | Low      | Haptic pattern sync                  |

The RX interrupt handler is written in assembly (`firmware/isr/uart_rx.asm`). It does exactly one thing: read `SBUF`, write to the ring buffer, advance the write pointer, and return. No protocol parsing in ISR context. Any logic beyond the ring buffer write risks missing the next byte.

Interrupt storms (INT0 firing repeatedly due to FPGA FIFO signaling) are a known failure mode. The simulation suite in `simulation/storm/` was built specifically to characterize this. The mitigation is a hysteresis threshold on the FPGA FIFO interrupt: it asserts when fill level exceeds 75% and deasserts only when it drops below 25%. This prevents rapid toggling.

### Watchdog Infrastructure

> `firmware/watchdog/`

The 8051's on-chip watchdog (where available) is used alongside a software watchdog maintained in firmware. The hardware watchdog resets the chip if the main loop stalls for more than ~100ms. The software watchdog tracks per-task health with finer granularity.

Each task that registers with the watchdog is assigned a watchdog slot:

```c
void wdog_register(uint8_t task_id, uint16_t timeout_ms);
void wdog_checkin(uint8_t task_id);   // call at start of task execution
void wdog_service(void);              // called by scheduler each tick
```

If `wdog_service()` finds a task has not checked in within its timeout, it logs a watchdog event (task ID, timestamp, last known state) to the diagnostics trace buffer and optionally resets that task's state machine. A full system reset is reserved for cases where the watchdog detects that multiple critical tasks are failing simultaneously.

The watchdog infrastructure is one of the few places in the firmware that deliberately writes to an append-only trace buffer even when the rest of the system is potentially unhealthy — the trace data needs to survive into the post-reset diagnostics window.

### Task Dispatch & Runtime Balancing

> `firmware/dispatch/`, `firmware/runtime/`

The task dispatch table maps task IDs to their handlers and contains metadata used by the runtime balancer:

```c
typedef struct {
    uint8_t  task_id;
    uint8_t  recent_runtime_us;  // rolling average, last 8 executions
    uint8_t  budget_us;          // allocated time budget
    uint8_t  overrun_count;
} RuntimeSlot;
```

The runtime balancer runs after each task completes and adjusts soft priorities. If a task consistently runs under budget, it may be shifted to yield more scheduler time to higher-demand tasks. This is not a hard real-time guarantee — it's a best-effort mechanism to prevent one badly-behaved task from starving others.

In practice, the balancer mostly handles the ADC sampling task and the packet builder task, which have variable execution times depending on how much data needs to be processed.

The dispatch and runtime code is in C (`firmware/dispatch/dispatch.c`, `firmware/runtime/balancer.c`) with the critical section protections written as inline assembly macros.

### ADC Pipeline & Joystick Subsystem

> `firmware/drivers/adc/`, `firmware/drivers/joystick/`

The analog joystick pipeline is more involved than it looks.

**Physical signal path:**

```
Joystick potentiometer
       │
       ▼
 Analog MUX (74HC4051)
       │
       ▼
 RC low-pass filter (hardware)
       │
       ▼
 ADC input pin (P1.x or external ADC)
       │
       ▼
 ADC conversion (10-bit)
       │
       ▼
 Software averaging (8-sample rolling)
       │
       ▼
 Noise floor clamping
       │
       ▼
 Deadzone application
       │
       ▼
 Normalization to [-32767, +32767]
       │
       ▼
 Calibration offset correction
       │
       ▼
 Output to packet builder
```

The hardware RC filter is a simple R/C network on the PCB that attenuates high-frequency noise (from PWM switching in the haptic driver, primarily). Without it, the ADC samples show visible 100-200 LSB noise spikes when the haptic motors are active. The filter values are documented in `hardware/schematics/`.

The software side averages 8 consecutive samples (circular buffer, power-of-two size for cheap modulo). The averaging window is long enough to smooth noise but short enough that fast stick movements don't feel laggy. Getting this tradeoff right required benchmarking — see `benchmarks/latency/joystick_latency.md`.

Deadzone handling: the center position of a joystick potentiometer drifts with temperature and wear. A fixed deadzone of ±5% is applied in software, with per-axis calibration offsets stored in the lower 32 bytes of XDATA. Calibration is triggered by a host command and runs a 500ms average of the stick at rest.

The joystick task (`firmware/drivers/joystick/joystick.c`) runs at 4ms periodicity — 250Hz sample rate. This is a deliberate choice; USB HID typically polls at 125Hz or 1000Hz, but the firmware samples faster and lets the middleware downsample as needed.

### Haptic Engine

> `firmware/drivers/haptic/`

Haptic feedback is driven by PWM output to motor driver ICs (DRV2605 or similar). The FPGA PWM engine generates the actual waveform; the firmware sends pattern parameters over the internal bus.

The haptic engine maintains a pattern queue:

```c
typedef struct {
    uint8_t  motor;          // LEFT (0) or RIGHT (1)
    uint8_t  intensity;      // 0–255
    uint16_t duration_ms;
    uint8_t  waveform_id;    // index into waveform table
} HapticCmd;
```

Pattern playback is handled by a state machine in `firmware/drivers/haptic/haptic.c`. The state machine checks the queue each scheduler tick and writes updated intensity values to the FPGA PWM register. Waveform envelopes (attack, sustain, release) are defined in a lookup table — it's not a synthesizer, just a table of pre-computed curves.

Timing precision for haptic patterns depends on the scheduler tick rate. At 1ms ticks, pattern timing resolution is 1ms, which is adequate for most feedback patterns. Finer granularity would require moving haptic timing into the FPGA itself.

The interaction between haptic PWM switching and ADC noise is the main reason for the hardware RC filter mentioned above. This coupling between subsystems is documented in `docs/tradeoffs.md`.

### Diagnostics Tracing

> `firmware/diagnostics/`

The firmware maintains a 64-byte ring buffer in IRAM for trace events. Each event is 4 bytes:

```
┌──────────┬──────────┬──────────────────────┐
│  Task ID │  Event   │  Timestamp (12-bit)  │
│  (4 bit) │  Code    │  (ms since boot,     │
│          │  (8 bit) │   wraps at 4096ms)   │
└──────────┴──────────┴──────────────────────┘
```

This is deliberately minimal. IRAM is 256 bytes total; spending 64 bytes on diagnostics is already a significant allocation. The ring buffer is packed into a contiguous region at the top of IRAM to minimize fragmentation.

Trace events are flushed to the host via a low-priority DSSX diagnostic packet type whenever the UART TX queue has headroom. In normal operation, the trace buffer drains faster than it fills. Under heavy load, events may be dropped — dropped events are counted in a 2-byte overflow counter that is always transmitted.

The host-side trace viewer (`diagnostics/trace_viewer/`) decodes and displays these events in real time. It can replay captured trace streams offline for post-mortem analysis.

---

## DSSX Transport Protocol

> `firmware/protocol/`, `docs/protocol_spec.md`

### Why a Custom Protocol

The short answer: existing protocols don't fit the constraints.

USB HID works fine for the final host-facing interface, but it's too heavy to run in firmware on an 8051 without an external USB controller. Serial framing protocols like SLIP are simple but don't include sequencing, acknowledgment, or CRC. UART raw stream gives no structure at all.

DSSX is a lightweight, framed, sequence-numbered protocol designed to run over a UART link with a small 8051 on one end and a host process on the other. It provides:

- Reliable framing (start/end markers, byte stuffing)
- Sequence numbering for ordered delivery
- CRC-16 for data integrity
- Packet types for different payload kinds (input, haptic, config, diagnostics)
- Selective retransmission for reliable delivery on lossy links
- Fragmentation for payloads that exceed the maximum packet size

It does not provide: encryption, authentication, QoS prioritization, or any network-layer routing. Those are out of scope for a single-link, fixed-topology embedded system.

### Packet Structure

All multi-byte fields are little-endian (matching the 8051's natural byte ordering).

```
DSSX Packet Frame

 Byte  0    1    2    3    4       5..N-3   N-2  N-1
      ┌────┬────┬────┬────┬────┬─────────┬────┬────┐
      │ SF │ LN │ TY │ SQ │ FL │ PAYLOAD │ CL │ CL │
      └────┴────┴────┴────┴────┴─────────┴────┴────┘

SF  = Start Frame (0xAA)
LN  = Payload length (0–255)
TY  = Packet type (see table below)
SQ  = Sequence number (0–255, wraps)
FL  = Flags byte
CL  = CRC-16 CCITT low byte (N-2) and high byte (N-1)
```

**Packet Types:**

| Type Code | Name         | Direction  | Description                              |
|-----------|--------------|------------|------------------------------------------|
| `0x01`    | INPUT_STATE  | FW → Host  | Full controller input snapshot           |
| `0x02`    | INPUT_DELTA  | FW → Host  | Delta from previous state (compact form) |
| `0x03`    | HAPTIC_CMD   | Host → FW  | Haptic pattern command                   |
| `0x04`    | CONFIG_SET   | Host → FW  | Set configuration parameter              |
| `0x05`    | CONFIG_GET   | Host → FW  | Request configuration parameter          |
| `0x06`    | CONFIG_RESP  | FW → Host  | Configuration parameter response         |
| `0x07`    | DIAG_TRACE   | FW → Host  | Firmware trace events                    |
| `0x08`    | DIAG_STATS   | FW → Host  | Runtime statistics snapshot              |
| `0x09`    | ACK          | Both       | Packet acknowledgment                    |
| `0x0A`    | NAK          | Both       | Negative acknowledgment / retransmit req |
| `0x0B`    | FRAG         | Both       | Fragment of a larger payload             |
| `0x0C`    | FRAG_LAST    | Both       | Final fragment                           |
| `0x0D`    | HEARTBEAT    | Both       | Keepalive / round-trip time measurement  |
| `0x0E`    | RESET_REQ    | Host → FW  | Request protocol state reset             |
| `0x0F`    | RESET_ACK    | FW → Host  | Protocol state reset acknowledged        |
| `0x10`    | CALIB_START  | Host → FW  | Begin calibration procedure              |
| `0x11`    | CALIB_DATA   | FW → Host  | Calibration sample data                  |

**Flags byte:**

```
Bit 7: FRAG_MORE   (1 = more fragments follow)
Bit 6: RELIABLE    (1 = ACK required)
Bit 5: COMPRESSED  (reserved, not yet implemented)
Bit 4: PRIORITY    (1 = high priority, skip queue head)
Bits 3-0: reserved, must be zero
```

**INPUT_STATE Payload (28 bytes):**

```
┌────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┐
│ LX_L   │ LX_H   │ LY_L   │ LY_H   │ RX_L   │ RX_H   │ RY_L   │ RY_H   │
├────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│ BTN_0  │ BTN_1  │ BTN_2  │ BTN_3  │ TRIG_L │ TRIG_R │ FLAGS  │ SEQTS_L│
├────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│ SEQTS_H│ BATT   │ TEMP   │ RSRVD  │ RSRVD  │ RSRVD  │ RSRVD  │ RSRVD  │
├────────┼────────┼────────┼────────┤
│ RSRVD  │ RSRVD  │ RSRVD  │ RSRVD  │
└────────┴────────┴────────┴────────┘

LX/LY/RX/RY: 16-bit signed, normalized joystick values
BTN_0–3: button bitmaps
TRIG_L/R: analog trigger values (0–255)
FLAGS: input validity flags
SEQTS: input sequence timestamp (relative to last HEARTBEAT sync)
BATT: battery level (0–100)
TEMP: MCU temperature estimate (degrees C, offset encoded)
```

### Fragmentation & Reassembly

The maximum payload per packet is 255 bytes (constrained by the single-byte length field). Payloads larger than this (rare but possible for config blobs and firmware trace dumps) are fragmented.

Fragment packets use the `FRAG` type with the `FRAG_MORE` flag set on all fragments except the last, which uses `FRAG_LAST`. Each fragment carries the original packet type in bytes 0–1 of its payload, followed by fragment index (1 byte), total fragment count (1 byte), and then the data slice.

The reassembly engine on the host side (`middleware/router/reassembler.c`) holds a partial assembly buffer per originating packet type. If fragments arrive out of order (unusual on a UART link but possible during recovery scenarios), the reassembler handles reordering. If a fragment is missing after a timeout, it requests retransmission of the specific fragment by sequence number.

The firmware-side fragmenter is in `firmware/protocol/frag.c`. It splits the source payload into chunks and enqueues them as individual packets. This keeps the TX queue simple — all entries in the queue are complete, ready-to-send packets.

### CRC & Packet Validation

CRC-16 CCITT (polynomial 0x1021, initial value 0xFFFF) is computed over the packet from byte 1 (length) through the last payload byte — the start frame byte and the CRC bytes themselves are excluded.

On the FPGA, there is a hardware CRC engine (`fpga/crc/`) that can compute CRC-16 at wire speed without burdening the 8051. The firmware uses this engine for transmission by DMA-style: it writes the packet to the FPGA TX FIFO and reads the resulting CRC from a status register once the FPGA signals completion. For receive, the FPGA validates incoming CRC and sets a status bit that the firmware reads — the firmware does not re-validate in software under normal conditions.

On platforms without the FPGA (simulation mode, direct UART debug), the middleware and firmware both include a software CRC implementation.

**Validation pipeline:**

```
Incoming byte stream
       │
       ▼
  Framing detector (look for 0xAA start byte)
       │
       ▼
  Length validation (length field plausible? < max?)
       │
       ▼
  Buffer accumulation (wait for length bytes)
       │
       ▼
  CRC check (hardware via FPGA or software)
       │
  ┌────┴────┐
  │         │
PASS      FAIL
  │         │
  ▼         ▼
Dispatch  NAK + discard
          + increment
          error counter
```

Packets that fail CRC validation generate a NAK with the sequence number of the failed packet. The sender responds with a retransmission. This works fine for occasional errors; persistent CRC failures trigger a protocol reset sequence.

### Retransmission Logic

The retransmission mechanism is simple: a sliding window of size 4 (configurable). The sender maintains a transmit buffer of the last N sent packets. On receiving a NAK, it retransmits the specified packet. On receiving an ACK, it advances the window.

The window size of 4 was chosen to match the FPGA FIFO depth divided by the maximum packet size. Larger windows improve throughput on high-latency links, but the UART link here has a fixed, low latency (~1ms round trip at 115200 baud), so window size matters less than on a TCP-over-WiFi link.

Retransmission timeout is 20ms. If no ACK arrives within 20ms of sending a reliable packet, it is retransmitted. After 3 retransmissions without acknowledgment, the session is considered broken and a recovery sequence begins.

The retransmit engine is in `firmware/protocol/retransmit.c` (firmware side) and `middleware/transport/retransmit.c` (host side).

### Runtime Recovery & Protocol Recovery

> `firmware/protocol/recovery.c`, `middleware/transport/recovery.c`, `simulation/recovery/`

Recovery handles the case where the protocol state on either end has diverged — usually due to a firmware reset, a host process restart, or a link error storm.

**Recovery sequence:**

```
  Host detects link failure (timeout, persistent NAK)
          │
          ▼
  Host sends RESET_REQ (sequence number resets to 0)
          │
          ▼
  Firmware receives RESET_REQ, clears TX/RX buffers,
  resets sequence counters, sends RESET_ACK
          │
          ▼
  Host receives RESET_ACK, resets its own state
          │
          ▼
  Both sides send HEARTBEAT to re-synchronize
  timestamps and confirm link health
          │
          ▼
  Normal operation resumes
```

If the firmware does not respond to RESET_REQ within 500ms, the host escalates by dropping the UART connection, waiting 1 second, and reconnecting. This handles the case where the firmware is in a state where it cannot process protocol packets at all (deep in a fault handler, for example).

The recovery path is tested extensively in `simulation/recovery/`. The fuzzer (`simulation/fuzzer/`) can inject recovery conditions by corrupting state at specific points in the packet stream and verifying that the system recovers correctly.

---

## UART Transport Layer

> `firmware/drivers/uart/`, `middleware/transport/uart_transport.c`

UART is the physical transport for DSSX. At 115200 baud, 8N1, the theoretical throughput is ~11,520 bytes/second. With protocol overhead, effective payload throughput is roughly 9,000 bytes/second.

An INPUT_STATE packet is 32 bytes (4 header + 28 payload + 2 CRC). At 250Hz sample rate, input state packets alone consume ~8,000 bytes/second — leaving limited headroom for diagnostics, haptic commands, and config traffic. This is a real constraint that shapes a number of design decisions:

- INPUT_DELTA packets (type `0x02`) were introduced specifically to reduce bandwidth. If only a few axes have changed, a delta packet carrying only the changed fields is far smaller.
- Diagnostics trace packets are rate-limited and only sent when there is UART headroom.
- Haptic commands are buffered on the firmware side with a small queue — the host does not need to receive acknowledgment before sending the next command.

**UART buffering:**

The firmware uses a 32-byte TX ring buffer and a 64-byte RX ring buffer (both in XDATA). The FPGA-side UART module has a 128-byte synchronous FIFO on both TX and RX paths, providing additional buffering between the MCU and the line.

The asymmetry in buffer sizes (RX larger than TX) reflects the traffic pattern: more data flows from firmware to host than from host to firmware.

**Baud rate and timing:**

With an 11.0592 MHz crystal, the baud rate generator produces exactly 115200 baud with 0% error using Timer 1 in 8-bit auto-reload mode. The UART setup is in `firmware/drivers/uart/uart_init.asm`.

---

## FPGA Acceleration Modules

> `fpga/`

The FPGA fabric runs alongside the 8051. All modules are written in synthesizable Verilog and targeted at a small FPGA (Lattice iCE40 or equivalent). The synthesis scripts and constraints are in `fpga/`.

The FPGA connects to the 8051 via a simple parallel bus, with 8 data lines and 4 address lines mapped into the 8051's XDATA space via chip select decoding. From firmware, accessing FPGA registers looks like accessing external memory.

### UART RX/TX Modules

> `fpga/uart/`

The FPGA handles UART framing at the bit level. The TX module accepts bytes from the FIFO and serializes them with start and stop bits. The RX module deserializes incoming bits, validates stop bits, and writes received bytes to the RX FIFO.

Baud rate is configured by a 16-bit divisor register (written by the 8051 at startup). The module supports 9600 to 921600 baud with a 50 MHz FPGA clock.

**Why run UART in the FPGA rather than using the 8051's on-chip UART?**

The 8051's on-chip UART is used for debug output on a separate physical port. Running the host-facing UART in the FPGA allows independent baud rate selection and, more importantly, lets the FPGA FIFO system decouple the UART timing from the MCU's interrupt response latency.

### FIFO Subsystem

> `fpga/fifo/`

Two FIFOs: one on the TX path (MCU → Host), one on the RX path (Host → MCU).

Both FIFOs are synchronous (single clock domain), 128 bytes deep, with configurable fill-level interrupt thresholds. The TX FIFO asserts an interrupt to the MCU when it drops below 25% full (requesting more data). The RX FIFO asserts an interrupt when it rises above 50% full (requesting the MCU drain it).

The FIFO module is parameterized by depth and data width. Current instantiation: depth=128, width=8. The Verilog source (`fpga/fifo/sync_fifo.v`) is generics-clean and can be re-instantiated at different depths.

### CRC Engine

> `fpga/crc/`

The CRC-16 CCITT engine is a parallel implementation — it computes the full CRC update for one byte in a single clock cycle, not through serial bit shifting. This means CRC computation for a 32-byte packet takes 32 clock cycles, which at 50 MHz is 640ns — effectively free.

The engine has three register-mapped interfaces:
- `CRC_INIT`: write to reset the CRC accumulator to the initial value
- `CRC_DATA`: write a byte to update the accumulator
- `CRC_RESULT_L` / `CRC_RESULT_H`: read the current CRC (two bytes)

For TX, firmware writes each packet byte to `CRC_DATA` as it loads the FIFO, then reads the result and appends it. For RX, firmware writes received bytes and compares the result against the received CRC bytes.

The parallel CRC logic was generated from the standard LFSR polynomial tables and verified against a software reference implementation in the test suite.

### Scheduler Timers

> `fpga/timers/`

The FPGA provides two 16-bit timer/counters accessible from the MCU. One is used as the scheduler tick source (1ms period, generates MCU interrupt via the parallel bus interrupt line). Using the FPGA for this frees up the 8051's Timer 0 for the UART baud rate generator in some configurations.

The second timer is a free-running microsecond counter used for high-resolution timestamp generation in the diagnostics trace events.

### PWM Engine

> `fpga/pwm/`

Two independent PWM channels for the left and right haptic motors. Each channel has:
- 8-bit duty cycle register
- 16-bit period register
- Soft start/stop control

The PWM frequency is set to ~200Hz for the LRA (linear resonant actuator) motors. For ERM (eccentric rotating mass) motors, a different frequency range is used — this is configurable via the period register.

The `PRIORITY` flag in DSSX haptic commands maps to a preemption mechanism in the PWM engine: a high-priority haptic command can interrupt a currently playing pattern, load new parameters, and start immediately. Low-priority commands queue behind the current pattern.

### Hardware Filtering

> `fpga/filter/`

This module implements a simple IIR low-pass filter in fixed-point arithmetic, applied to ADC samples before the firmware sees them. It's a first-order filter (single-pole) with a configurable coefficient.

The filter exists because even after the hardware RC network on the PCB, there is still residual high-frequency content in the joystick samples. The software averaging in the firmware handles some of this, but a hardware filter stage with properly chosen coefficients does the job more cleanly.

The filter coefficient is written by the MCU at boot time (computed based on the sample rate and desired cutoff frequency). The FPGA module stores the coefficient in a register and applies it to each sample as it arrives from the ADC.

---

## Middleware Architecture

> `middleware/`

The middleware runs on the host machine (Linux or Windows) as a user-space process. It owns the UART connection to the device, handles DSSX protocol framing/parsing, and presents clean interfaces to the SDK layer above it.

The middleware is written in C, single-threaded with an event loop (similar in philosophy to how libuv works — not using libuv, but similar model). This avoids the complexity of multi-threaded shared state while keeping the system responsive.

### Runtime Management

> `middleware/runtime/`

The middleware runtime manages the lifecycle of connections, protocol sessions, and stream handlers. A session object tracks:

- Current connection state (disconnected, connecting, syncing, active, recovering)
- Protocol state (sequence numbers, retransmit window)
- Per-packet-type statistics
- Last heartbeat timestamp

Sessions are created when the UART connection is established and torn down on disconnect. The runtime supports reconnection with session state preservation — if the firmware reconnects within a configurable window, the protocol session is resumed rather than reset.

### Packet Routing

> `middleware/router/`

Incoming DSSX packets are dispatched to registered handlers based on packet type. The routing table is a function pointer array indexed by packet type. Handlers can be registered dynamically (SDK plugins or test harnesses register handlers at startup).

Outgoing packets are enqueued to the transport layer's TX queue. The router enforces per-type rate limits on the TX side: for example, haptic commands are limited to 100/sec to prevent the UART link from being saturated by rapid haptic sequences.

### Stream Scheduling

> `middleware/stream/`

Input state packets arrive at 250Hz from the firmware. Not all consumers need data at 250Hz. The stream scheduler maintains a list of output streams with configurable target rates, and downsamples the input appropriately.

The HID output stream runs at 125Hz (USB HID polling rate for standard mode) or 1000Hz (high-performance mode, requires USB HID descriptor claiming 1ms poll). The SDK stream runs at whatever rate the SDK consumer requests, up to the input rate.

Backpressure is handled by dropping the oldest sample when a consumer's output buffer is full. The dropped sample count is tracked and exposed through the diagnostics interface.

### HID Translation Layer

> `middleware/hid/`

The HID translation layer converts DSSX INPUT_STATE packets to OS-appropriate HID reports. This is how the platform appears as a gamepad to the operating system without requiring a custom kernel driver.

**HID translation pipeline:**

```
DSSX INPUT_STATE packet
        │
        ▼
  Payload decoder
  (parse into internal InputState struct)
        │
        ▼
  Axis scaling
  (normalize -32767..+32767 to HID axis range)
        │
        ▼
  Button mapping
  (DSSX button bits → HID usage page / usage ID)
        │
        ▼
  HID report packer
  (pack into HID input report descriptor format)
        │
        ▼
  Virtual HID device
  (Linux: /dev/uhid or uinput; Windows: ViGEm or HidHide)
```

The HID descriptor is generated at session initialization based on the device capabilities (number of axes, buttons, trigger types). The descriptor generation code is in `middleware/hid/descriptor.c`.

Button mapping is configurable via a mapping table loaded from a config file (`~/.config/dssx/mapping.json` by default). This allows remapping without recompiling.

### Diagnostics Dashboard

> `middleware/diagnostics/`

The diagnostics dashboard aggregates data from all middleware subsystems and exposes it through a local HTTP server (port 7070 by default). The dashboard serves a simple JSON status API and a human-readable HTML summary page.

Data available through the dashboard:
- Connection state and session statistics
- Per-packet-type counts, error rates, and rates
- Firmware trace event stream (live, decoded)
- Joystick axis values (current, min/max seen)
- Scheduler statistics from firmware
- Retransmit counts and recovery events
- Stream scheduler output rates

This is primarily useful during development and debugging. In production use, the dashboard can be disabled in the config.

### Runtime Synchronization

> `middleware/sync/`

The middleware and firmware maintain synchronized timestamps for correlating events. The HEARTBEAT packet carries a host-side timestamp; the firmware reflects it back with a firmware-side timestamp. The round-trip measurement allows the host to estimate clock offset and drift between the two systems.

This synchronization is important for the diagnostics trace system: firmware events carry 12-bit millisecond timestamps (relative to last sync), and the host maps these onto its own absolute timestamp base.

Clock drift between the host and the 8051 crystal is real — the 11.0592 MHz crystal has a typical tolerance of ±20 ppm. Over a 60-second session, this is approximately 1.2ms of drift. The sync protocol corrects for this by re-synchronizing every 10 seconds. The sync implementation is in `middleware/sync/clock_sync.c`.

### Transport Layer Abstraction

> `middleware/transport/`

The transport layer abstracts the physical UART connection behind an interface that the rest of the middleware does not know is physical. This is important for testing: the simulation suite replaces the transport layer with a simulated transport that injects errors, delays, and corruption.

```c
typedef struct {
    int  (*open)(const char *path, uint32_t baud);
    void (*close)(void);
    int  (*write)(const uint8_t *buf, size_t len);
    int  (*read)(uint8_t *buf, size_t maxlen);
    int  (*set_error_injection)(const ErrorInjectionParams *p);
} TransportOps;
```

The real UART implementation uses platform POSIX or Win32 serial APIs. The simulated implementation is in `middleware/transport/sim_transport.c` and is used by the simulation suite and by SDK-level unit tests.

---

## Diagnostics Infrastructure

> `diagnostics/`

The standalone diagnostics tools in `diagnostics/` are separate from the middleware's built-in dashboard. They are desktop applications (Python + terminal UI) that connect to the middleware's diagnostics API.

**trace_viewer**: Connects to the middleware HTTP endpoint and displays firmware trace events in real time. Events are color-coded by task and severity. Supports filtering by task ID, event type, and time range. Can export to JSON for offline analysis.

**packet_inspector**: Captures the raw DSSX packet stream (from the middleware transport layer's capture hook) and decodes it for display. Shows per-packet CRC status, sequence numbers, timing gaps, and payload contents. Invaluable for diagnosing framing issues and retransmit storms.

**runtime_profiler**: Samples the firmware's scheduler statistics (transmitted in DIAG_STATS packets) and plots per-task execution time and overrun counts over time. Identifies tasks that are exceeding their budgets.

All three tools use the same Python client library (`sdk/python/`) for transport and decoding.

---

## Simulation Systems

> `simulation/`

The simulation suite exists for one reason: real failure modes need to be reproducible without waiting for them to happen naturally.

Most of the interesting failure modes in this system are transient — a brief noise burst corrupts one packet, the recovery runs, and everything is fine. Without the ability to reproduce this on demand, verifying that the recovery works correctly is guesswork.

### Protocol Fuzzer

> `simulation/fuzzer/`

The fuzzer uses a mutation-based approach: it takes valid captured packet streams and applies random mutations (bit flips, byte insertions, byte deletions, sequence number corruption, length field corruption). Mutated streams are fed through the simulated transport to the middleware and the responses are evaluated.

The fuzzer runs in a loop with a configurable mutation budget and records any cases where the middleware crashes, hangs, or produces incorrect output. It has found several off-by-one errors in the reassembly engine and one case where a corrupted length field caused an out-of-bounds buffer read (fixed; see `docs/adr/008-fuzz-findings.md`).

### Interrupt Storm Simulation

> `simulation/storm/`

On real hardware, an interrupt storm happens when the FPGA FIFO threshold interrupt fires more rapidly than the firmware can process it. In simulation, this is reproduced by running the firmware in a software emulator (based on an 8051 emulator core — `tools/emu8051/`) and injecting interrupt signals at configurable frequencies.

The tests verify that:
- The firmware's interrupt hysteresis mechanism activates correctly
- The scheduler remains responsive during storm conditions
- The watchdog correctly identifies tasks that are being starved by interrupt handling
- The system recovers gracefully when the storm ends

### Runtime Overload Tests

> `simulation/overload/`

Runtime overload tests inject artificially slow task execution (by adding delay loops into task handlers during simulation runs) to reproduce scheduler overrun conditions. The tests verify that:

- The runtime balancer responds correctly to persistent overruns
- Watchdog events are generated for overrunning tasks
- The protocol stack continues operating under reduced scheduler bandwidth
- Input sampling continues (possibly at reduced rate) during overload

### Packet Corruption Scenarios

> `simulation/corruption/`

Packet corruption tests go beyond the fuzzer by testing specific known-bad scenarios:

- Missing start frame byte (framing resync required)
- Correct CRC on corrupted payload (tests upper-layer validation)
- Truncated packet (connection timeout / partial reassembly)
- Duplicate sequence numbers (deduplication path)
- Out-of-order fragments (reassembly reordering)
- Length field overflow (buffer safety tests)

Each scenario is a named test case with an expected outcome. The test framework compares actual middleware behavior against expected behavior and reports deviations.

### Recovery Simulation

> `simulation/recovery/`

Recovery simulation tests exercise the full recovery sequence under controlled conditions. Test scenarios include:

- Clean restart (firmware reset, clean protocol state reset)
- Dirty restart (firmware reset mid-packet, host detects via timeout)
- Host process restart (firmware running, host reconnects)
- Bidirectional corruption followed by recovery
- Recovery during fragmentation (fragment partially delivered, firmware resets)

The recovery simulation has a configurable fault injection point — it can inject the failure at any point in the packet stream and verify that recovery completes within the specified time bound.

---

## SDK Ecosystem

> `sdk/`

The SDK provides language-appropriate interfaces for building applications on top of the DSSX platform. All SDK variants communicate with the middleware over a local IPC channel (Unix domain socket or named pipe). The middleware exposes a simple message-based API over this channel.

### C SDK

> `sdk/c/`

The C SDK is a thin wrapper around the IPC channel. It provides:

- Synchronous and callback-based input event subscription
- Haptic command sending
- Configuration get/set
- Session management

It uses no dynamic memory allocation (for embedded host use cases). All buffers are caller-provided. The header is `sdk/c/dssx.h`.

```c
// Example: polling input state
DSSXSession *session = dssx_open("/run/dssx/sock");
DSSXInputState state;
while (dssx_read_input(session, &state, DSSX_TIMEOUT_BLOCK) == DSSX_OK) {
    printf("LX: %d LY: %d\n", state.lx, state.ly);
}
dssx_close(session);
```

### C++ SDK

> `sdk/cpp/`

The C++ SDK wraps the C SDK with RAII handles and typed packet interfaces. It uses modern C++ (C++17). Key additions over the C SDK:

- `DSSXSession` as a move-only RAII class
- Typed packet structs with accessor methods
- `InputEventStream` — a range-based interface for consuming input events
- `HapticPattern` builder class for constructing haptic commands
- `std::optional` return types instead of error-code/pointer pairs

No exceptions are used in the core SDK paths (exception overhead matters in latency-sensitive code paths on some platforms). Errors surface as `std::expected<T, DSSXError>` (or `std::optional` where the error is unambiguous).

### Python SDK

> `sdk/python/`

The Python SDK is asyncio-based. It exposes an async generator for input events and coroutines for haptic and config operations. It's designed for tooling, testing, and the diagnostics applications — not for latency-sensitive production use.

```python
import asyncio
from dssx import Session

async def main():
    async with Session("/run/dssx/sock") as session:
        async for state in session.input_events():
            print(f"LX={state.lx} LY={state.ly}")

asyncio.run(main())
```

The Python SDK is used by the diagnostics tools and the simulation suite driver scripts.

### Rust SDK

> `sdk/rust/`

The Rust SDK is async (Tokio-based) with strong typing. It provides a typed packet enum and uses Rust's type system to prevent common misuses (e.g., sending a config_set to a read-only field at compile time, via marker types).

The Rust SDK has the most comprehensive error handling of the four — it uses `thiserror`-derived error types and surfaces all protocol error conditions through typed error variants rather than opaque codes. This makes it the preferred SDK for production host-side code where correctness guarantees matter.

The Rust crate is at `sdk/rust/dssx/`. It is also published separately for projects that want to use just the protocol types without the full SDK.

---

## Benchmarking

> `benchmarks/`

Benchmarks are organized into four categories:

### Latency Benchmarks

> `benchmarks/latency/`

Measure end-to-end latency from physical input change (simulated via test jig) to HID event visible on the host.

| Measurement Point                         | Target  | Measured (115200 baud) |
|-------------------------------------------|---------|------------------------|
| ADC sample → packet builder               | < 2ms   | ~0.8ms                 |
| Packet builder → UART TX start            | < 1ms   | ~0.4ms                 |
| UART TX start → host UART RX              | < 1ms   | ~0.7ms (depends on baud) |
| UART RX → middleware decode               | < 0.5ms | ~0.2ms                 |
| Middleware decode → HID event             | < 1ms   | ~0.5ms                 |
| **Total (typical)**                       | < 5.5ms | **~2.6ms**             |

Numbers are from `benchmarks/latency/e2e_latency.py` on a mid-spec Linux host. Windows adds ~1ms due to HID driver overhead.

### Throughput Benchmarks

> `benchmarks/throughput/`

Measure sustainable packet throughput at different packet sizes and types.

| Packet Type   | Rate    | Utilization (115200 baud) |
|---------------|---------|---------------------------|
| INPUT_STATE   | 250/sec | ~69%                      |
| INPUT_DELTA   | 250/sec | ~20–40% (varies by motion) |
| DIAG_TRACE    | burst   | up to 15%                 |
| Haptic CMD    | 100/sec | ~5%                       |
| Heartbeat     | 10/sec  | ~1%                       |

The headroom at 250Hz INPUT_STATE with DIAG_TRACE enabled is tight (~10%). Running at a higher baud rate (230400 or 460800) provides more comfortable headroom; see `docs/adr/005-baud-rate-selection.md` for the tradeoff discussion.

### Scheduler Benchmarks

> `benchmarks/scheduler/`

Measure scheduler overhead and per-task dispatch latency, run in the 8051 emulator with cycle counting enabled.

| Metric                              | Value     |
|-------------------------------------|-----------|
| Scheduler tick ISR duration         | ~12 cycles |
| Task table scan (16 slots)          | ~48 cycles |
| Ready queue sort (worst case, 4 ready) | ~32 cycles |
| Total scheduler overhead per ms     | < 2% of CPU time |

### Recovery Time Benchmarks

> `benchmarks/recovery_time/`

Measure time from fault injection to recovery completion across different fault types.

| Fault Type                       | Recovery Target | Measured   |
|----------------------------------|-----------------|------------|
| Single packet corruption         | < 40ms          | ~22ms      |
| Sequence number divergence       | < 100ms         | ~65ms      |
| Firmware reset (clean)           | < 200ms         | ~140ms     |
| Firmware reset (mid-fragment)    | < 300ms         | ~210ms     |
| Full session loss and reconnect  | < 1000ms        | ~680ms     |

---

## Design Tradeoffs

A more detailed discussion is in `docs/tradeoffs.md`. Key tradeoffs summarized here:

**Cooperative vs preemptive scheduling**: Cooperative is simpler and more debuggable on the 8051. The cost is that a misbehaving task can delay others. This is mitigated by the watchdog and the design rule that tasks should be short. The rare case of a legitimately long operation (e.g., flash write) is handled by breaking it into multiple scheduled steps.

**FPGA as co-processor vs integrated MCU**: Using an FPGA adds board complexity and cost. The benefit is that it provides a clean boundary for offloading timing-critical work without coupling it to firmware complexity. An alternative would be a more capable MCU (STM32, RP2040), but that would change the character of the platform.

**Single-byte packet length field**: Limits payload to 255 bytes. Sufficient for all current packet types. A two-byte length field would allow larger payloads but would add complexity to every parser. Fragmentation handles the few cases where larger payloads are needed.

**Software CRC on the non-FPGA path**: Software CRC-16 on the 8051 takes ~200 cycles for a 32-byte packet. At 12 MHz, that's ~17 microseconds — acceptable, but it adds up across multiple packets. This is why the FPGA CRC engine was added. The software path remains for fallback and testing.

**Rate-limiting diagnostics traffic**: Diagnostics packets are intentionally deprioritized and rate-limited to prevent them from saturating the link. The tradeoff is that under high-activity conditions, trace events may be dropped. For most debugging purposes, this is acceptable — the diagnostics system is a tool for understanding behavior, not a safety-critical channel.

**HID via userspace (uinput/uhid/ViGEm)**: Avoids the need for kernel drivers, which simplifies deployment. The cost is higher latency compared to a kernel driver, and occasional issues with applications that expect specific USB HID device identifiers. The `middleware/hid/` directory contains workaround notes for known incompatible applications.

---

## Engineering Notes

Notes that don't fit cleanly elsewhere:

**On the 8051 memory model**: The 8051 has four distinct memory spaces (CODE, IRAM, XDATA, SFR). IRAM is 256 bytes of fast on-chip RAM; XDATA is external data memory (16-bit address space, typically 64K). Variables declared without qualifiers go to IRAM. The firmware's memory layout is carefully documented in `firmware/memory_map.md`. Running out of IRAM in an 8051 project is extremely easy to do by accident and produces confusing runtime bugs.

**On debugging the 8051 without a JTAG**: Most low-cost 8051 variants have no JTAG interface. The primary debug mechanism is the diagnostics trace system and the second UART port (used purely for printf-style debug output at 9600 baud on a separate physical connector). The emulator (`tools/emu8051/`) is useful for logic verification but does not model hardware timing precisely.

**On the FPGA build**: The FPGA bitstream build uses Yosys + nextpnr for open-source synthesis. The build is reproducible (bitstream matches bit-for-bit with the same Yosys/nextpnr versions). Build instructions are in `fpga/README.md`.

**On the Python SDK performance**: The Python SDK is not suitable for latency-sensitive paths. At 250Hz input rate, Python's asyncio event loop introduces jitter that is visible in the timing data. For any application where input latency matters, use the C or Rust SDK.

**On testing**: The test suite is in `tests/` (not shown in the top-level layout above — it's there). Unit tests use `cmocka` (for C) and Cargo's built-in test framework (for Rust). Integration tests use the Python SDK and the simulated transport. The CI pipeline runs unit tests, integration tests, and a short fuzzer run on every commit.

---
