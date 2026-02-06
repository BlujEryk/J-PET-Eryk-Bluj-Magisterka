# NLK Valves Control System

Tu bedzie ladne readme z opisami po angielsku
to ponizej jest tu jako moj template

This project is a **graphical interface and server for controlling NLK and SVV valves** using a Raspberry Pi 4b.  
It integrates GPIO hardware control, live signal plotting, and different operation modes to automate or manually control valves depending on proton beam signals (`WK` and `WWK`).

---

## Features

- **Graphical User Interface (Tkinter)**:
  - Real-time valve state visualization
  - Buttons for manual valve control
  - Signal indicators for `WK`, `WWK`, and conditioning mode
  - Live plotting of signals

- **Valves Control**:
  - Support for **NLK** and **SVV** valves
  - Control of three pipelines: **n2EDM**, **Tau spect**, and **Top**

- **Modes of Operation**:
  1. **Manual**             – user directly opens/closes valves
  2. **n2EDM priority**     – NLK valves switch with configurable delay
  3. **Tau spect priority** – NLK valves switch with configurable delay
  4. **Mixed**              – cycle-based alternating priority between n2EDM and Tau spect

- **Signal Handling**:
  - Reads digital input from Raspberry Pi pins (`WK`, `WWK`, `Conditioning`)
  - Detects rising/falling edges of signals
  - Stores last 100 samples in a live buffer
  - Refresh rate: 20 Hz (every 0.05 s)

- **Server Functionality**:
  - TCP socket server on port **9999**
  - Provides textual and binary status of valves and modes
  - Supports commands: `get_status` and `get_binary_status`

  - `get_status` – returns human-readable status of valves, conditioning, and mode.  
  - `get_binary_status` – returns status in **binary format** (`1 = open/ON`, `0 = closed/OFF`).  

### Binary Output Order

When calling `get_binary_status`, the response is a sequence of numbers, each on a new line, followed by the current mode and parameters (if applicable).

The order is:

1. **NLK n2EDM valve**  
2. **NLK Tau spect valve**  
3. **NLK Top valve**  
4. **SVV n2EDM valve**  
5. **SVV Tau spect valve**  
6. **SVV Top valve**  
7. **Conditioning signal**  
8. **Current mode name** (`Manual` -> 1, `n2EDM priority` -> 2, `Tau spect priority` -> 3, `Mixed` ->4)  
9. **Mode parameters** (only if not Manual):  
   - For `Mixed`: `n2EDM_delay_time`, `Tau spect_delay_time`, `n2EDM_cycle_number`, `Tau spect_cycle_number`  
   - For `n2EDM priority`: `delay_time`  
   - For `Tau spect priority`: `delay_time`

- Sample server response after calling `get_status`
- ![Mode selection](/Images/for_readme/get_status.jpg)
- Sample server response after calling `get_binary_status`
- ![Mode selection](/Images/for_readme/get_binary_status.jpg)

## Graphical Interface

The GUI is divided into sections:
1. **Top Left** – mode selection & configuration  
2. **Top Right** – signal indicators (`WK`, `WWK`, `Conditioning`)  
3. **Bottom Left** – live plot of signals  
4. **Bottom Right** – valves status grid  

- Mode selection
- ![Mode selection](/Images/for_readme/manual.jpg)
- In addition, if user tries to change the mode when WK/WWk signal is detected this warning will occur
- ![In addition, if user tries to change the mode when WK/WWk signal is detected this warning will occur](/Images/for_readme/warning.jpg)
- Signals and Conditioning status
- ![Signals and Conditioning status](/Images/for_readme/signals.jpg)
- Signals plotting
- ![Signals plotting](/Images/for_readme/graph.jpg)
- Current Valves status with additional information such as time reamining until valves status changes and number of cycles remaining until priority changes
- ![Current Valves status with additional information such as time reamining until valves status changes and number of cycles remaining until priority changes](/Images/for_readme/properties.jpg)

---

## Hardware Setup

This system runs on a **Raspberry Pi (GPIO BCM mode)**.  
The valves and signals are connected to specific pins:

### Input Pins
- `Conditioning`: GPIO 5  
- `WK`: GPIO 20  
- `WWK`: GPIO 21  
- `NLK n2EDM`: GPIO 16  
- `NLK Tau spect`: GPIO 13  
- `NLK Top`: GPIO 12  
- `SVV n2EDM`: GPIO 26  
- `SVV Tau spect`: GPIO 19  
- `SVV Top`: GPIO 6  

### Output Pins
- `NLK n2EDM`: GPIO 23  
- `NLK Tau spect`: GPIO 24  
- `NLK Top`: GPIO 25  
- `SVV n2EDM`: GPIO 4  
- `SVV Tau spect`: GPIO 8  
- `SVV Top`: GPIO 7  
- Additional control: GPIO 2, GPIO 3  

---

### Hardware & Schematics

- PCB plate circuit diagram
- ![PCB plate circuit diagram](/Images/for_readme/circuit_diagram.jpg)
- Photo of PCB plate
- ![Photo of PCB plate](/Images/for_readme/hardware.jpg)
- Pins on the front of PCB plate
- ![Pins on the front of PCB plate](/Images/for_readme/pins.jpg) 

---

## Getting Started

### Requirements
- Raspberry Pi 4b with GPIO headers
- Python 3.11
- Installed libraries:
    - RPi.GPIO
    - tkinter
    - matplotlib
    - numpy
    - time
    - threading
    - copy
    - socket
    - string
    - collections



### Running
1. Connect valves and signals to Raspberry Pi according to the pinout above.
2. Start the program:
   ```bash
   python3 interface.py
   ```
3. GUI window will open with live updates.

---

## Modes Explanation

- **Manual Mode**         – full manual control with GUI buttons.  
- **n2EDM priority**      – n2EDM line prioritized, after a configurable delay valves switch.  
- **Tau spect priority**  – Tau spect line prioritized, behaves same as above.  
- **Mixed**               – alternating priority between n2EDM and Tau spect in configurable cycles/delays.  

- Manual mode gui
- ![Manual mode gui](/Images/for_readme/manual.jpg)
- n2EDM priority mode gui
- ![n2EDM priority mode gui](/Images/for_readme/n2EDM.jpg)
- Tau spect priority mode gui
- ![Tau spect priority mode gui](/Images/for_readme/Tauspect.jpg)
- Mixed mode gui
- ![Mixed mode gui](/Images/for_readme/mixed.jpg)

---

## Contact details
  - If you have any qyestions or would like me to make any changes, here are my contact details:
  - erykbluj@gmail.com
  - +48 668 727 367