"""In der folgenden Anwendung werden mithilfe von 3 Klassen verschiedene RPG tätigkeiten ermöglicht. der Spieler kann sich seine Stats ansehen (Characterübersicht), Heiltränke trinken
und gegen verschiedene Gegner kämpfen. Testweise habe ich Waffen und Gegner in eigene Klassen gepackt

Die Bewaffnung wird bei der Erstellung der Charaktäre mit übergeben und in der Klassendefinition auf "weapon" zugewiesen, dadurch kann die Waffe dann quasi über self.weapon.weapon_damage
den Waffenschaden aus der Klasse Weaponry laden

falls hier irgendwas gänzlich Falsch gemacht wird bitte bescheidsagen :D - funktionieren tuts aufjedenfall soweit ich getestet hab, hab das ganze auch noch ein bisschen mit kommentaren versehen
"""
import random

class Weaponry:
    def __init__(self, weapon_name, weapon_damage):
        self.weapon_name = weapon_name
        self.weapon_damage = weapon_damage

class Enemy:
    def __init__(self, enemy_name, enemy_hp, enemy_bounty):
        self.enemy_name = enemy_name
        self.enemy_hp = enemy_hp
        self.enemy_bounty = enemy_bounty

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
        self.gold = gold

    #Anzeigen der Stats
    def display_stats(self):
        print(f"Dein Charakter {self.name} ist ein {self.character_class}.")
        print(f"Du hast {self.health_points}/{self.maxhp} Healthpoints")
        print(f"Du machst mit einem Hit mit der Waffe {self.weapon.weapon_name} {self.weapon.weapon_damage} Schaden")
        print(f"Du bist Level {self.character_level} mit {self.experience} Erfahrungspunkten")
        print(f"Du besitzt aktuell {self.gold} Gold und {self.potion_count} Healthpotions")

    #Funktionsdefinitioon um einen Healpot zu benutzen
    def use_potion(self):
        if self.potion_count > 0:    #überprüfung ob man noch Pots hat
            if self.health_points + self.potion_power > self.maxhp:
                over_heal = (self.health_points + self.potion_power) - self.maxhp                #Arbeitsvariable für den Overheal
                self.health_points = self.maxhp
                self.potion_count -= 1
                print(f"Du hast ein Healthpotion konsumiert. Deine Healthpoints betragen jetzt {self.health_points}/{self.maxhp}. Dabei hast du {over_heal}HP verschwendet")
                print(f"{self.potion_count} Healthpotions verbleibend")
            else:
                self.health_points += self.potion_power
                self.potion_count -= 1
                print(f"Du hast ein Healthpotion benutzt. Deine Healthpoints betragen jetzt {self.health_points}/{self.maxhp}.")
                print(f"{self.potion_count} Healthpotions verbleibend")
        else:
            print("Du kannst dich nicht heilen da du keine Healthpotions mehr hast.")

    #Funktionsdefinition für die Kampffunktion
    def fight(self, enemy_id):
        print(f"Du beginnst den Kampf gegen einen {enemy_id.enemy_name}")
        while True:
            attack_y_n = input("Möchtest du Angreifen? (J/N)")
            if attack_y_n.upper() == "J":
                enemy_id.enemy_hp -= self.weapon.weapon_damage                                                                    #Mein verursachter Schaden wird von den HP des Gegners abgezogen
                print(f"Du hast den {enemy_id.enemy_name} angegriffen und {self.weapon.weapon_damage} Schaden verursacht.")
                print(f"Der {enemy_id.enemy_name} hat nun {enemy_id.enemy_hp}HP")
                if enemy_id.enemy_hp <= 0:
                    print(f"Du hast den {enemy_id.enemy_name} besiegt.")
                    self.gold += enemy_id.enemy_bounty
                    print(f"Du hebst {enemy_id.enemy_bounty} Gold auf")
                    break
            elif attack_y_n.upper() == "N":                                                                         #Kampf wird abgebrochen,
                print(f"Du hast den Kampf abgebrochen, der {enemy_id.enemy_name} ist mit {enemy_id.enemy_hp}HP entkommen")
                break
            else:
                continue                                    #falls etwas anderes als j oder n eingegeben wird, wird erneut nach der eingabe gefragt


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