from Finchbot.BirdBrain import Finch
from time import sleep
from enum import Enum
import math

class BotStateEnum(Enum):
    detecting = 'detecting'
    chasing = 'chasing'
    goingBehind = 'goingBehind'

botStateEnum:BotStateEnum = BotStateEnum.detecting

DELAY_VALUE:float = 0.001 #.001 of a second = 1 millisecond

finch:Finch = Finch()

speed:float = 30
maxSpeed:float = 30
rangeDist:float = 50
prevDist = 0

def goBehind(distOfEnemy:float, turnNumber:int):
    print('GOING behind')
    # finch.setTurn('R', 90, 100)
    # global speed
    # speed = maxSpeed
    # finch.setMotors(maxSpeed, maxSpeed)

    # return 
    if(turnNumber>3):
        global botStateEnum
        botStateEnum = BotStateEnum.detecting
        return
    
    finchSpeed:float = 20 #TODO:Measure this

    print('TURNING')
    finch.setTurn('R', 60, 100)
    finch.setMotors(maxSpeed, maxSpeed)

    distToCoverInFirstTurn:float = ((distOfEnemy/2)/math.sin(1.0472))#around (distOfEnemy/2)/0.86

    timeBeforeAnotherTurn:float = distToCoverInFirstTurn/finchSpeed #time = distance/velocity

    timeElapsed:float = 0
    while(True):
        if(adjustIfOnBoundary()):
            break

        if(timeElapsed >= timeBeforeAnotherTurn):
            goBehind(distOfEnemy=distOfEnemy, turnNumber=(turnNumber+1))
            break
        else:
            print(f'STILL GOING BEHIND elapsed{timeElapsed}, nextTurn {timeBeforeAnotherTurn}')
            # finch.setMotors(30, 30)

        sleep(DELAY_VALUE)
        timeElapsed+=DELAY_VALUE

def rotate():
    global botStateEnum
    botStateEnum = BotStateEnum.detecting

    global speed
    speed = 0
    finch.setMotors(speed, speed)
    finch.setTurn('R', 40, 100)

def adjustIfOnBoundary() -> bool:

    leftLightReflected = finch.getLine('L')
    rightLightReflected = finch.getLine('R')

    # print(f"light reflected: left {leftLightReflected}, right {rightLightReflected}")
    if(leftLightReflected < 80 or rightLightReflected < 80):
        print('On boundary')
        finch.setMotors(-maxSpeed, -maxSpeed)
        sleep(0.5)
        rotate()
        return True
    
    return False

finch.print('TECHBOT')
finch.setTail("all", 123, 240, 126)

detectionTimes:int = 0

while True:
    dist = finch.getDistance()

    adjustIfOnBoundary()

    if(botStateEnum == BotStateEnum.detecting):
        if(detectionTimes%2==0 or detectionTimes==0): rotate() #rotate on every even turn
        #detect dist and prevDist

        if(((detectionTimes%2 != 0)) and dist<rangeDist): #every odd turn, when prevDist has been populated along with presentDist, see the distance difference in this rotation angle
        #bot is close
            if(dist>=(prevDist+1)):
                #the other bot is moving is running away or is still, so slam it out of the ring.
                print('Bot running away from me')
                botStateEnum = BotStateEnum.chasing
            elif(dist<(prevDist-1)):
            #the other bot is coming towards us.
                print('Bot coming towards me')
                botStateEnum = BotStateEnum.goingBehind
            else:
                print('Might be inaccurate detection')

        else:
            print('No bot in my range')

    elif(botStateEnum == BotStateEnum.chasing):
        # finch.setMotors(100, 100)
        print('Chasing')
        finch.setMotors(maxSpeed, maxSpeed)
        # finch.setMotors(0, 0)
    elif(botStateEnum == BotStateEnum.goingBehind):
        # finch.setMotors(maxSpeed, maxSpeed)
        goBehind(distOfEnemy=dist, turnNumber=1)

    if(finch.getButton('A') or finch.getButton('B')):
        print('Stopping.')
        finch.setMotors(0,0)
        break

    detectionTimes+=1
    prevDist = dist
    sleep(DELAY_VALUE)