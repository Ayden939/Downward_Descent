"""
label = tk.label(root, text = 'Some Text')
label.pack

Label will display text/images
root is where tkinter places it
.pack(), .grid(), .place() actually places it

"""

import tkinter as tk
from character import Character
from enemy import Skeleton, Goblin, Orc, Phantom, King
from database import log
import database
import random
from equipment import Sword, Shield
from loot import loot_drop

# Game objects
hero = Character("Lady Samantha Rostnovak", 1)
floor = 1
enemy = random.choice([Skeleton(), Goblin()])

# Tkinter GUI setup
root = tk.Tk()      # This creates the window, and root.title just applies the title to it
root.title("Legacy Game")
root.geometry("500x300")


# Info Labels
floor_label = tk.Label(root, text=f"Floor: {floor}")
floor_label.pack(padx = 1, pady = 1)

hero_label = tk.Label(root, text=f"{hero.name} HP: {hero.health}")
hero_label.pack(padx = 1, pady = 1)

enemy_label = tk.Label(root, text=f"{enemy.name} Enemy HP: {enemy.health}")
enemy_label.pack(padx = 1, pady = 1)

output_label = tk.Label(root, text = "")
output_label.pack(expand = True, fill = "both", padx = 1, pady = 1)


output_label.config(text = "The towns greatest hero, Lady Samantha Rostnovak, enters the dungeon. Little is known about the dungeon except\n"
"that it has been around long before any person had settled there. Many have dove in to explore the depths, but most have fallen,\n"
"and none have gone very far. There are a hundreed floors, and a long adventure for our courageous hero.")

def attack():
    damage = hero.attack(enemy)
    if(enemy.health <= 0):
        update_labels("Enemy defeated!")
        item = loot_drop(enemy.rarity, hero)
        log("Lady Samantha Rostnovak", hero.generation, "Killed Enemy", 0, floor)
        if item:
            disable_buttons()
            equip_items(item, enemy)
        else:
            new_floor()
        return
        
    enemy.attack(hero)
    update_labels(f"{hero.name} attacks {enemy.name} for {damage} damage!")

    if(hero.health <= 0):
        update_labels("Defeated")
        disable_buttons()
        return

    
def heal():
    result = hero.heal()
    if result is None:
        update_labels(f"Health is full! Nothing happens.")
        return
    healed, damage = result
    if(hero.health > 0):
        update_labels(f"Hero gained {healed} health and was attacked for {damage} damage!\n")
    else:
        update_labels(f"Hero gained {healed} but took {damage} damage and was defeated!")
        disable_buttons()
        return

def retreat():
    update_labels(f"{hero.name} has left the dungeon")
    disable_buttons()
    return 

def update_labels(text):
    hero_label.config(text = f"{hero.name} HP: {hero.health}")
    enemy_label.config(text = f"{enemy.name} HP: {enemy.health}")
    output_label.config(text = text)

def disable_buttons():
    attack_btn.config(state = "disabled")
    heal_btn.config(state = "disabled")
    retreat_btn.config(state = "disabled")

def new_floor():
    global floor, enemy
    floor = floor + 1
    floor_label.config(text = f"Floor: {floor}")
    if(floor <= 4):
        pool = [Skeleton(), Goblin()]
    elif(floor >= 5 and floor <= 7):
        pool = [Skeleton(), Goblin(), Orc()]
    elif(floor >= 8 and floor <= 9):
        pool = [Orc(), Phantom()]
    elif(floor == 10):
        pool = [King()]
    else:
        disable_buttons()
        update_labels("You cleared the dungeon!")
        return
    
    enemy = random.choice(pool)
    update_labels(f"A {enemy.name} appears!")

def equip_items(equipment, enemy):
    attack_btn.pack_forget()
    heal_btn.pack_forget()
    retreat_btn.pack_forget()

    output_label.config(text = f"{enemy.name} has dropped {equipment.name}! Would you like to equip?")

    def yes():
        hero.equip(equipment)
        output_label.config(text = f"{hero.name} equipped {equipment.name}")
        equip_screen.pack_forget()
        new_floor()
        enable_actions()

    def no():
        output_label.config(text = f"{hero.name} continues on...")
        equip_screen.pack_forget()
        new_floor()
        enable_actions()

    yes_btn.config(command=yes)
    no_btn.config(command=no)
    equip_screen.pack()

def enable_actions():
    attack_btn.config(state="normal")
    heal_btn.config(state="normal")
    retreat_btn.config(state="normal")
    attack_btn.pack()
    heal_btn.pack()
    retreat_btn.pack()

attack_btn = tk.Button(root, text = "Attack", command = attack)
attack_btn.pack()
heal_btn = tk.Button(root, text = "Heal", command = heal)
heal_btn.pack()
retreat_btn = tk.Button(root, text = "Retreat", command = retreat)
retreat_btn.pack()

# This will create a pop-up for equipping items
equip_screen = tk.Frame(root)
yes_btn = tk.Button(equip_screen, text = "Yes")
yes_btn.pack(side="left")
no_btn = tk.Button(equip_screen, text = "N0")
no_btn.pack(side="right")
equip_screen.pack_forget()

root.mainloop()


database.con.close()