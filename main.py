"""
label = tk.label(root, text = 'Some Text')
label.pack


Label will display text/images
root is where tkinter places it
.pack(), .grid(), .place() actually places it

"""

import tkinter as tk
import tkinter.simpledialog as simpledialog
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

# Character name
name = simpledialog.askstring("Name", "What is your heros name: ")
if name:
    hero.name = name

# Info Labels
floor_label = tk.Label(root, text="")
floor_label.pack(padx = 1, pady = 1)


hero_label = tk.Label(root, text="")
hero_label.pack(padx = 1, pady = 1)


enemy_label = tk.Label(root, text="")
enemy_label.pack(padx = 1, pady = 1)


output_label = tk.Label(root, text = "")
output_label.pack(expand = True, fill = "both", padx = 1, pady = 1)

# Styling

root.configure(bg="black")

hero_label.config(bg="black", fg="white")
enemy_label.config(bg="black", fg="white")
floor_label.config(bg="black", fg="white")
output_label.config(bg="black", fg="white", wraplength=450)

output_label.config(text = "Five years ago the world was peaceful. People attended daily life, children went to school, people dated, traveled,"
"life was... good.\n\n"
"That changed when the earth opened up, and the beasts arrived.\n\n"
"Since then, over half of the "
"worlds population was simply destroyed. Cities burned, homes were lost, people were killed. \n\n"
"You are the last hope of humanity. Descend the depths of this dungeon, find the king of these"
f" demons, and end this. Good luck, and farewll {hero.name}.")

def attack():
    damage = hero.attack(enemy)
    if(enemy.health <= 0):
        gold_drop = random.randint(10,25)
        hero.gold += gold_drop
        update_labels(f"Enemy defeated!")
        item = loot_drop(enemy.rarity, hero)
        log(hero.name, hero.generation, "Killed Enemy", 0, floor)
        if item:
            disable_buttons()
            root.after(1000, lambda: equip_items(item, enemy))
        else:
            root.after(1000, new_floor)
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
    hero_label.config(text = f"{hero.name} HP: {hero.health} | Gold: {hero.gold}")
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
        output_label.config(text = "The king staggers...")
        root.after(1500, lambda: win())
        return
    
    enemy = random.choice(pool)
    update_labels(f"A {enemy.name} appears!")

def win():
    floor_label.config(text = "")
    hero_label.config(text = "")
    enemy_label.config(text = "")
    output_label.config(text = "As the King of Monsters collapses before you, the dungeon falls silent.\n\n"
    "With his final breath, he speaks:\n\n"
    "\"You may have won... today.\n\n"
    "But I was never your enemy.\n\n"
    "I stood guard... against what lies beyond.\n\n"
    "Now... you must face it... alone.\"")
    attack_btn.pack_forget()
    heal_btn.pack_forget()
    retreat_btn.pack_forget()


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
    attack_btn.pack(side = "left", padx = 5)
    heal_btn.pack(side = "left", padx = 5)
    retreat_btn.pack(side = "left", padx = 5)

def start_game():
    start_btn.pack_forget()
    button_frame.pack(pady = 10)
    update_labels(f"A {enemy.name} appears, it's eyes burning red.")
    floor_label.config(text=f"Floor: {floor}")
    hero_label.config(text=f"{hero.name} HP: {hero.health} | Gold: {hero.gold}")
    enemy_label.config(text=f"{enemy.name} Enemy HP: {enemy.health}")

def on_resize(event):
    new_size = max(10, int(event.height / 40))
    output_label.config(
        #wraplength = event.width - 40,
        font = ("Arial", new_size)
    )
root.bind("<Configure>", on_resize)

# This will create my buttons
button_frame = tk.Frame(root, bg="black")
button_frame.pack(pady=10)
attack_btn = tk.Button(button_frame, text = "Attack", command = attack)
attack_btn.pack(side = "left", padx = 5)
heal_btn = tk.Button(button_frame, text = "Heal", command = heal)
heal_btn.pack(side = "left", padx = 5)
retreat_btn = tk.Button(button_frame, text = "Retreat", command = retreat)
retreat_btn.pack(side = "left", padx = 5)
button_frame.pack_forget()

start_btn = tk.Button(root, text = "Descend", command = start_game)
start_btn.pack(pady = 10)

# This will create a pop-up for equipping items
equip_screen = tk.Frame(root)
yes_btn = tk.Button(equip_screen, text = "Yes")
yes_btn.pack(side="left")
no_btn = tk.Button(equip_screen, text = "No")
no_btn.pack(side="right")
equip_screen.pack_forget()

root.mainloop()


database.con.close()