# Switch NDS Emulator (Switch 1 & Switch 2)

## Overview

This project is a Nintendo DS emulator running on Nintendo Switch (all models including Switch Lite and OLED) as well as Switch 2.

It is based on the [switch-gba](https://github.com/itsbjoern/switch-gba) project and replaces mGBA with **DeSmuME** for Nintendo DS emulation.

This is an experimental work in progress.

---

## Project Origin

This project takes advantage of a behavior in the Nintendo Switch built-in browser, which is used during certain network authentication flows (for example DNS-based captive portals such as Switchbru).

Reference: https://www.switchbru.com/dns/

### Technical Concept

The Switch browser handles the **B button** differently when an iframe is present:

- The B button first navigates inside the iframe history
- Only then does it affect the main page navigation

This behavior is used as part of the workaround implemented in this project.

The system also uses `postMessage` to maintain a consistent iframe navigation state.

---

## Features

### Implemented
- Nintendo DS game support (.nds files)
- ROM loading from local storage

### In Progress
- Audio emulation
- Touchscreen input support
- X and Y button mapping
- Microphone emulation via a virtual button

### Planned
- WiFi support through a DeSmuME fork with network capabilities

---

## Installation and Usage

### Windows 10 / 11

1. Download the latest release
2. Extract the `.zip` archive
3. Run `switch-nds.exe`

Place your `.nds` ROM files inside the `roms/` folder (empty by default).

---

### Linux

#### Requirements
- Python 3.10 recommended (Python 3.14 is not supported)

#### Setup

```bash
git clone https://github.com/Gabriel-Chevallier/switch-nds.git
cd switch-nds

pip install -r requirements.txt

chmod u+x run.sh
./run.sh