import pydobot
from serial.tools import list_ports
from yaspin import yaspin
import inquirer
import os
import sys

device = None
spinner = yaspin(text="Movendo", color="yellow")
head = None

# Mandar para a posição home
def home():
    #sys.stdout = open(os.devnull, "w")
    spinner.start()
    device.move_to(240.53,0,150.23,0,True)
    spinner.stop()
    #sys.stdout = sys.__stdout__
    print("Robô em sua posição inicial")
    menu()



# Ligar a ferramenta (atuador)
def ligarFerramenta():
    if head == "garra":
        device.grip(True)
        device.wait(200)
    else:
        device.suck(True)
        device.wait(200)
    print("Ferramenta ligada")
    menu()

# Desligar a ferramenta (atuador)
def desligarFerramenta():
    if head == "garra":
        device.grip(False)
        device.wait(200)
    else:
        device.suck(False)
        device.wait(200)
    print("Ferramenta desligada")
    menu()

def quit():
    print("Adieu!")
    exit(1)

def moveA(p : str):
    qtd = round(float(input("Quanto mexer?\n")),2)
    (x,y,z,r,j1,j2,j3,j4) = device.pose()
    match p:
        case "x":
            device.move_to(round(x,2)+qtd,round(y,2),round(z,2),0,True)
            print(f"Robô movido para: [{round(x,2)+qtd}, {round(y,2)}, {round(z,2)}]")
        case "y":
            device.move_to(round(x,2),round(y,2)+qtd,round(z,2),0,True)
            print(f"Robô movido para: [{round(x,2)}, {round(y,2)+qtd}, {round(z,2)}]")
        case "z":
            device.move_to(round(x,2),round(y,2),round(z,2)+qtd,0,True)
            print(f"Robô movido para: [{round(x,2)}, {round(y,2)}, {round(z,2)+qtd}]")
        case _:
            print("Eixo inválido")
    menu()
    
def posicao():
    (x,y,z,r,j1,j2,j3,j4) = device.pose()
    print(f'A posição atual é x: {round(x,2)}, y: {round(y,2)} e z: {round(z,2)}')
    menu()

def menu():
    question = [inquirer.List("command","O que você quer fazer?",["Ajuda","Ligar","Desligar","Home","Mover","Mover em um eixo","Posição","Desligar"])]
    answer = inquirer.prompt(question)
    inter = answer['command']

    match inter:
        case "Ligar":
            ligarFerramenta()
        case "Desligar":
            desligarFerramenta()
        case "Home":
            home()
        case "Fechar":
            quit()
        case "Mover":
            move()
        case "Posição":
            posicao()
        case "Mover em um eixo":
           q = inquirer.prompt([inquirer.List("eixo","Qual eixo?",["X","Y","Z"])])
           moveA(q['eixo'])
        case "Ajuda":
            print("\n- Ligar (liga o atuador)\n- Desligar (desliga o atuador)\n- Home (coloca o Magician em sua posição inicial)\n- Fechar (fecha o programa)\n- Mover (move para as coordenadas x, y e z especificadas)\n- Mover em um eixo (move a garra apenas em um eixo, acrescendo ou diminuindo um valor)\n- Posição (imprime no console a posição do robô) \n- Ajuda (lista todas as funções)")
            menu()
        case _:
            quit()



def move():
    coord = [round(float(i),2) for i in input("Para onde será o movimento? (ex: 100.2, 3.24, -5.9): ").split(", ")]
    spinner.start()
    device.move_to(coord[0],coord[1],coord[2],0,True)
    spinner.stop()
    spinner.ok("✅ ")
    print(f"Robô movido para: [{coord[0]}, {coord[1]}, {coord[2]}]")
    menu()

# if __name__ == "__main__":
available_ports = list_ports.comports()
try:
    port = available_ports[0].device
    device = pydobot.Dobot(port=port, verbose=False)
except:
    port = available_ports[1].device
    device = pydobot.Dobot(port=port, verbose=False)
print("\nOlá! esta é uma pequena interface gráfica para interagir com o robô")
head = str(input("\nInicialmente, qual o atuador sendo utilizado? (garra ou ventosa)\n- "))
menu()

