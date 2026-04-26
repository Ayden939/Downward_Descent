"""
Defines main player character and actions.
Will be expanded to help manage character generations and inventory
"""


import random

class  Character:


    def __init__(self, name, generation, gold = 0, weapon = None, armor = None):
        self.name = name
        self.floor = 1
        self.health = 100
        self.strength = 20
        self.generation = generation
        self.gold = gold
        self.weapon = weapon
        self.armor = armor
    

    def incoming_damage(self, damage):

        if(self.armor):
            if(damage - self.armor.defense > 0):
                damage = damage - self.armor.defense
            else:
                damage = 0

        #print(f"{self.name} takes {damage} damage!")
        self.health = self.health - damage
        if self.health < 0:
            self.health = 0

        return damage

    def attack(self, target):

        if(self.weapon):
            weapon_attack = self.weapon.attack
        else:
            weapon_attack = 0

        strike = self.strength + random.randint(1,5) + weapon_attack
        print(f"{self.name} attacks {target.name} for {strike} damage!")
        target.incoming_damage(strike)
        return strike

    def heal(self):
        if self.health < 100:
            amount = random.choice([5,10,15,20])
            if self.health + amount < 100:
                self.health = self.health + amount
                #print(f"{self.name} gains {amount} health!")
                damage = random.choice([0, 10, 15])
                damage = self.incoming_damage(damage)
                return amount, damage
            else:
                difference = 100 - self.health
                self.health = 100
                #print(f"{self.name} gains {difference} health!")
                damage = random.choice([0, 10, 15])
                damage = self.incoming_damage(damage)
                return difference, damage
        else:
            return None


    def equip(self, equipment):
        if(equipment.type == "weapon"):
            self.weapon = equipment
        else:
            self.armor = equipment
