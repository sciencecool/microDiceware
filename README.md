# microDiceware
 Using MicroPython to generate random diceware words for secure password creation
## what?
Some simple MicroPython code, a Raspberry Pico, a generic button and SSD1306 OLED screen, combine into a tiny device that generates (hopefully) random diceware words with which one can make a password.
## why?
Diceware is the best way to make passwords, but keeping/using a paper word list and dice is cumbersome. I don't trust online diceware password generators, so I wanted an airgapped solution based on a Pico which has no wireless connectivity to speak of. The output should be 'true' random because it's seeded by random user input combined with a sensor (temperature) reading, and I assume that once you cut the power there is no log of the previously generated seed, so it should be opsec proof.

## attribution?
SSD1306 library (probably) from adafruit: https://learn.adafruit.com/micropython-hardware-ssd1306-oled-display/micropython  
Diceware word list: https://theworld.com/~reinhold/diceware.wordlist.asc  
