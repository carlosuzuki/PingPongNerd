from machine import Pin
from utime import sleep
from neopixel import Neopixel
import pingPongNerd

#button1 = Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
#button2 = Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)

button1 = Pin(22, machine.Pin.IN)
button2 = Pin(1, machine.Pin.IN)

###########################Início configurações fita#################################
# número de pixels
numpix = 112
# objeto strip com quantidade de pixels, máquina de estado, número GPIO e modo de cor
strip = Neopixel(numpix, 0, 3, "GRB")
  
# Cores com índices R, B e B em cada uma
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 150, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (75, 0, 130)
violet = (138, 43, 226)
pink = (255, 102, 178)
cyan = (0, 204, 204)
white = (255, 255, 255)
colors_rgb = (red, orange, yellow, green, blue, indigo, violet, pink, cyan, white)
  
# Brilho da fita
strip.brightness(300)
###########################FIM configurações fita#################################

def firula1(cor):
    for i in range(111):
        strip.set_pixel(i, cor)
        sleep(0.003)
        strip.show()
        
def firula2(cor): 
    for i in range(111, -1, -1):
        strip.set_pixel(i, cor)
        sleep(0.003)
        strip.show()

def InfracaoTipo3():
    global actualLed
    global numpix
    global endOfGame
    global loser
    
    if actualLed >= numpix-1:
        endOfGame = True
        loser = "Player2"
    if actualLed <= 0:
        endOfGame = True
        loser = "Player1"
        
def AtualizaPosicaoLed():
    global endOfGame
    global direction
    global actualLed
    
    if not endOfGame:  
        if direction:
            actualLed -= 1
        else:
            actualLed += 1        

def UpdateStripActualLed():
    global endOfGame
    global middleLed
    global middleFieldColor
    global actualLed
    global blue
    global transitionDelay
    
    if not endOfGame:        
        strip.set_pixel(middleLed, middleFieldColor)
        strip.set_pixel(actualLed, blue)
        strip.show()
        sleep(transitionDelay)
        strip.clear()
        
def EndOfGame():
    global endOfGame
    global loser
    global middleLed
    global actualLed
    global numpix
    global red
    global green
    global blue
    global middleFieldColor
    
    if endOfGame:
        if loser == "Player1":
            for i in range(middleLed, 0, -1):
                strip.set_pixel(i, red)
            for i in range(middleLed, numpix, 1):
                strip.set_pixel(i, green)    
            strip.set_pixel(middleLed, middleFieldColor)
            strip.set_pixel(actualLed, blue)
            strip.show()
            sleep(0.100)
            loser = ""
            
        if loser == "Player2":
            for i in range(middleLed, 0, -1):
                strip.set_pixel(i, green)
            for i in range(middleLed, numpix, 1):
                strip.set_pixel(i, red)    
            strip.set_pixel(middleLed, middleFieldColor)
            strip.set_pixel(actualLed, blue)
            strip.show()
            sleep(0.100)
            loser = ""

def RestartGame():
    global endOfGame
    global actualLed
    global numpix
    global transitionDelay
    global stepSize
    global direction
    global auxButton1 
    global auxButton2
    global loser
    global leve
    global middleFieldColor
    global white 
    
    if endOfGame and not button1.value() and not button1.value():
        #middleLed = numpix//2
        actualLed = numpix//2
        transitionDelay = 0.800
        stepSize = 0.100
        direction = True  
        auxButton1 = True  #Player1
        auxButton2 = False #Player2
        endOfGame = False
        loser = ""
        sleep(0.500)
        level = "Easy"
        middleFieldColor = white            

def TransitionSpeedController():
    global transitionDelay
    global level
    global middleFieldColor
    global yellow
    global stepSize
    
    if transitionDelay <= 0.001:
        level = "Hard"
        middleFieldColor = yellow     
        transitionDelay = 0.000
        stepSize = 0.000
    elif transitionDelay <= 0.050:
        stepSize = 0.002
    elif transitionDelay <= 0.400:
        stepSize = 0.050

def Button1Read():
    global auxButton1
    global auxButton2
    global actualLed 
    global middleLed
    global level
    global endOfGame
    global loser
    global direction
    global transitionDelay
    global stepSize

    if not button1.value():
        while not button1.value():
            sleep(0.150)
        if auxButton1:
            if actualLed <= middleLed:             
                if level == "Hard" and actualLed == middleLed:
                    endOfGame = True
                    loser = "Player2"         
                else:
                    auxButton1 = False
                    auxButton2 = True
                    direction = not direction
                    transitionDelay = transitionDelay - stepSize                   
            else: #Infração: "bateu no campo do adversário"
                endOfGame = True
                loser = "Player1"       
        else: #Infração: "bateu duas vezes na bola"
            endOfGame = True
            loser = "Player1"

def Button2Read():
    global auxButton1
    global auxButton2
    global actualLed 
    global middleLed
    global level
    global endOfGame
    global loser
    global direction
    global transitionDelay
    global stepSize
    if not button2.value():
        while not button2.value():
            sleep(0.150)
        if auxButton2:
            if actualLed >= middleLed:
                if level == "Hard" and actualLed == middleLed:
                    endOfGame = True
                    loser = "Player1"         
                else:
                    auxButton1 = True
                    auxButton2 = False
                    direction = not direction
                    transitionDelay = transitionDelay - stepSize                 
            else: #Infração: "bateu no campo do adversário"
                endOfGame = True
                loser = "Player2"              
        else: #Infração: "bateu duas vezes na bola"
            endOfGame = True
            loser = "Player2"            

def Initialization():
    global middleFieldColor
    global numpix
    global green
    global red
    global orange
    global blue
    
    firula1(green)
    firula2(red)
    firula1(orange)
    firula2(blue) 
    strip.set_pixel(numpix//2, middleFieldColor)
    strip.show()   
    
middleLed = numpix//2
actualLed = numpix//2
transitionDelay = 0.800
stepSize = 0.100
direction = True  
auxButton1 = True  #Player1
auxButton2 = False #Player2
endOfGame = False
loser = ""
level = "Easy"
middleFieldColor = white

Initialization()

while True:
    UpdateStripActualLed()
    TransitionSpeedController()
    Button1Read()
    Button2Read()
    InfracaoTipo3()
    AtualizaPosicaoLed()
    EndOfGame()
    RestartGame()