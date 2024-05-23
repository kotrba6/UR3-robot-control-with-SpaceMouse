# Control of UR Robot Using SpaceMouse
[Czech](README.cz.md)/English
## Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Introduction
This project consists of a modular program designed for initializing and controlling a USB device and a Universal Robot (UR) robotic arm. The program reads data from the USB device and processes it to control the movements of the robotic arm.

## Installation
### Requirements
- Recommended to run on Linux for easy installation of the `ur_rtde` library.
- Python 3.x
- Required Python libraries:
  - `usb`
  - `ur_rtde`

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/kotrba6/UR3-robot-control-with-SpaceMouse.git
    cd UR3-robot-control-with-SpaceMouse
    ```
2. Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

## Usage
### Running the Program
1. Set the parameters in the `config.py` file:
   - Enter the correct Vendor ID and Product ID of the USB device.
   - Enter the correct IP address of the UR robotic arm.
   - Set the maximum speed for translation and rotation.
   - Set the default position of the UR robotic arm.

2. Run the `UR_control.py` script:
    ```bash
    python UR_control.py
    ```

After running the script, it should be possible to control the robotic arm using the SpaceMouse.

### Description of Scripts
- **USB_initialization.py**: Initializes the USB device using Vendor ID and Product ID, sets up device configuration, and prepares the endpoint for data reading.
- **UR_initialization.py**: Establishes a connection with the UR robotic arm and moves the arm to the default position.
- **UR_control.py**: Reads data from the USB device, processes it, and controls the movements of the UR robotic arm accordingly.
- **functions.py**: Contains helper functions for data conversion and processing.
- **config.py**: Defines configuration parameters for the USB device and the UR robotic arm.

## Features
- Initialization and data reading from the USB device.
- Initialization and control of the UR robotic arm.
- Data processing functions for conversion and filtering.
- Configuration file for easy parameter adjustments.

## Configuration
The `config.py` file contains the following configurable parameters:
- **USB_initialization**:
  - `VENDOR_ID`: Vendor ID of the USB device.
  - `PRODUCT_ID`: Product ID of the USB device.
- **UR_initialization**:
  - `UR_IP_ADDRESS`: IP address of the UR robotic arm.
  - `DEFAULT_POSITION`: Default position of the UR robotic arm.
- **UR_control**:
  - `TRASLATION_COEF`: Coefficient for calculating translation speed vectors.
  - `ROTATION_COEF`: Coefficient for calculating rotation speed vectors.
  - `TRANSLATION_MAX_SPEED`: Maximum speed for translation [m/s].
  - `ROTATION_MAX_SPEED`: Maximum speed for rotation [rad/s].
  - `DEAD_ZONE_SIZE`: Size of the dead zone.
  - `MEMORY_LENGTH`: Length of the moving average memory.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.
