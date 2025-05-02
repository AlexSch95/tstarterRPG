import random
import sqlite3

"""Datenbankfunktionen um
Charaktäre zu laden
Gegner zu laden und in eine Liste zu zu schreiben
Speichern des Fortschritts"""
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
        fetched_weapon = cursor.fetchone()        #fetchen des DB Datensatzes und schreiben als tupel in eine variable

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
            WHERE name = '{character.name}';""")      # Aktuelle Werte vom Speicher in die Datenbank schreiben
        conn.commit()
        conn.close()
        return f"Automatisches speichern...\nFortschritt erfolgreich gespeichert!"
    except:
        return f"Fehler beim Speichern"

def load_enemies():
    try:
        enemy_list = []
        conn = sqlite3.connect('rpg.db')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT enemy_name, enemy_hp, enemy_maxhp, enemy_damage, enemy_bounty FROM enemies""")
        fetched_enemies = cursor.fetchall()
        for row in fetched_enemies:
            enemy_name, enemy_hp, enemy_maxhp, enemy_damage, enemy_bounty = row
            enemy_obj_creator = Enemy(enemy_name, enemy_hp, enemy_maxhp, enemy_damage, enemy_bounty)
            enemy_list.append(enemy_obj_creator)  #für die Gegnerliste zur Randomauswahl der Gegner

        conn.close()
        return enemy_list  #schickt die Liste zurück damit sie im Hauptprogramm weiter verwendet werden kann
    except:
        print("Fehler beim Laden der Gegner")


"""Anfang der Klassendefinitionen für
Waffen
Charaktäre
Gegner"""
class Weaponry:
    def __init__(self, weapon_name, weapon_damage):
        self.weapon_name = weapon_name
        self.weapon_damage = weapon_damage

class Enemy:
    def __init__(self, enemy_name, enemy_hp, enemy_maxhp, enemy_damage, enemy_bounty):
        self.enemy_name = enemy_name
        self.enemy_hp = enemy_hp
        self.enemy_maxhp = enemy_maxhp
        self.enemy_damage = enemy_damage
        self.enemy_bounty = enemy_bounty        #der Gold-Wert eines Gegners, hier wird gespeichert wieviel Gold man nach besiegen eines Gegners erhält

