import pydobot
from serial.tools import list_ports
import os
import sys
import easygui

device = None
head = None

# Mandar para a posição home
def home():
    sys.stdout = open(os.devnull, "w")
    device.move_to(240.53,0,150.23,0,True)
    sys.stdout = sys.__stdout__
    menu("Robô em sua posição inicial")

# Ligar a ferramenta (atuador)
def ligarFerramenta():
    if head == "Garra":
        sys.stdout = open(os.devnull, "w")
        device.grip(True)
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, "w")
        device.suck(True)
        sys.stdout = sys.__stdout__
    menu("Ferramenta ligada")

# Desligar a ferramenta (atuador)
def desligarFerramenta():
    if head == "Garra":
        sys.stdout = open(os.devnull, "w")
        device.grip(False)
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, "w")
        device.suck(False)
        sys.stdout = sys.__stdout__
    menu("Ferramenta desligada")

def quit():
    easygui.textbox("Adieu!","Fechar")
    exit(1)

def moveA():
    msg = "Qual eixo?"
    opt = ["x","y","z"]
    p = easygui.choicebox(msg,"Escolha de eixo", choices = opt)
    msg1 = "Quanto mexer?"
    qtd = round(float(easygui.enterbox(msg1,"Quantidade","ex. -10")),2)
    sys.stdout = open(os.devnull, "w")
    (x,y,z,r,j1,j2,j3,j4) = device.pose()
    match p:
        case "x":
            device.move_to(round(x,2)+qtd,round(y,2),round(z,2),0,True)
            menu("Movido no eixo x em " + str(qtd))
        case "y":
            device.move_to(round(x,2),round(y,2)+qtd,round(z,2),0,True)
            menu("Movido no eixo y em " + str(qtd))
        case "z":
            device.move_to(round(x,2),round(y,2),round(z,2)+qtd,0,True)
            menu("Movido no eixo z em " + str(qtd))
        case _:
            sys.stdout = sys.__stdout__
            menu("Eixo inválido")
    
def posicao():
    sys.stdout = open(os.devnull, "w")
    (x,y,z,r,j1,j2,j3,j4) = device.pose()
    sys.stdout = sys.__stdout__
    #msgUltima = f'A posição atual é x: {round(x,2)}, y: {round(y,2)} e z: {round(z,2)}'
    menu(f'A posição atual é x: {round(x,2)}, y: {round(y,2)} e z: {round(z,2)}')

def menu(te : str):
    msg = "O que você quer fazer? (caso queira saber as funções presentes, pressione 'ajuda')\n\nMensagem mais recente: " +te
    opt = ["Ajuda","Ligar", "Desligar","Home","Mover","Mover em um eixo", "Posição atual","Fechar"]
    inter = easygui.choicebox(msg, choices = opt)
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
        case "Posição atual":
            posicao()
        case "Mover em um eixo":
           moveA()
        case "Ajuda":
            ajuda()
        case _:
            quit()

def ajuda():
    easygui.textbox("O que cada comando faz de maneira simplificada","Ajuda","- ligar (liga o atuador)\n- desligar (desliga o atuador)\n- home (coloca o Magician em sua posição inicial)\n- fechar (fecha o programa)\n- mover (move para as coordenadas x, y e z especificadas)\n- mover em um eixo (move a garra apenas em um eixo, acrescendo ou diminuindo um valor)\n- posição (imprime no console a posição do robô) \n- ajuda (lista todas as funções)")
    menu("")

def move():
    msg = "Para onde será o movimento?:"
    title = "Mover"
    exText = "ex: 100.2, 3.24, -5.9"
    coord = [round(float(i),2) for i in easygui.enterbox(msg,title,exText).split(", ")]
    sys.stdout = open(os.devnull, "w")
    device.move_to(coord[0],coord[1],coord[2],0,True)
    sys.stdout = sys.__stdout__
    menu(f'A posição atual é x: {round(float(coord[0]),2)}, y: {round(float(coord[1]),2)} e z: {round(float(coord[2]),2)}')

# if __name__ == "__main__":
available_ports = list_ports.comports()
sys.stdout = open(os.devnull, "w")
try:
    port = available_ports[0].device
    device = pydobot.Dobot(port=port, verbose=True)
except:
    port = available_ports[1].device
    device = pydobot.Dobot(port=port, verbose=True)
sys.stdout = sys.__stdout__

msg = "Olá! esta é uma pequena interface gráfica para interagir com o robô\nInicialmente, qual o atuador sendo utilizado?"
opt = ["Garra", "Ventosa"]
head = easygui.choicebox(msg,"Interface de interação com o Magician Lite", choices = opt)
menu("")

