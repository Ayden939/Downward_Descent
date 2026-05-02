"""
label = tk.label(root, text = 'Some Text')
label.pack


Label will display text/images
root is where tkinter places it
.pack(), .grid(), .place() actually places it

"""

import tkinter as tk
import tkinter.font as tkfont
import tkinter.simpledialog as simpledialog
from character import Character
from enemy import Skeleton, Goblin, Orc, Phantom, King
from database import log
import database
import random
from equipment import Sword, Shield
from loot import loot_drop
from shop import shop_inventory, purchase_item



# Game objects
hero = Character("Lady Samantha Rostnovak", 1)
floor = 1
enemy = random.choice([Skeleton(), Goblin()])
current_shop_items = []

# Tkinter GUI setup
root = tk.Tk()      # This creates the window, and root.title just applies the title to it
root.title("Legacy Game")
root.geometry("900x650")
root.resizable(False, False)
shared_font = tkfont.Font(family="Arial", size=15)

# Character name
name = simpledialog.askstring("Name", "What is your heros name: ")
if name:
    hero.name = name

# Info Labels
floor_label = tk.Label(root, text="", font = shared_font)
floor_label.pack(padx = 1, pady = (30,1))


hero_label = tk.Label(root, text="", font = shared_font)
hero_label.pack(padx = 1, pady = 1)


enemy_label = tk.Label(root, text="", font = shared_font)
enemy_label.pack(padx = 1, pady = 1)

output_label = tk.Label(root, text = "", font = shared_font)
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
        gold_drop = random.randint(9 + floor, 25 + floor * 3)
        hero.gold += gold_drop
        update_labels(f"Enemy defeated!")
        item = loot_drop(enemy.rarity, hero, floor)
        log(hero.name, hero.generation, "Killed Enemy", 0, floor)
        if item:
            disable_buttons()
            root.after(1000, lambda: equip_items(item, enemy))
        else:
            root.after(1000, new_floor)
        return
        
    enemy_damage = enemy.attack(hero)
    update_labels(f"{hero.name} attacks {enemy.name} for {damage} damage!\n"
    f"{enemy.name} hits back for {enemy_damage} damage!")

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
    if floor % 3 == 0:
        open_shop()
        return
    
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
        floor_label.config(text = "")
        hero_label.config(text = "")
        enemy_label.config(text = "")
        output_label.config(text = "The king staggers...")
        root.after(2000, lambda: win())
        return
    
    enemy = random.choice(pool)
    if floor == 10:
        update_labels(f"The {enemy.name} appears!")
    else:
        update_labels(f"A {enemy.name} appears!")

def win():
    output_label.config(text = "As the King of Monsters collapses before you, the dungeon falls silent.\n\n"
    "With his final breath, he speaks:\n\n"
    "\"You may have won... today.\n\n"
    "But I was never your enemy.\n\n"
    "I stood guard... against what lies beyond.\n\n"
    "Now... you must face it... alone.\"")
    attack_btn.pack_forget()
    heal_btn.pack_forget()
    retreat_btn.pack_forget()

def open_shop():

    attack_btn.pack_forget()
    heal_btn.pack_forget()
    retreat_btn.pack_forget()
    button_frame.pack_forget()

    items = shop_inventory()
    output_label.config(text = "")
    text = "A strange creature appears, offering wares...\n\n"

    for i, item in enumerate(items, 1):
        text += f"{i}) {item['name']} (+{item['value']}): {item['cost']} gold\n"

    shop_label.config(text=text)

    global current_shop_items
    current_shop_items = items
    
    shop_frame.pack(pady = 20)

def buy(index):
    item = current_shop_items[index]
    success, message = purchase_item(hero, item)

    output_label.config(text=message)

    if not success:
        return

    if success:
        update_labels("")

    shop_frame.pack_forget()
    enable_actions()
    button_frame.pack(pady = 30)
    root.after(800, new_floor)

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


# This will create my buttons
button_frame = tk.Frame(root, bg="black")
button_frame.pack(pady=30)
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
equip_screen = tk.Frame(root, bg = "black")
yes_btn = tk.Button(equip_screen, text = "Yes")
yes_btn.pack(side="left", padx = 5, pady = 10)
no_btn = tk.Button(equip_screen, text = "No")
no_btn.pack(side="right", padx = 5, pady = 10)
equip_screen.pack_forget()

# This will create a pop up for the shop (I hope)
shop_frame = tk.Frame(root, bg = "black")
shop_label = tk.Label(shop_frame, text="", bg="black", fg="white", font=shared_font)
shop_label.pack(pady=10)
btn1 = tk.Button(shop_frame, text="Minor Health Upgrade", command=lambda: buy(0))
btn1.pack(pady = 10, padx = 10, side = "left")
btn2 = tk.Button(shop_frame, text="Major Health Upgrade", command=lambda: buy(1))
btn2.pack(pady = 10, padx = 10, side = "left")
btn3 = tk.Button(shop_frame, text="Minor Attack Boost", command=lambda: buy(2))
btn3.pack(pady = 10, padx = 10, side = "left")
btn4 = tk.Button(shop_frame, text="Major Attack Boost", command=lambda: buy(3))
btn4.pack(pady = 10, padx = 10, side = "left")
shop_frame.pack_forget()

root.mainloop()


database.con.close()