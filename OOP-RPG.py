"""In der folgenden Anwendung werden mithilfe von 3 Klassen verschiedene RPG tätigkeiten ermöglicht. der Spieler kann sich seine Stats ansehen (Characterübersicht), Heiltränke trinken
und gegen verschiedene Gegner kämpfen. Testweise habe ich Waffen und Gegner in eigene Klassen gepackt

Die Bewaffnung wird bei der Erstellung der Charaktäre mit übergeben und in der Klassendefinition auf "weapon" zugewiesen, dadurch kann die Waffe dann quasi über self.weapon.weapon_damage
den Waffenschaden aus der Klasse Weaponry laden

falls hier irgendwas gänzlich Falsch gemacht wird bitte bescheidsagen :D - funktionieren tuts aufjedenfall soweit ich getestet hab, hab das ganze auch noch ein bisschen mit kommentaren versehen
"""
import random #random wird importiert um die Zufallsauswahl eines Gegners zu ermöglichen

from classes import *

#Funktionsaufrufe mit Menü
while True:
    user_char_choice = input("Charakter auswählen (Gundolf, Duplolas oder Schimmli): ").title()
    character = load_char(user_char_choice)    #funktionsaufruf zum laden aus der DB
    if isinstance(character, RpgCharacter) == True:
        print(f"Willkommen {character.name} - {character.character_class}")
          ### erstellen der leeren Liste die beim Login durch den funktionsaufruf beladen wird
        enemy_list = load_enemies()  #### sprung in die funktion load_enemies
        break
    elif character == f"Falscher Charactername... Bitte erneut versuchen.":
        print(character)
        continue



while True:
    if character.health_points <= 0:
        character.health_points = 1
        print("Willkommen zurück im Lager, du wurdest wiederbelebt und deine Lebenspunkte wurden auf 1 gesetzt.")
    print()
    print(f"{character.name}, was möchtest du tun?")
    print("1. Characterstats ansehen")
    print("2. Healthpotion benutzen")
    print("3. Zufälligen Gegner bekämpfen")
    print("4. Wave-Defense")
    print("5. Tränke kaufen")
    print("6. Exit (Speichert automatisch)")
    user_input = input("Bitte Auswahl eingeben: ")
    print()

    if user_input == "1":
        character.display_stats()

    elif user_input == "2":
        character.use_potion()
        saving = save_char(character)
        print(saving)

    elif user_input == "3":
        character.random_fight(random.choice(enemy_list))
        saving = save_char(character)
        print(saving)

    elif user_input == "4":
        while True:
            print("Wieviele Wellen möchtest du bekämpfen? Abbrechen bringt dich zurück zum Menü")
            wave_count = input("Wellen: ")
            if wave_count.isnumeric() == True:
                wave_count = int(wave_count)
                success_lose = character.wave_defense(wave_count, enemy_list)
                saving = save_char(character)
                print(saving)
                if success_lose == "Gestorben":
                    break
                else:
                    continue
            elif wave_count.lower() == "abbrechen":
                break
            else:
                continue

    elif user_input == "5":
        character.buy_potion()
        saving = save_char(character)
        print(saving)

    elif user_input == "6":
        saving = save_char(character)
        print(saving)
        break

    else:
        continue