import pydobot
from serial.tools import list_ports
import os
import sys

device = None
head = None

# Mandar para a posição home
def home():
    sys.stdout = open(os.devnull, "w")
    device.move_to(240.53,0,150.23,0,True)
    sys.stdout = sys.__stdout__
    print("Robô em sua posição inicial")
    menu()



# Ligar a ferramenta (atuador)
def ligarFerramenta():
    if head == "garra":
        sys.stdout = open(os.devnull, "w")
        device.grip(True)
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, "w")
        device.suck(True)
        sys.stdout = sys.__stdout__
    print("Ferramenta ligada")
    menu()

# Desligar a ferramenta (atuador)
def desligarFerramenta():
    if head == "garra":
        sys.stdout = open(os.devnull, "w")
        device.grip(False)
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, "w")
        device.suck(False)
        sys.stdout = sys.__stdout__
    print("Ferramenta desligada")
    menu()

def quit():
    print("Adieu!")
    exit(1)

def moveA(p : str):
    qtd = round(float(input("Quanto mexer?\n")),2)
    sys.stdout = open(os.devnull, "w")
    (x,y,z,r,j1,j2,j3,j4) = device.pose()
    match p:
        case "x":
            device.move_to(round(x,2)+qtd,round(y,2),round(z,2),0,True)
        case "y":
            device.move_to(round(x,2),round(y,2)+qtd,round(z,2),0,True)
        case "z":
            device.move_to(round(x,2),round(y,2),round(z,2)+qtd,0,True)
        case _:
            sys.stdout = sys.__stdout__
            print("Eixo inválido")
    sys.stdout = sys.__stdout__
    menu()
    
def posicao():
    sys.stdout = open(os.devnull, "w")
    (x,y,z,r,j1,j2,j3,j4) = device.pose()
    sys.stdout = sys.__stdout__
    print(f'A posição atual é x: {round(x,2)}, y: {round(y,2)} e z: {round(z,2)}')
    menu()

def menu():
    inter = str(input("\nO que você quer fazer? (caso queira saber as funções presentes, digite 'ajuda') \n- "))
    match inter:
        case "ligar":
            ligarFerramenta()
        case "desligar":
            desligarFerramenta()
        case "home":
            home()
        case "fechar":
            quit()
        case "mover":
            move()
        case "posição":
            posicao()
        case "mover em um eixo":
           moveA(input("Qual eixo? \n"))
        case "ajuda":
            print("\n- ligar (liga o atuador)\n- desligar (desliga o atuador)\n- home (coloca o Magician em sua posição inicial)\n- fechar (fecha o programa)\n- mover (move para as coordenadas x, y e z especificadas)\n- mover em um eixo (move a garra apenas em um eixo, acrescendo ou diminuindo um valor)\n- posição (imprime no console a posição do robô) \n- ajuda (lista todas as funções)")
            menu()
        case _:
            quit()



def move():
    coord = [round(float(i),2) for i in input("Para onde será o movimento? (ex: 100.2, 3.24, -5.9): ").split(", ")]
    sys.stdout = open(os.devnull, "w")
    device.move_to(coord[0],coord[1],coord[2],0,True)
    sys.stdout = sys.__stdout__
    menu()

if __name__ == "__main__":
    available_ports = list_ports.comports()
    sys.stdout = open(os.devnull, "w")
    try:
        port = available_ports[0].device
        device = pydobot.Dobot(port=port, verbose=True)
    except:
        port = available_ports[1].device
        device = pydobot.Dobot(port=port, verbose=True)
    sys.stdout = sys.__stdout__
    print("\nOlá! esta é uma pequena interface gráfica para interagir com o robô")
    head = str(input("\nInicialmente, qual o atuador sendo utilizado? (garra ou ventosa)\n- "))
    menu()

