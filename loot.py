import random
from equipment import Sword, IronSword, SteelSword, Shield, IronShield, SteelShield

def loot_drop(rarity, hero, floor):
    
    possible_drops = []
    weights = []

    if floor <= 4:
        weapon = Sword()
        armor = Shield()
    elif floor <= 7:
        weapon = IronSword()
        armor = IronShield()
    else:
        weapon = SteelSword()
        armor = SteelShield()

    if hero.weapon is None or weapon.attack > hero.weapon.attack:
        possible_drops.append(weapon)
        weights.append(.2)

    if hero.armor is None or armor.defense > hero.armor.defense:
        possible_drops.append(armor)
        weights.append(.2)

    possible_drops.append(None)
    weights.append(.6)

    choice = random.choices(possible_drops, weights = weights, k = 1)[0]

    return choice