"""In der folgenden Anwendung werden mithilfe von 3 Klassen verschiedene RPG tätigkeiten ermöglicht. der Spieler kann sich seine Stats ansehen (Characterübersicht), Heiltränke trinken
und gegen verschiedene Gegner kämpfen. Testweise habe ich Waffen und Gegner in eigene Klassen gepackt

Die Bewaffnung wird bei der Erstellung der Charaktäre mit übergeben und in der Klassendefinition auf "weapon" zugewiesen, dadurch kann die Waffe dann quasi über self.weapon.weapon_damage
den Waffenschaden aus der Klasse Weaponry laden

falls hier irgendwas gänzlich Falsch gemacht wird bitte bescheidsagen :D - funktionieren tuts aufjedenfall soweit ich getestet hab, hab das ganze auch noch ein bisschen mit kommentaren versehen
"""
import random #random wird importiert um die Zufallsauswahl eines Gegners zu ermöglichen
from classes import *

#Waffen
wand = Weaponry("Zauberstab", 5)
comp_bow = Weaponry("Kompositbogen", 6)

#Player Characters
alex = RpgCharacter("Alex", "Magier", wand, 70, 1, 10, 95, 500) #Objekt "Alex" wird als Character erstellt
helen = RpgCharacter("Helen", "Bogenschützin", comp_bow, 50, 1, 15, 70, 3)

#Gegner
goblin = Enemy("Goblin", 25, 10)
wolf = Enemy("Wolf", 18, 7)

#Liste der Gegner für nutzung von zufallsgegnerwahl
enemy_list = [goblin, wolf]

#Funktionsaufrufe mit Menü
while True:
    selected_character = input("Character auswählen (aktuell nur Alex oder Helen):")
    if selected_character.lower() == "helen" or "alex":
        print(f"Willkommen {selected_character.title()} im Techstarter RPG ")
        break
    else:
        continue


while True:
    print("Was möchtest du tun?")
    print("1. Characterstats ansehen")
    print("2. Healthpotion benutzen")
    print("3. Kämpfen")
    print("4. Tränke kaufen")
    print("5. Exit")
    user_input = input("Bitte Auswahl eingeben:")

    if user_input == "1":
        if selected_character.lower() == "helen":
            helen.display_stats()
        elif selected_character.lower() == "alex":
            alex.display_stats()

    elif user_input == "2":
        if selected_character.lower() == "helen":
            helen.use_potion()
        if selected_character.lower() == "alex":
            alex.use_potion()

    elif user_input == "3":
        if selected_character.lower() == "helen":
            helen.fight((random.choice(enemy_list)))
        if selected_character.lower() == "alex":
            alex.fight((random.choice(enemy_list)))

    elif user_input == "4":
        if selected_character.lower() == "helen":
            print(f"Du hast aktuell {helen.gold} Gold.")
            buy_amount = int(input("Wieviele Healthpotions möchtest du kaufen? Preis: 5 Gold pro Healthpotion: "))
            if buy_amount > 0:
                if helen.gold > (buy_amount * 5):
                    helen.potion_count += buy_amount
                    helen.gold -= buy_amount * 5
                    print(f"Du hast {buy_amount} Healthpotions gekauft und dafür {buy_amount * 5} Gold ausgegeben.")
                else:
                    print(f"Das kannst du dir nicht leisten!")
            else:
                    print("Fehlerhafte eingabe, bitte eingabe überprüfen!")
        if selected_character.lower() == "alex":
            print(f"Du hast aktuell {alex.gold} Gold.")
            buy_amount = int(input("Wieviele Healthpotions möchtest du kaufen? Preis: 5 Gold pro Healthpotion: "))
            if buy_amount > 0:
                if alex.gold > (buy_amount * 5):
                    alex.potion_count += buy_amount
                    alex.gold -= buy_amount * 5
                    print(f"Du hast {buy_amount} Healthpotions gekauft und dafür {buy_amount * 5} Gold ausgegeben.")
                else:
                    print(f"Das kannst du dir nicht leisten!")
            else:
                print("Fehlerhafte eingabe, bitte eingabe überprüfen!")


    elif user_input == "5":
        break

    else:
        continue