class Weaponry:
    def __init__(self, weapon_name, weapon_damage):
        self.weapon_name = weapon_name
        self.weapon_damage = weapon_damage

class Enemy:
    def __init__(self, enemy_name, enemy_hp, enemy_bounty):
        self.enemy_name = enemy_name
        self.enemy_hp = enemy_hp
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

    def buy_potion(self):
        print(f"Du hast aktuell {self.gold} Gold.")
        buy_amount = int(input("Wieviele Healthpotions möchtest du kaufen? Preis: 5 Gold pro Healthpotion: "))
        if buy_amount > 0:
            if self.gold > (buy_amount * 5):
                self.potion_count += buy_amount
                self.gold -= buy_amount * 5
                print(f"Du hast {buy_amount} Healthpotions gekauft und dafür {buy_amount * 5} Gold ausgegeben.")
            else:
                print(f"Das kannst du dir nicht leisten!")
        else:
            print("Fehlerhafte eingabe, bitte Eingabe überprüfen!")