class RpgCharacter:
    def __init__(self, name, character_class, weapon, health_points, potion_count, character_level, experience, gold=0):
        self.maxhp = 100                                        #Max HP
        self.potion_power = 10                                  #wieviel heilt ein Trank
        self.potion_count = potion_count                        #wieviele Pots
        self.name = name                                        #charactername
        self.character_class = character_class                  #characterklasse
        self.weapon = weapon                                    #Waffe
        self.health_points = health_points                      #aktuelle HP
        self.character_level = character_level                  #aktuelles Level
        self.experience = experience                            #aktuelle EXP
        self.gold = gold                                        #Kontostand des Charakters

    #Anzeigen der Stats
    def display_stats(self):
        print(f"Charaktername: {self.name}")
        print(f"Klasse: {self.character_class}")
        print(f"HP: {self.health_points}/{self.maxhp}")
        print(f"Waffe: {self.weapon.weapon_name} ({self.weapon.weapon_damage} Schaden)")
        print(f"Healthpotions: {self.potion_count} Stück")
        print(f"Characterlevel: {self.character_level} ({self.experience}/100 EXP)")
        print(f"Gold: {self.gold}")
        print()
        while True:
            return_to_menu = input("Möchtest du zum Hauptmenü zurückkehren? (J/N): ")
            if return_to_menu.upper() == "J":
                break
            else:
                continue
        print()

    #Funktionsdefinitioon um einen Healpot zu benutzen
    def use_potion(self):
        if self.potion_count > 0:    #überprüfung ob man noch Pots hat
            if self.health_points + self.potion_power > self.maxhp:
                over_heal = (self.health_points + self.potion_power) - self.maxhp                #Arbeitsvariable für den Overheal
                self.health_points = self.maxhp
                self.potion_count -= 1
                print(f"Du hast ein Healthpotion konsumiert. Deine Healthpoints betragen jetzt {self.health_points}/{self.maxhp}. Dabei hast du {over_heal}HP verschwendet")
                print(f"{self.potion_count} Healthpotions verbleibend")
                print()
            else:
                self.health_points += self.potion_power
                self.potion_count -= 1
                print(f"Du hast ein Healthpotion benutzt. Deine Healthpoints betragen jetzt {self.health_points}/{self.maxhp}.")
                print(f"{self.potion_count} Healthpotions verbleibend")
                print()
        else:
            print("Du kannst dich nicht heilen da du keine Healthpotions mehr hast.")
            while True:
                potion_shop_shortcut = input("Möchtest du zum Shop wechseln? (J/N)")
                if potion_shop_shortcut.upper() == "J":
                    self.buy_potion()
                    break
                elif potion_shop_shortcut.upper() == "N":
                    print("Kehre zurück zum Hauptmenü")
                    break
                else:
                    continue

    #Funktionsdefinition für die Kampffunktion
    def random_fight(self, enemy_id):
        print(f"Du beginnst den Kampf gegen einen {enemy_id.enemy_name}")
        while True:
            attack_y_n = input("Möchtest du Angreifen (J/N)? ")
            if attack_y_n.upper() == "J":
                enemy_id.enemy_hp -= self.weapon.weapon_damage                                                                    #Mein verursachter Schaden wird von den HP des Gegners abgezogen
                print(f"Du hast den {enemy_id.enemy_name} angegriffen und {self.weapon.weapon_damage} Schaden verursacht.")
                print(f"Der {enemy_id.enemy_name} hat nun {enemy_id.enemy_hp}HP")
                print()
                if enemy_id.enemy_hp <= 0:
                    print(f"Du hast den {enemy_id.enemy_name} besiegt.")
                    enemy_id.enemy_hp = enemy_id.enemy_maxhp #Gegner HP wird wieder auf Max gesetzt
                    self.gold += enemy_id.enemy_bounty
                    print(f"Du hebst {enemy_id.enemy_bounty} Gold auf")
                    print()
                    break
                print(f"Dein Gegner greift an und verursacht {enemy_id.enemy_damage} Schaden")
                self.health_points -= enemy_id.enemy_damage
                print(f"Deine Lebenspunkte sinken auf {self.health_points}/{self.maxhp} Healthpoints")
                if self.health_points <= 0:
                    print(f"Du bist gestorben. Du kehrst zum Lager zurück")
                    print()
                    break
                if self.health_points <= 25:
                    while True:
                        heal_y_n = input("Deine HP sind gering, Möchtest du dich Heilen vor dem nächsten Angriff? (J/N)")
                        if heal_y_n.upper() == "J":
                            self.use_potion()
                            break
                        elif heal_y_n.upper() == "N":
                            print("Du entscheidest dich keinen Heiltrank zu trinken, kehre zum Kampf zurück")
                            break
                        else:
                            continue
            elif attack_y_n.upper() == "N":                                #Kampf wird abgebrochen,
                print(f"Du hast den Kampf abgebrochen, der {enemy_id.enemy_name} ist mit {enemy_id.enemy_hp}HP entkommen")
                print()
                break
            else:
                continue                                    #falls etwas anderes als j oder n eingegeben wird, wird erneut nach der eingabe gefragt

    def wave_defense(self, wave_count, enemy_list):
        waves = wave_count
        print(waves)
        bonus_gold = wave_count * 5  # 5 Gold Bonus pro Welle
        while wave_count > 0 and self.health_points > 0:
            self.random_fight(random.choice(enemy_list)) #ruft den Kampf auf und wählt für jeden funktionsaufruf einen random gegner aus
            wave_count -= 1  #zähler -1 weil eine welle besiegt wurde
            if self.health_points <= 0:
                return "Gestorben"

            if wave_count == 0:
                print(f"Du hast alle {waves} Wellen besiegt, Glückwunsch!")
                print(f"Als Belohnung für deinen Sieg über alle Wellen erhältst du {bonus_gold} zusätzliches Gold")
                self.gold += bonus_gold  ## Bonus Gold wird dem Charakter hinzugefügt
                print(f"Du besitzt nun {self.gold} Gold")
                return "Gewonnen"
        else:
            return 0




    def buy_potion(self):
            print(f"Du hast aktuell {self.gold} Gold.")             #ausgabe vom Gold
            buy_amount = int(input("Wieviele Healthpotions möchtest du kaufen? Preis: 5 Gold pro Healthpotion: "))
            if buy_amount > 0:                  #man darf nicht weniger als 0 kaufen
                if self.gold > (buy_amount * 5):        # gold darf nicht weniger sein als die anzahl der pots * 5 (preis für einen pot)
                    self.potion_count += buy_amount     #pots im besitz + gekaufte menge
                    self.gold -= buy_amount * 5         #gold im besitz - preis der gekauften pots
                    print(f"Du hast {buy_amount} Healthpotions gekauft und dafür {buy_amount * 5} Gold ausgegeben.")
                    print()
                else:
                    print(f"Das kannst du dir nicht leisten!")
                    print()    #wenn das gold nicht ausreicht
            else:
                print("Fehlerhafte eingabe, bitte Eingabe überprüfen!")     #bei einer ungültigen eingabe zb. abcdefg
                print()