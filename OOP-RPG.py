"""In der folgenden Anwendung werden mithilfe von 3 Klassen verschiedene RPG tätigkeiten ermöglicht. der Spieler kann sich seine Stats ansehen (Characterübersicht), Heiltränke trinken
und gegen verschiedene Gegner kämpfen. Testweise habe ich Waffen und Gegner in eigene Klassen gepackt

Die Bewaffnung wird bei der Erstellung der Charaktäre mit übergeben und in der Klassendefinition auf "weapon" zugewiesen, dadurch kann die Waffe dann quasi über self.weapon.weapon_damage
den Waffenschaden aus der Klasse Weaponry laden

falls hier irgendwas gänzlich Falsch gemacht wird bitte bescheidsagen :D - funktionieren tuts aufjedenfall soweit ich getestet hab, hab das ganze auch noch ein bisschen mit kommentaren versehen
"""
import random #random wird importiert um die Zufallsauswahl eines Gegners zu ermöglichen
import sqlite3
from classes import *


def load_char(user_char_choice):
    try:
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect('rpg.db')
        cursor = conn.cursor()
        # Laden aus der SQLite DB 'rpg.db'
        cursor.execute(f"""SELECT username, name, character_class, weapon, health_points, potion_count, 
        character_level, experience, gold FROM characters WHERE username = '{user_char_choice}'""")     #Datensatz des gewählten Users über SQL abfragen
        fetched_character = cursor.fetchone()               #fetchen des DB Datensatzes und schreiben als tupel in eine variable
        username, name, character_class, weapon, health_points, potion_count, character_level, experience, gold = fetched_character  # tupel in variablen laden
        cursor.execute(f"""SELECT weapon_name, weapon_damage FROM weapons WHERE ID = '{weapon}'""")     #Datensatz der Waffe des gewählten Characters
        fetched_weapon = cursor.fetchone()                  #fetchen des DB Datensatzes und schreiben als tupel in eine variable
        #Schliessen der Verbindung zur DB
        conn.close()

        weapon_name, weapon_damage = fetched_weapon         #tupel in variablen laden
        weapon = Weaponry(weapon_name, weapon_damage)       #objektinstanzierung der Waffe
        character = RpgCharacter(name, character_class, weapon, health_points, potion_count, character_level, experience, gold) # objektinstanzierung des Characters

        return character
    except:
        return f"Falscher Charactername... Bitte erneut versuchen."

def save_char(character):
    try:
        conn = sqlite3.connect('rpg.db')
        cursor = conn.cursor()
        cursor.execute(f"""UPDATE characters
            SET health_points = {character.health_points},
            potion_count = {character.potion_count},
            character_level = {character.character_level},
            experience = {character.experience},
            gold = {character.gold}
            WHERE name = '{character.name}';""")
        conn.commit()
        conn.close()
        return f"Automatisches speichern...\nFortschritt erfolgreich gespeichert!"
    except:
        return f"Fehler beim Speichern"


#Waffen
#fists = Weaponry("Fäuste", 1)
#wand = Weaponry("Zauberstab", 5)
#comp_bow = Weaponry("Kompositbogen", 6)

#Objektinstanzierung Spielercharaktäre
#dummy = RpgCharacter("Dummy", "Dummy", fists, 100, 0, 1, 0, 0) #Dummy Character
#mage = RpgCharacter("Gandalf", "Zauberer", wand, 1, 0, 1, 0, 100)
#ranger = RpgCharacter("Legolas", "Bogenschütze", comp_bow, 100, 0, 1, 0, 100)
#gollum = RpgCharacter("Smeagol", "Hobbit", fists, 100, 1, 0,1,100 )

#Objektinstanzierung Gegner
goblin = Enemy("Goblin", 25, 25, 3, 10)
wolf = Enemy("Wolf", 18, 18, 5, 7)
rat = Enemy("Ratte", 10, 10, 3, 2)
troll = Enemy("Bergtroll", 40, 40, 4, 15)
bats = Enemy("Schwarm Fledermäuse", 20, 20, 2, 12)
orc = Enemy("Ork", 25, 25, 8, 14)


"""Listen der bekämpfbaren Gegner 
(diese werden automatisch aus dem
speicher heraus erstellt und deren Speicheradressen werden als Werte in eine Liste gepackt"""

enemy_list = []

for enemy in dir():
    if isinstance(locals()[enemy], Enemy):
        enemy = eval(enemy)
        enemy_list.append(enemy)

"""Ähnlich wie bei der Liste der Gegner werden hier alle Spielercharaktäre in ein Dictionary geladen
im Dictionary wird die Objekteigenschaft "name" als Schlüssel verwendet und die Adresse im Speicher als Key
um nachfolgend dann zu überprüfen ob der gewählte charakter ein objekt der klasse RpgCharacters ist"""


#Funktionsaufrufe mit Menü
while True:
    user_char_choice = input("Charakter auswählen (Gundolf, Duplolas oder Schimmli): ").title()
    character = load_char(user_char_choice)
    if isinstance(character, RpgCharacter) == True:
        print(f"Willkommen {character.name}")
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