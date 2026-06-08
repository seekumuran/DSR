# Interrupt Pipeline

```txt
Timer Interrupt
      ↓
Scheduler Dispatch
      ↓
Input Scan Task
      ↓
Packet Build Task
      ↓
UART Transmission Task
      ↓
Interrupt Exit
