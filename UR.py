import socket
import serial
import time
import math
#[-0.78, -1.57, -1.57, 0, 1.57, 0]
class UR:
    def __init__(self, ip='192.168.1.2', port=30003, grip_port='COM11',
                 home=[0.42855, 0.2628, 0.4340, -2.6952, 1.5921, 0.0067], delta=0.05, alpha=45):
        self.alpha = alpha * math.pi / 180
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.grip_port = grip_port
        self.home = home
        self.current_position = home
        self.delta = delta

    def go_home(self, vel=0.5, acc=1):
        self.sock.send('movej(p' + str(self.home) + ', a=' + str(acc) + ', v=' + str(vel) + ')\n')
        time.sleep(5)

    def move_forward(self, axis, vel=0.1, acc=0.1):
        if axis is 'g':
            self._gripper_open()
            return
        ex_time = self.delta / vel + 0.5 * vel / acc
        if axis is 'x':
            self.current_position[0] += self.delta * math.cos(self.alpha)
            self.current_position[1] += self.delta * math.sin(self.alpha)
        elif axis is 'y':
            self.current_position[0] -= self.delta * math.sin(self.alpha)
            self.current_position[1] += self.delta * math.cos(self.alpha)
        elif axis is 'z':
            self.current_position[2] += self.delta
        self.sock.send('movep(p' + str(self.current_position) + ', a=' + str(acc) + ', v=' + str(vel) + ')\n')
        time.sleep(ex_time)

    def move_backward(self, axis, vel=0.1, acc=0.1):
        if axis is 'g':
            self._gripper_close()
            return
        ex_time = self.delta / vel + 0.5 * vel / acc
        if axis is 'x':
            self.current_position[0] -= self.delta * math.cos(self.alpha)
            self.current_position[1] -= self.delta * math.sin(self.alpha)
        elif axis is 'y':
            self.current_position[0] += self.delta * math.sin(self.alpha)
            self.current_position[1] -= self.delta * math.cos(self.alpha)
        elif axis is 'z':
            self.current_position[2] -= self.delta
        self.sock.send('movep(p' + str(self.current_position) + ', a=' + str(acc) + ', v=' + str(vel) + ')\n')
        time.sleep(ex_time)

    def _gripper_open(self):
        ser = serial.Serial(port=self.grip_port, baudrate=115200, timeout=1, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        ser.write("\x09\x10\x03\xE8\x00\x03\x06\x00\x00\x00\x00\x00\x00\x73\x30")
        time.sleep(1)
        ser.write("\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\x00\xFF\xFF\x72\x19")
        time.sleep(10)

    def _gripper_close(self):
        ser = serial.Serial(port=self.grip_port, baudrate=115200, timeout=1, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        ser.write("\x09\x10\x03\xE8\x00\x03\x06\x00\x00\x00\x00\x00\x00\x73\x30")
        time.sleep(1)
        ser.write("\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\x00\xFF\xFF\x72\x19")
        time.sleep(10)


if __name__ == "__main__":
    ur = UR()
    ur.gripper_close()
    # ur.gripper_open()
    # ur.go_home()
    # a = 'x'
    # time.sleep(2)
    # start = time.time()
    # ur.move_forward(a)
    # print(time.time() - start)
    # start = time.time()
    # ur.move_forward(a)
    # print(time.time() - start)
    # start = time.time()
    # ur.move_forward(a)
    # print(time.time() - start)
    # start = time.time()
    # ur.move_forward(a)
    # print(time.time() - start)
    # start = time.time()
    # ur.move_forward(a)
    # print(time.time() - start)
    # # time.sleep(2)
    # ur.move_forward(a)
    # time.sleep(2)
    # ur.move_forward(a)
    # time.sleep(2)
    # ur.move_forward(a)
    # time.sleep(2)
    # ur.move_forward(a)
    # time.sleep(4)
    # ur.move_backward(a)
    # time.sleep(2)
    # ur.move_backward(a)
    # time.sleep(2)
    # ur.move_backward(a)
    # time.sleep(2)
    # ur.move_backward(a)
    # time.sleep(2)
    # ur.move_backward(a)
