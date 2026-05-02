"""
Defines all enemy types and behavior.
Enemies ineherit from the parent enemy class.
"""


import random

class Enemy:
    def __init__(self, name, strength, health, rarity):
        self.name = name
        self.strength = strength
        self.health = health
        self.rarity = rarity

    def attack(self, target):
        strike = self.strength + random.randint(5,20)
        damage = target.incoming_damage(strike)
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        return damage

    
    def incoming_damage(self, damage):
        print(f"{self.name} takes {damage} damage!")
        self.health = self.health - damage
        if(self.health < 0):
            self.health = 0
    
    

class Skeleton(Enemy):

    def __init__(self):
        super().__init__("Skeleton", 15, 100, "common")


class Goblin(Enemy):

    def __init__(self):
        super().__init__("Goblin", 20, 90, "common")


class Orc(Enemy):

    def __init__(self):
        super().__init__("Orc", 30, 100, "rare")

class Phantom(Enemy):

    def __init__(self):
        super().__init__("Phantom", 5, 150, "rare")

    def attack(self, target):
        strike = self.strength + random.randint(5,20)
        print(f"{self.name} attacks {target.name} for {strike} damage!")
        target.incoming_damage(strike)

        print(f"{self.name} grows stronger...")
        self.strength += 2

class King(Enemy):
    def __init__(self):
        super().__init__("Monster King", 35, 400, "unique")
    
    def attack(self, target):
        strike = self.strength + random.randint(0,15)
        print(f"{self.name} attacks {target.name} for {strike} damage!")
        target.incoming_damage(strike)

        print(f"{self.name} grows furious...")
        self.strength += 5
