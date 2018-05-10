import unittest
import random
import pca9551


class TestPCA9551Driver(unittest.TestCase):
    
    test_data = (
        ([0],       0x55, 0x55, pca9551.LED_ON, (0x54, 0x55)),
        ([0, 1],    0xa5, 0xbc, pca9551.LED_ON, (0xa0, 0xbc)),
        ([1, 5],    0x38, 0xdf, pca9551.LED_ON, (0x30, 0xd3)),
        ([0, 2, 5], 0xbb, 0x57, pca9551.LED_ON, (0x88, 0x53)),

        ([6, 7],    0x24, 0x6b, pca9551.LED_OFF, (0x24, 0x5b)),
        ([1, 4],    0xdd, 0xf4, pca9551.LED_OFF, (0xd5, 0xf5)),
        ([0, 2, 7], 0x4c, 0x41, pca9551.LED_OFF, (0x5d, 0x41)),
        ([2, 5, 7], 0x96, 0x21, pca9551.LED_OFF, (0x96, 0x65)),

        ([1, 7],    0x50, 0x57, pca9551.LED_PWM0, (0x58, 0x97)),
        ([0, 5],    0xef, 0x5e, pca9551.LED_PWM0, (0xee, 0x5a)),
        ([0, 2, 5], 0x31, 0xa1, pca9551.LED_PWM0, (0x22, 0xa9)),
        ([1, 3, 7], 0x44, 0xe0, pca9551.LED_PWM0, (0x88, 0xa0)),

        ([0, 1],    0x8c, 0xeb, pca9551.LED_PWM1, (0x8f, 0xeb)),
        ([3, 7],    0x52, 0x51, pca9551.LED_PWM1, (0xd2, 0xd1)),
        ([0, 2, 5], 0xba, 0x2a, pca9551.LED_PWM1, (0xbb, 0x2e)),
        ([5, 6, 7], 0xa2, 0xb6, pca9551.LED_PWM1, (0xa2, 0xfe)),
    )

    def test_leds_to_selectors_no_change(self):
        for _ in range(10):  # 10 random integers
            a, b = random.randint(0x00, 0xff), random.randint(0x00, 0xff)
            self.assertEqual(pca9551._leds_to_selectors([], a, b, 0x00), (a, b))

    def test_leds_to_selectors(self):
        for leds, ls0, ls1, set_to, expected in self.test_data:
            self.assertEqual(pca9551._leds_to_selectors(leds, ls0, ls1, set_to), expected)

    def test_duty_cycle_to_byte(self):
        self.assertEqual(pca9551._duty_cycle_to_byte(1.0), b'\x00')
        self.assertEqual(pca9551._duty_cycle_to_byte(0.0), b'\xff')
        self.assertEqual(pca9551._duty_cycle_to_byte(0.5), b'\x80')
    
    def test_duty_cycle_byte_to_percent(self):
        self.assertAlmostEqual(pca9551._duty_cycle_byte_to_percent(b'\x00'), 1.0)
        self.assertAlmostEqual(pca9551._duty_cycle_byte_to_percent(b'\xff'), 0.0)
        self.assertAlmostEqual(pca9551._duty_cycle_byte_to_percent(b'\x80'), 0.5)

if __name__ == '__main__':
    unittest.main()
