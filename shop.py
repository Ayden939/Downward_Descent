def shop_inventory():
    return{
        
        {"name": "Minor Health Potion", "type": "health", "value": 10, "cost": 20},
        {"name": "Major Health Potion", "type": "health", "value": 25, "cost": 40},
        {"name": "Minor Strength Potion", "type": "attack", "value": 5, "cost": 30},
        {"name": "Major Strength Potion", "type": "attack", "value": 10, "cost": 60},

    }

def purchase_item(hero, item):
    if hero.gold < item["cost"]:
        return False, "Not enough gold"

    hero.gold -= item["cost"]

    if item["type"] == "health":
        hero.max_health += item["value"] 
        return True, f"You gain {item['value']} max health!"

    elif item["type"] ==  "attack":
        hero.strength += item["value"]
        return True, f"You gain {item['value']} attack!"

    return False, "Something went wrong."
