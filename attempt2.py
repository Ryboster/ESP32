from machine import Pin, Timer
import ubluetooth
from time import sleep_ms
from esp32 import raw_temperature
import bleparser

class BLE():
    def __init__(self, name):
        self.name = name             # Set the discoverable name
        self.ble = ubluetooth.BLE()   # Initialize the Bluetooth Low Energy module
        self.ble.active(True)         # Activate the Bluetooth module

        self.led = Pin(2, Pin.OUT)    # Initialize the LED on pin 2
        self.timer1 = Timer(0)        # Initialize Timer 0
        self.timer2 = Timer(1)        # Initialize Timer 1
        
        self.disconnected()           # Call the disconnected method
        self.ble.irq(self.ble_irq)    # Set the interrupt handler for Bluetooth events
        self.register()               # Call the register method to set up services
        self.advertiser()             # Start BLE advertising
        self.found_addresses = []	  # Create a list object for handling of discovered devices
    
    def scan(self):
        self.ble.gap_scan(10000)
        
    def connected(self):
        self.timer1.deinit()          # Deinitialize Timer 1
        self.timer2.deinit()          # Deinitialize Timer 2

    def disconnected(self):
        self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))

    def ble_irq(self, event, data):
        if event == 1:
            '''Central disconnected'''
            self.connected()
            self.led(1)
        
        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()
        
        elif event == 3:
            '''New message received'''            
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            print(message)
            if message == 'red_led':
                red_led.value(not red_led.value())
                print('red_led', red_led.value())
                ble.send('red_led' + str(red_led.value()))
            if message == 'read_temp':
                print(sensor.read_temperature(True))
                ble.send(str(sensor.read_temperature(True)))
            if message == 'read_hum':
                print(sensor.read_humidity())
                ble.send(str(sensor.read_humidity()))
                
        elif event == 5:
            '''Scan result received'''
            print(data)
            addr_type, address, adv_type, signal_strength, idk = data
            if addr_type == 0:
                addr_type = "public"
            elif addr_type == 1:
                addr_type = "private"
            address = ':'.join(hex(x)[2:] for x in address)
            idk = ':'.join(hex(x)[2:] for x in idk)
            print(idk)
            

    def register(self):
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
        
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
        
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)
        
BLE("BT32").scan()
