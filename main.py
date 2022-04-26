from machine import Pin, I2C, ADC
from utime import sleep
import ssd1306
import random
#import dht

##### SETUP HARDWARE #####

#defining the button pin
button = Pin(5, Pin.IN, Pin.PULL_UP)

#setting up the oled screen
i2c = I2C(0, scl=Pin(1), sda=Pin(0),freq=400000)
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

#setting up sensors
#sensor = dht.DHT11(Pin(14, Pin.OUT, Pin.PULL_DOWN))
adc = machine.ADC(4)

##### SETUP FUNCTIONS #####

#urandom is missing randint and function so define one:
def randint(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = random.getrandbits(30) // div
    val = min + offset
    return val

#source: https://gist.github.com/damianzim/4ddc025f48af7634fb6fe89063659367
def shuffled(array: list, seed: int) -> list:
    length_ = len(array)
    shuffled = [0]*length_
    seed_pos = seed ^ 0xFFFF
    for i in list(reversed(range(length_))):
        index = seed_pos % (i + 1)
        shuffled[i] = array.pop(index)
    return shuffled

##### PROGRAM START #####

#welcome
oled.text("Welcome!",0,0)
oled.text("Let's generate",0,10)
oled.text("diceware words.",0,20)
oled.show()
sleep(2)
oled.fill(0)
oled.show()

#instruction for random seed
oled.text("Repeatedly press",0,0)
oled.text("the button for",0,10)
oled.text("a random seed",0,20)
oled.show()
sleep(0.1)

#take input for random seed
zerocount = 0
onecount = 0
seconds = 0
print("user generating seed")
while seconds < 5:
    if button.value() == 0:
        zerocount += 1
        sleep(0.01)
        seconds += 0.01
    if button.value() == 1:
        onecount += 1
        sleep(0.01)
        seconds += 0.01

seed = (onecount + 8) * (adc.read_u16()) ** zerocount
sleep(0.1)
print("the seed is:", seed)

#text
oled.fill(0)
oled.show()
oled.text("OK! That'll do.",0,0)
oled.text("Generating your",0,10)
oled.text("words...",0,20)
oled.show()

random.seed(int(seed))

#generating random nums
numslist = []
for i in range(8): #range can be whatever but i don't need more than 7 at a time
    numslist.append(randint(1,7776)) #7776 words in words.txt

numslist.sort()
randwords = []

with open("words.txt") as file_in:
    lines = 1
    for line in file_in:
        if lines in numslist:
            randwords.append(line.strip())
            lines += 1
        if lines not in numslist:
            lines += 1

#prevent alphabetical password
print("shuffling words")
print("pre shuffle: ", randwords)
randwords = shuffled(randwords, seed)
print("post shuffle: ", randwords)

#show the random words 
oled.fill(0)
oled.show()

worded = 0
print("first word:", randwords[worded])
while worded < len(randwords):
    if button.value() == 0:
        oled.text(str(str(worded+1) + ": " + str(randwords[worded])),0,10)
        oled.show()
        sleep(0.1)
    if button.value() == 1:
        oled.fill(0)
        oled.show()
        worded += 1
        if worded < len(randwords):
            print("next word:", randwords[worded])
        sleep(0.3)

if worded >= len(randwords):
    oled.text("that's all folks",0,10)
    oled.show()
    print("run complete")
    

#turn off