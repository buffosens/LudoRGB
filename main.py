# Hier werden externe Module importiert. Das heißt jemand anderes hat für das Programm schon einmal Code geschrieben den du hier nur benennen mußt um ihn einfach zu benutzen (wie z.B. die Funktion aus dem Zufallszahlengenerator)
import time
from time import sleep
from random import randint
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# ---------------------------------------------------------------------------------------------------------

# Hier kommen Konstanten hin, das heißt Variablen die ihren Wert zu Laufzeit nicht ändern sollen. Das drückt man damit aus, indem man dem Namen nur Großbuchstaben gibt. ACHTUNG: die Bezeichnungen müssen eindeutig sein, das heißt kein Name darf mehr als einmal vorkommen
BUTTON_GPIO_ROT = 16
BUTTON_GPIO_BLAU = 26
BUTTON_GPIO_GELB = 19
BUTTON_GPIO_GRUEN = 13
LED_COUNT = 100

# Farbem

FARBE_BLAU = (50,0,0)

# Hier wird die Schnittstelle auf dem Pi initialisiert. Das bedeutet wir sagen dem Pi wo wir die Led-Kette angeschlossen haben und welchen Mechanismus (Bus) wir verwenden wollen um alle LEDs anzusprechen (in diesem Fall einen SPI-Bus)
SPI_PORT = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(
    LED_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

# Hier unsere Definition des Spielfeldes im Sinne eines Dictionaries. Ab jetzt gilt: die Bezeichnungen beziehen sich auf die LED-Nummer minus 1!
spielfeld_leds = {1: 0, 2: 1, 3: 2, 4: 3, 5: 11, 6: 12, 7: 15, 8: 14, 9: 20,
                           10: 23, 11: 25, 12: 26, 13: 27, 14: 28, 15: 36, 16: 37, 17: 38, 18: 43, 19: 46,
                           20: 47, 21: 52, 22: 53, 23: 54, 24: 57, 25: 65, 26: 66, 27: 67, 28: 72, 29: 73,
                           30: 74, 31: 50, 32: 78, 33: 79, 34: 82, 35: 90, 36: 91, 37: 92, 38: 97, 39: 98,
                           40: 99}

# die maximale Anzahl der Felder ergibt sich aus den definierten Feldern an sich oben drüber - damit wir bspw. alle auf einmal anmachen können oder ähnliches.
MAXIMALE_FELDZAHL = len(spielfeld_leds)

# Hier die Definition der Würfel. Richtig ist, dass die Namen wieder eindeutig sein müssen, von daher hier alles richtig. Da es insgesamt 7 LEDs sind, können wir hier noch die '7' definieren damit wir alle wieder ausmachen können bevor wir neu würfeln.
wuerfel_rot = {1: [84],
                2: [86, 89],
                3: [84, 86, 89],
                4: [86, 87, 83, 89],
                5: [83, 84, 86, 87, 89],
                6: [83, 85, 86, 87, 88, 89],
                7: [83, 84, 85, 86, 87, 88, 89]}

wuerfel_blau = {1: [8],
                2: [6, 10],
                3: [6, 8, 10],
                4: [4, 6, 7, 10],
                5: [4, 6, 7, 8, 10],
                6: [4, 5, 6, 7, 9, 10],
                7: [4, 5, 6, 7, 8, 9, 10]}

wuerfel_gelb= {1: [34],
                  2: [29,32],
                  3: [29,32,34],
                  4: [29,31,32,35],
                  5: [29,31,32,34,35],
                  6: [29,30,31,32,33,35]}

wuerfel_gruen= {1: [60],
                  2: [58,62],
                  3: [29,32,34],
                  4: [58,61,62,64],
                  5: [58,61,60,62,64],
                  6: [58,59,61,62,63,64]}

# Definieren von Startfeld der Figuren
START_ROT = 27
START_BLAU = 37
START_GELB = 7
START_GRUEN = 17

# ---------------------------------------------------------------------------------------------------------

# Ab hier definieren wir uns Funktionen. Das Ziel davon ist, dass wir nachher so das Programm logisch unterteilen können und es ungefähr das abbildet was der Programmablaufplan nachher beschreibt


def feld_gehen(standort, feldzahl):
      endfeld = standort + feldzahl  # neues Feld ist aktuelles Feld + die gewürfelte Zahl
      if endfeld > MAXIMALE_FELDZAHL:  # nötig hier, damit die Figur "rund" laufen kann
            endfeld = (endfeld - MAXIMALE_FELDZAHL)
      return endfeld  # Rückgabewert der Funktion ist die neue Position

def check_rauswerfen(neuer_standort):
      if neuer_standort is standort_rot: # rot wird rausgekegelt
            standort_rot = START_ROT
            pixels.set_pixel(spielfeld_leds.get(standort_rot), Adafruit_WS2801.RGB_to_color( 50,0,0 ))
            pixels.show()
            sleep(0.2) # warte kurz
      elif neuer_standort is standort_blau: # blau wird rausgekegelt
            standort_blau = START_BLAU
            pixels.set_pixel(spielfeld_leds.get(standort_blau), Adafruit_WS2801.RGB_to_color( 0,0,50 ))
            pixels.show()
            sleep(0.2) # warte kurz
      elif neuer_standort is standort_gelb: # gelb wird rausgekegelt
            standort_gelb = START_GELB
            pixels.set_pixel(spielfeld_leds.get(standort_gelb), Adafruit_WS2801.RGB_to_color( 50,50,0 ))
            pixels.show()
            sleep(0.2) # warte kurz
      elif neuer_standort is standort_gruen: # gruen wird rausgekegelt
            standort_gruen = START_GRUEN
            pixels.set_pixel(spielfeld_leds.get(standort_gruen), Adafruit_WS2801.RGB_to_color( 0,50,0 ))
            pixels.show()
            sleep(0.2) # warte kurz

def initialisiere_spielfeld(pixels):
      # for i in range(100):
      #      pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( 50,50,50 ))
      pixels.set_pixel(15, Adafruit_WS2801.RGB_to_color(50, 50, 0))
      pixels.set_pixel(16, Adafruit_WS2801.RGB_to_color(50, 50, 0))
      pixels.set_pixel(17, Adafruit_WS2801.RGB_to_color(50, 50, 0))
      pixels.set_pixel(18, Adafruit_WS2801.RGB_to_color(50, 50, 0))
      pixels.set_pixel(19, Adafruit_WS2801.RGB_to_color(50, 50, 0))
      pixels.set_pixel(13, Adafruit_WS2801.RGB_to_color(10, 10, 0))
      pixels.set_pixel(21, Adafruit_WS2801.RGB_to_color(10, 10, 0))
      pixels.set_pixel(22, Adafruit_WS2801.RGB_to_color(10, 10, 0))
      pixels.set_pixel(24, Adafruit_WS2801.RGB_to_color(10, 10, 0))
      pixels.set_pixel(38, Adafruit_WS2801.RGB_to_color(0, 50, 0))
      pixels.set_pixel(39, Adafruit_WS2801.RGB_to_color(0, 50, 0))
      pixels.set_pixel(40, Adafruit_WS2801.RGB_to_color(0, 50, 0))
      pixels.set_pixel(41, Adafruit_WS2801.RGB_to_color(0, 50, 0))
      pixels.set_pixel(42, Adafruit_WS2801.RGB_to_color(0, 50, 0))
      pixels.set_pixel(44, Adafruit_WS2801.RGB_to_color(0, 10, 0))
      pixels.set_pixel(45, Adafruit_WS2801.RGB_to_color(0, 10, 0))
      pixels.set_pixel(48, Adafruit_WS2801.RGB_to_color(0, 10, 0))
      pixels.set_pixel(49, Adafruit_WS2801.RGB_to_color(0, 10, 0))
      pixels.set_pixel(67, Adafruit_WS2801.RGB_to_color(50, 0, 0))
      pixels.set_pixel(68, Adafruit_WS2801.RGB_to_color(50, 0, 0))
      pixels.set_pixel(69, Adafruit_WS2801.RGB_to_color(50, 0, 0))
      pixels.set_pixel(70, Adafruit_WS2801.RGB_to_color(50, 0, 0))
      pixels.set_pixel(71, Adafruit_WS2801.RGB_to_color(50, 0, 0))
      pixels.set_pixel(56, Adafruit_WS2801.RGB_to_color(10, 0, 0))
      pixels.set_pixel(55, Adafruit_WS2801.RGB_to_color(10, 0, 0))
      pixels.set_pixel(51, Adafruit_WS2801.RGB_to_color(10, 0, 0))
      pixels.set_pixel(75, Adafruit_WS2801.RGB_to_color(10, 0, 0))
      pixels.set_pixel(92, Adafruit_WS2801.RGB_to_color(0, 0, 50))
      pixels.set_pixel(93, Adafruit_WS2801.RGB_to_color(0, 0, 50))
      pixels.set_pixel(94, Adafruit_WS2801.RGB_to_color(0, 0, 50))
      pixels.set_pixel(95, Adafruit_WS2801.RGB_to_color(0, 0, 50))
      pixels.set_pixel(96, Adafruit_WS2801.RGB_to_color(0, 0, 50))
      pixels.set_pixel(76, Adafruit_WS2801.RGB_to_color(0, 0, 10))
      pixels.set_pixel(77, Adafruit_WS2801.RGB_to_color(0, 0, 10))
      pixels.set_pixel(80, Adafruit_WS2801.RGB_to_color(0, 0, 10))
      pixels.set_pixel(81, Adafruit_WS2801.RGB_to_color(0, 0, 10))
      pixels.set_pixel(4, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(5, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(6, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(7, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(8, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(9, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(10, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(29, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(30, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(31, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(32, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(33, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(34, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(35, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(58, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(59, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(60, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(61, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(62, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(63, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(64, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(83, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(84, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(85, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(86, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(87, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(88, Adafruit_WS2801.RGB_to_color(0, 0, 0))
      pixels.set_pixel(89, Adafruit_WS2801.RGB_to_color(0, 0, 0))


# Hier beginnt das Hauptprogramm, das heißt wenn das Skript gestartet wird fängt es immer hier an
if __name__ == "__main__":
      # Zuerst weisen wir den Würfel-Knoepfen ihre Funktion zu
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(BUTTON_GPIO_ROT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.setup(BUTTON_GPIO_BLAU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.setup(BUTTON_GPIO_GELB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.setup(BUTTON_GPIO_GRUEN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      ist_rot_gedrueckt = False
      ist_blau_gedrueckt = False
      ist_gelb_gedrueckt = False
      ist_gruen_gedrueckt = False

      # Alle LEDs erstmal aus
      pixels.clear()
      pixels.show()

      # Alle LEDs so anmachen wie wir starten wollen
      initialisiere_spielfeld(pixels)
      pixels.show()

      # In diesen Variablen speichern wir den momentanen Standort der Spieler wenn es nur eine Figur gibt und benutzen die dann bei jedem Durchlauf
      standort_rot = START_ROT
      standort_blau = START_BLAU
      standort_gelb = START_GELB
      standort_gruen = START_GRUEN

      # Hier beginnt unsere Hauptschleife. Diese wird solange durchlaufen bis das Programm irgendwann abgebrochen wird. Im Grunde wird immer wieder geguckt ob irgendein Knopf gedrückt wurde und dann dementsprechend reagiert
      while True:
            if not GPIO.input(BUTTON_GPIO_ROT): # Der Knopf für den roten Spieler ist gedrückt
                  if not ist_rot_gedrueckt:
                        # Wir löschen das alte Feld
                        pixels.set_pixel(spielfeld_leds.get(standort_rot), Adafruit_WS2801.RGB_to_color( 0,0,0 )) # lösche altes Feld, Figur rückt
                        pixels.show()
                        sleep(0.2) # warte kurz

                        # Wir würfeln
                        zufallszahl = randint(1,6) # Erzeuge eine Würfelzufallszahl zwischen 1 und 6
                        neues_feld_fuer_spieler_rot = feld_gehen(standort_rot, zufallszahl) # Ermittele neues Spielfeld für die Figur
                        standort_rot = neues_feld_fuer_spieler_rot # speichere neues Spielfeld für nächsten Durchlauf
                        pixels.set_pixel(spielfeld_leds.get(standort_rot), Adafruit_WS2801.RGB_to_color( 50,0,0 )) # setze neues Spielfeld in Spielfarbe

                        check_rauswerfen(standort_rot)

                        # Setze jetzt die richtigen Farben am Würfel
                        # Mache die roten Würfel-LEDs aus
                        pixels.set_pixel(83, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(84, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(85, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(86, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(87, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(88, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(89, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.show()
                        sleep(0.2) # Warte kurz
                        for led in wuerfel_rot.get(zufallszahl,[]):
                              pixels.set_pixel(led, Adafruit_WS2801.RGB_to_color( 50,0,0 ))
                        pixels.show()
                        sleep(0.2)
                        ist_rot_gedrueckt = True
                  else:
                        ist_rot_gedrueckt = False
            elif not GPIO.input(BUTTON_GPIO_BLAU): # Der Knopf für den blauen Spieler ist gedrückt
                  if not ist_rot_gedrueckt:
                        # Wir würfeln
                        zufallszahl = randint(1,6) # Erzeuge eine Würfelzufallszahl zwischen 1 und 6
                        neues_feld_fuer_spieler_blau = feld_gehen(standort_blau, zufallszahl) # Ermittele neues Spielfeld für die Figur
                        standort_blau = neues_feld_fuer_spieler_blau # speichere neues Spielfeld für nächsten Durchlauf
                        print(standort_blau)
                        pixels.set_pixel(spielfeld_leds.get(standort_blau), Adafruit_WS2801.RGB_to_color( 0,0,50 )) # setze neues Spielfeld in Spielfarbe
                        sleep(0.2) # warte kurz

                        check_rauswerfen(standort_blau)

                        # Setze jetzt die richtigen Farben am Würfel
                        # Mache die blauen Würfel-LEDs aus
                        pixels.set_pixel(5, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(6, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(7, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(8, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(9, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(10, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(11, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.show()
                        sleep(0.2) # Warte kurz
                        for led in wuerfel_blau.get(zufallszahl,[]):
                              pixels.set_pixel(led, Adafruit_WS2801.RGB_to_color( 0,0,50 ))
                        pixels.show()
                        sleep(0.2)

                        ist_blau_gedrueckt = True
                  else:
                        ist_blau_gedrueckt = False
            if not GPIO.input(BUTTON_GPIO_GELB):
                  if not ist_gelb_gedrueckt:
                        print("GELB")
                        pixels.set_pixel(spielfeld_leds.get(standort_gelb), Adafruit_WS2801.RGB_to_color( 0,0,0 )) # lösche altes Feld, Figur rückt
                        pixels.show()
                        sleep(0.2)

                        zufallszahl = randint(1,6)
                        neues_feld_fuer_spieler_gelb = feld_gehen(standort_gelb, zufallszahl)
                        standort_gelb = neues_feld_fuer_spieler_gelb
                        pixels.set_pixel(spielfeld_leds.get(standort_gelb), Adafruit_WS2801.RGB_to_color( 50,50,0 ))

                        check_rauswerfen(standort_gelb)

                        pixels.set_pixel(29, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(30, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(31, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(32, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(33, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(34, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(35, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.show()
                        sleep(0.2)
                        for led in wuerfel_gelb.get(zufallszahl,[]):
                                    pixels.set_pixel(led, Adafruit_WS2801.RGB_to_color( 50,50,0 ))
                        pixels.show()
                        sleep(0.2)
                        ist_gelb_gedrueckt = True
                  else:
                        ist_gelb_gedrueckt = False

            if not GPIO.input(BUTTON_GPIO_GRUEN):
                  if not ist_gruen_gedrueckt:
                        print("GRUEN")

                        pixels.set_pixel(spielfeld_leds.get(standort_gruen), Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.show()
                        sleep(0.2)

                        zufallszahl = randint(1,6)
                        neues_feld_fuer_spieler_gruen = feld_gehen(standort_gruen, zufallszahl)
                        standort_gruen = neues_feld_fuer_spieler_gruen
                        pixels.set_pixel(spielfeld_leds.get(standort_gruen), Adafruit_WS2801.RGB_to_color( 0,50,0 ))

                        check_rauswerfen(standort_gruen)

                        pixels.set_pixel(58, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(59, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(60, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(61, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(62, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(63, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.set_pixel(64, Adafruit_WS2801.RGB_to_color( 0,0,0 ))
                        pixels.show()
                        sleep(0.2)
                        for led in wuerfel_gruen.get(zufallszahl,[]):
                                    pixels.set_pixel(led, Adafruit_WS2801.RGB_to_color( 0,50,0 ))
                        pixels.show()
                        sleep(0.2)
                        ist_gruen_gedrueckt = True
                  else:
                        ist_gruen_gedrueckt = False
            time.sleep(0.2)
