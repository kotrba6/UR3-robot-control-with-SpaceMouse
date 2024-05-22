# UR3-robot-control-with-SpaceMouse
## Overview
This project consists of a modular program designed for controlling a Universal Robots robotic arm. The code is structured into several modules, each serving a specific purpose in the overall system. Below is an overview of the functions provided by each module.

### Recommendation: 
To ensure smooth installation and operation, we recommend running this code on a Linux operating system. Installing the ur_rtde library is significantly easier on Linux systems.

## Modules
### 1. USB_initialization.py
This module is responsible for initializing USB devices using their Vendor ID and Product ID.

#### Dependencies:
usb.core

#### Configuration:
Vendor ID and Product ID are defined in the config.py file.

#### Key Functions:
Finding and initializing the USB device.
Detaching the kernel driver if it is active.
Setting the configuration and endpoint for data reading.

### 2. config.py
This module contains various configuration parameters used throughout the project.

#### USB Initialization:
VENDOR_ID: Vendor ID of the USB device.
PRODUCT_ID: Product ID of the USB device.

#### UR Initialization:
UR_IP_ADDRESS: IP address of the Universal Robots robotic arm.
DEFAULT_POSITION: Default position for the robotic arm.

#### UR Control:
Coefficients and maximum speeds for translation and rotation.
Dead zone size and filter memory length.
EMA_COEF: Coefficient for Exponential Moving Average.
FIR_FILTER_COEFS: Coefficients for the FIR filter.

### 3. functions.py
This module contains various helper functions for data processing and control.

#### Key Functions:
bytes_to_int: Convert bytes to an integer.
apply_fir_filter: Apply FIR filter to a vector.
apply_ema_filter: Apply EMA filter to a value.
dead_zone_filter: Apply dead zone filter to a vector.
moving_average: Calculate the moving average of a vector.
convert_to_speed_vector: Convert vectors to speed vectors for translation and rotation.
collect_data_tool and collect_data_joint: Collect data on tool position and joints and write them to CSV files.

### 4. UR_control.py
This module provides the main loop for reading data from the USB device and controlling the robotic arm as needed.

#### Dependencies:
usb.core, functions.py

#### Key Functions:
Initializing the USB device.
Processing data from the USB device.
Applying various filters to the data.
Sending control commands to the robotic arm based on processed data.
Collecting data on tool and joint positions.

### 5. UR_initialization.py
This module initializes the connection to the Universal Robots robotic arm and sets it to the default position.

#### Dependencies: 
rtde_control, rtde_receive

#### Key Functions:
Initializing the control and receive interface for the robotic arm.
Checking the connection status.
Moving the robot to the default position using inverse kinematics.

## Installation
Install dependencies:
Ensure you have Python 3.x and pip installed. Then install the dependencies using the following command:

pip install -r requirements.txt

## Setup: 
Ensure all configuration parameters in the config.py file are correctly set for your environment.

## Usage
Robot Control: Run UR_control.py to start the main loop and control the robotic arm.

## Dependencies
Python 3.x
Libraries: pyusb, ur_rtde

## Notes
Ensure the robot's IP address and USB device IDs are correctly set in the config.py file.
The code includes exception handling for various USB and communication errors.
The loop in UR_control.py is designed to run continuously, processing data and controlling the robot until interrupted.
