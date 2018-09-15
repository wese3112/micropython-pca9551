try:
    from micropython import const
except ImportError:
    def const(var):
        return var
from math import ceil

PCA9551_ADDRESS = const(0x67)

# PCA9551 register addresses
INPUT = const(0x00)
PSC0 = const(0x01)
PWM0 = const(0x02)
PSC1 = const(0x03)
PWM1 = const(0x04)
LS0 = const(0x05)
LS1 = const(0x06)

# LED output states
LED_ON =   const(0b00)  # output is set LOW (LED on)
LED_OFF =  const(0b01)  # output is set high-impedance (LED off; default)
LED_PWM0 = const(0b10)  # output blinks at PWM0 rate
LED_PWM1 = const(0b11)  # output blinks at PWM1 rate


def _leds_to_selectors(leds: list, ls0: int, ls1: int, set_to=LED_OFF) -> (int, int):
    '''Takes a list of LEDs to modify and modifies the passed selector variables
    (ls0, ls1) accroding to the what the set_to argument is specified to (LED_ON,
    LED_OFF, LED_PWM0, LED_PWM1).

    Returns two modified selector variables (ls0, ls1) as a tuple.'''
    ls = (ls1 << 8) | ls0  # make a 16bit int from ls0 and ls1 (easier to work with)
    for led in leds:
        # set LED selector bits to 00, but do not change the other bits
        ls &= (~(0b11 << (led*2)) & 0xFFFF)
        # set the masked out bits to set_to
        ls |= set_to << (led*2)

    # separate ls0 and ls1 from the 16bit ls variable
    return ls & 0xFF, (ls & 0xFF00) >> 8


def _duty_cycle_to_byte(duty_cycle: float) -> bytes:
    '''Returns a byte that maps a float from 0.0..1.0 to an int 255..0. The
    range is reversed to match the PCA9551 duty cycle logic.'''
    assert 0.0 <= duty_cycle <= 1.0, 'enter duty cycle as percent in 0.0 .. 1.0'
    return bytes([ceil((1.0 - duty_cycle) * 255)])


def _duty_cycle_byte_to_percent(duty_cycle: bytes) -> float:
    '''Returns a float (1.0 .. 0.0) converted from the value range (0..255).'''
    dc = int.from_bytes(duty_cycle, 'little')
    return round(1.0 - float(dc/0xff), 2)


class PCA9551:

    def __init__(self, write_callback, read_callback, address=PCA9551_ADDRESS):
        '''Two callback functions must be passed to the constructor to perform
        the I2C operations. The callbacks must take the following arguments:
        
        write_callback(i2c_address: int, register_address: int, data: bytes)
        read_callback(i2c_address: int, register_address: int, num_read: int)
        '''
        self.write_callback = write_callback
        self.read_callback = read_callback
        self._addr = address
    
        self.write = lambda r, b: self.write_callback(self._addr, r, b)
        self.read = lambda r, n: self.read_callback(self._addr, r, n)

        # initial state of LED selectors = all LEDs off
        self.ls0, self.ls1 = 0x55, 0x55

    def read_inputs(self) -> bytes:
        return self.read(INPUT, 1)

    def _change_led_state(self, leds, set_to):
        self.ls0, self.ls1 = _leds_to_selectors(leds, self.ls0, self.ls1, set_to)
        self.write(LS0, bytes([self.ls0]))
        self.write(LS1, bytes([self.ls1]))

    def leds_on(self, leds: list, others_off=True):
        if others_off:
            self.ls0, self.ls1 = 0x55, 0x55
        self._change_led_state(leds, LED_ON)

    def leds_off(self, leds: list):
        self._change_led_state(leds, LED_OFF)
        
    def leds_pwm0(self, leds: list):
        self._change_led_state(leds, LED_PWM0)
    
    def leds_pwm1(self, leds: list):
        self._change_led_state(leds, LED_PWM1)
    
    @property
    def pwm0_duty_cycle(self):
        return _duty_cycle_byte_to_percent(self.read(PWM0, 1))

    @pwm0_duty_cycle.setter
    def pwm0_duty_cycle(self, duty_cycle: float):
        self.write(PWM0, _duty_cycle_to_byte(duty_cycle))
    
    @property
    def pwm1_duty_cycle(self):
        return _duty_cycle_byte_to_percent(self.read(PWM1, 1))

    @pwm1_duty_cycle.setter
    def pwm1_duty_cycle(self, duty_cycle: float):
        self.write(PWM1, _duty_cycle_to_byte(duty_cycle))

    def _write_to_pwm_prescaler(self, prescaler_register, value):
        assert value >= 0 and value <= 255, 'only unsigned 8-bit value allowed'
        self.write(prescaler_register, value)

    @property
    def pwm0_prescaler(self, value):
        self._write_to_pwm_prescaler(PSC0, bytes([value]))
    
    @property
    def pwm1_prescaler(self, value):
        self._write_to_pwm_prescaler(PSC1, bytes([value]))
    