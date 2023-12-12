from Finchbot.BirdBrain import Finch
from time import sleep
from enum import Enum

DELAY_VALUE:float = 0.1 #.1 of a second = 100 milliseconds

finch:Finch = Finch()

prevDist = 0

def goBehind():
    pass

def rotate():
    finch.setTurn('R', 20, 100)

def adjustIfOnBoundary():
    pass

moving:bool = False

class BotStateEnum(Enum):
    detecting = 'detecting'
    chasing = 'chasing'
    goingBehind = 'goingBehind'

botStateEnum:BotStateEnum = BotStateEnum.detecting

while True:
    dist = finch.getDistance()

    adjustIfOnBoundary()

    if(botStateEnum == BotStateEnum.detecting):
        rotate()
        if(dist<50):
        #bot is close
            if(dist>=(prevDist)):
                #the other bot is moving is running away or is still, so slam it out of the ring.
                print('Bot running away from me')
                botStateEnum = BotStateEnum.chasing
            else:
            #the other bot is coming towards us.
                print('Bot coming towards me')
                botStateEnum = BotStateEnum.goingBehind
        else:
            print('No bot in my range')
            moving=False
    elif(botStateEnum == BotStateEnum.chasing):
        # finch.setMotors(100, 100)
        finch.setMotors(5, 5)
        # finch.setMotors(0, 0)
    elif(botStateEnum == BotStateEnum.goingBehind):
        goBehind()

    prevDist = dist

    sleep(DELAY_VALUE)