class Equipment:
    
    def __init__(self, name, defense, attack, type):
        self.name = name
        self.defense = defense
        self.attack = attack
        self.type = type


class Sword(Equipment):
    def __init__(self):
        super().__init__("Rusty Sword", 0, 5, "weapon")

class IronSword(Equipment):
    def __init__(self):
        super().__init__("Iron Sword", 0, 10, "weapon")

class SteelSword(Equipment):
    def __init__(self):
        super().__init__("Steel Sword", 0, 20, "weapon")

class Shield(Equipment):
    def __init__(self):
        super().__init__("Worn Shield", 5, 0, "armor")

class IronShield(Equipment):
    def __init__(self):
        super().__init__("Iron Shield", 10, 0, "armor")

class SteelShield(Equipment):
    def __init__(self):
        super().__init__("Steel Shield", 20, 0, "armor")