"""In der folgenden Anwendung werden mithilfe von 3 Klassen verschiedene RPG tätigkeiten ermöglicht. der Spieler kann sich seine Stats ansehen (Characterübersicht), Heiltränke trinken
und gegen verschiedene Gegner kämpfen. Testweise habe ich Waffen und Gegner in eigene Klassen gepackt

Die Bewaffnung wird bei der Erstellung der Charaktäre mit übergeben und in der Klassendefinition auf "weapon" zugewiesen, dadurch kann die Waffe dann quasi über self.weapon.weapon_damage
den Waffenschaden aus der Klasse Weaponry laden

falls hier irgendwas gänzlich Falsch gemacht wird bitte bescheidsagen :D - funktionieren tuts aufjedenfall soweit ich getestet hab, hab das ganze auch noch ein bisschen mit kommentaren versehen
"""
import random #random wird importiert um die Zufallsauswahl eines Gegners zu ermöglichen
from classes import *

#Waffen
fists = Weaponry("Fäuste", 1)
wand = Weaponry("Zauberstab", 5)
comp_bow = Weaponry("Kompositbogen", 6)

#Player Characters
dummy = RpgCharacter("Dummy", "Dummy", fists, 100, 0, 1, 0, 0) #Dummy Character
alex = RpgCharacter("Alex", "Magier", wand, 70, 1, 10, 95, 500) #Objekt "Alex" wird als Character erstellt
helen = RpgCharacter("Helen", "Bogenschützin", comp_bow, 50, 1, 15, 70, 3)

#Gegner
goblin = Enemy("Goblin", 25, 10)
wolf = Enemy("Wolf", 18, 7)

#Liste der Gegner für nutzung von zufallsgegnerwahl
enemy_list = [goblin, wolf]
playable_characters = {"alex": alex,
                       "helen": helen}

#Funktionsaufrufe mit Menü
while True:
    selected_character = dummy
    user_char_choice = input("Character auswählen (aktuell nur Alex oder Helen):").lower()
    if user_char_choice.lower() in playable_characters:
        selected_character = playable_characters[user_char_choice]
        print(f"Willkommen {user_char_choice.title()} im Techstarter RPG")
        break
    else:
        continue


while True:
    print(f"{selected_character.name}, was möchtest du tun?")
    print("1. Characterstats ansehen")
    print("2. Healthpotion benutzen")
    print("3. Kämpfen")
    print("4. Tränke kaufen")
    print("5. Exit")
    user_input = input("Bitte Auswahl eingeben: ")

    if user_input == "1":
        selected_character.display_stats()

    elif user_input == "2":
        selected_character.use_potion()

    elif user_input == "3":
        selected_character.fight(random.choice(enemy_list))

    elif user_input == "4":
        selected_character.buy_potion()

    elif user_input == "5":
        break

    else:
        continue