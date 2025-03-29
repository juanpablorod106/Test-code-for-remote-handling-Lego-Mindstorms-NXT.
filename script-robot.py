import nxt
import nxt.locator
from nxt.motor import Motor
import sys
import tty
import termios

class NXTController:
    def __init__(self):
        # Conectar con el NXT via Bluetooth
        print("Buscando NXT...")
        self.brick = nxt.locator.find_one_brick()
        print("Conectado al NXT!")
        
        # Inicializar motores (usando los puertos correctos)
        self.motor_left = Motor(self.brick, nxt.locator.PORT_B)  # Motor izquierdo
        self.motor_right = Motor(self.brick, nxt.locator.PORT_C)  # Motor derecho
        
        # Velocidades
        self.speed = 75  # Velocidad normal (0-127)
        self.turn_speed = 50  # Velocidad de giro
        
    def move_forward(self):
        self.motor_left.run(self.speed)
        self.motor_right.run(self.speed)
        
    def move_backward(self):
        self.motor_left.run(-self.speed)
        self.motor_right.run(-self.speed)
        
    def turn_left(self):
        self.motor_left.run(-self.turn_speed)
        self.motor_right.run(self.turn_speed)
        
    def turn_right(self):
        self.motor_left.run(self.turn_speed)
        self.motor_right.run(-self.turn_speed)
        
    def stop(self):
        self.motor_left.idle()
        self.motor_right.idle()
        
    def close(self):
        self.stop()
        self.brick.sock.close()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    controller = NXTController()
    
    print("Controles:")
    print("W - Adelante")
    print("A - Izquierda")
    print("S - Atrás")
    print("D - Derecha")
    print("ESPACIO - Detener")
    print("Q - Salir")
    
    try:
        while True:
            char = getch()
            
            if char == 'w':
                controller.move_forward()
                print("Adelante")
            elif char == 's':
                controller.move_backward()
                print("Atrás")
            elif char == 'a':
                controller.turn_left()
                print("Izquierda")
            elif char == 'd':
                controller.turn_right()
                print("Derecha")
            elif char == ' ':
                controller.stop()
                print("Detener")
            elif char == 'q':
                print("Saliendo...")
                break
                
    except KeyboardInterrupt:
        print("\nInterrupción por teclado")
    finally:
        controller.close()

if __name__ == '__main__':
    main()
