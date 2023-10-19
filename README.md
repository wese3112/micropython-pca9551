# PCA9551 Python Library

Welcome to the PCA9551 Python library repository! This library is designed to facilitate communication with the PCA9551 I2C LED controller from your MicroPython projects. This README will guide you through the key features and usage of this library, making it accessible to developers of all skill levels.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
  - [Initializing PCA9551](#initializing-pca9551)
  - [Reading Inputs](#reading-inputs)
  - [Controlling LEDs](#controlling-leds)
  - [PWM Control](#pwm-control)
- [Contributing](#contributing)

## Introduction

The PCA9551 is an I2C LED controller that allows you to control LED outputs and implement various lighting effects. This library simplifies the interaction with the PCA9551 by providing a Python interface to control the LEDs and their brightness.

## Installation

You can install this library in your MicroPython environment by following these steps:

1. Download the `pca9551.py` file from this repository.
2. Place the `pca9551.py` file in your MicroPython project directory.

## Usage

### Initializing PCA9551

To get started with the PCA9551 library, you need to initialize an instance of the `PCA9551` class. The class constructor takes two callback functions for I2C operations:

```python
from pca9551 import PCA9551

def write_callback(i2c_address, register_address, data):
    # Implement I2C write operation here
    pass

def read_callback(i2c_address, register_address, num_read):
    # Implement I2C read operation here
    pass

# Initialize PCA9551 instance
pca = PCA9551(write_callback, read_callback)
```

### Reading Inputs
You can read the input state of the PCA9551 using the `read_inputs` method:

```
input_state = pca.read_inputs()
```

### Controlling LEDs
The PCA9551 library provides methods for controlling LED states. You can turn LEDs on, off, or set them to PWM modes. For example:

```
# Turn on specific LEDs
pca.leds_on([0, 1, 2])

# Turn off specific LEDs
pca.leds_off([1, 3])

# Set specific LEDs to PWM0 mode
pca.leds_pwm0([2, 4])
```

### PWM Control
You can also control the duty cycle of PWM0 and PWM1 outputs:

```
# Get the current duty cycle of PWM0
duty_cycle = pca.pwm0_duty_cycle

# Set the duty cycle of PWM0 (0.0 to 1.0)
pca.pwm0_duty_cycle = 0.5

# Get the current duty cycle of PWM1
duty_cycle = pca.pwm1_duty_cycle

# Set the duty cycle of PWM1 (0.0 to 1.0)
pca.pwm1_duty_cycle = 0.3
```

## Contributing
We welcome contributions to this library. If you have suggestions, bug reports, or want to add new features, please create an issue or submit a pull request.
