import random

def display_player_status(player_stats):
    """Display player's health and attack status"""
    print(f"Your current health: {player_stats['health']}, Attack: {player_stats['attack']}")

def handle_path_choice(player_stats):
    """Player chooses a path"""
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_stats['health'] = min(100, player_stats['health'] + 10)
    else:
        print("You fall into a pit and lose 15 health points.")
        player_stats['health'] = max(0, player_stats['health'] - 15)
        if player_stats['health'] == 0:
            print("You are barely alive!")
    return player_stats

def player_attack(monster_health, player_stats):
    """Player attacks the monster"""
    print(f"You strike the monster for {player_stats['attack']} damage!")
    return monster_health - player_stats['attack']

def monster_attack(player_stats):
    """Monster attacks the player"""
    if random.random() < 0.5:
        print("The monster lands a critical hit for 20 damage!")
        player_stats['health'] -= 20
    else:
        print("The monster hits you for 10 damage!")
        player_stats['health'] -= 10
    return player_stats

def combat_encounter(player_stats, monster_health, has_treasure):
    """Combat encounter between player and monster"""
    while player_stats['health'] > 0 and monster_health > 0:
        monster_health = player_attack(monster_health, player_stats)
        if monster_health <= 0:
            print("You defeated the monster!")
            return has_treasure
        player_stats = monster_attack(player_stats)
        display_player_status(player_stats)
        if player_stats['health'] <= 0:
            print("Game Over!")
            return False
    return has_treasure

def discover_artifact(player_stats, artifacts, artifact_name):
    """Discover an enchanted artifact and apply its effects."""
    if artifact_name in artifacts:
        artifact = artifacts.pop(artifact_name)  # Remove found artifact
        print(f"You discovered: {artifact_name} - {artifact['description']}")
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
        print(f"Effect applied: {artifact['effect']}. Your stats are now: {player_stats}")
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Find and store a unique clue."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Simulates the player exploring the dungeon rooms."""
    for room in dungeon_rooms:
        room_description, item, challenge_type, challenge_outcome = room
        print(room_description)
        if item:
            inventory.append(item)
            print(f"You found a {item}!")
        
        if challenge_type == "library":
            print("You find ancient texts containing cryptic clues.")
            possible_clues = ["The treasure is hidden where the dragon sleeps.", "The key lies with the gnome.", "Beware the shadows.", "The amulet unlocks the final door."]
            for clue in random.sample(possible_clues, 2):
                clues = find_clue(clues, clue)
        
        display_inventory(inventory)
    return player_stats, inventory, clues

def display_inventory(inventory):
    """Displays the player's current inventory"""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for index, item in enumerate(inventory, 1):
            print(f"{index}. {item}")

def main():
    """Main game loop."""
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()

    artifacts = {
        "amulet_of_vitality": {"description": "Glowing amulet, life force.", "power": 15, "effect": "increases health"},
        "ring_of_strength": {"description": "Powerful ring, attack boost.", "power": 10, "effect": "enhances attack"},
        "staff_of_wisdom": {"description": "Staff of wisdom, ancient.", "power": 5, "effect": "solves puzzles"}
    }
    
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]
    
    has_treasure = random.choice([True, False])
    
    display_player_status(player_stats)
    player_stats = handle_path_choice(player_stats)
    
    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat is not None:
            print("You found the hidden treasure!" if treasure_obtained_in_combat else "The monster did not have the treasure.")
        
        if random.random() < 0.3 and artifacts:
            artifact_name = random.choice(list(artifacts.keys()))
            player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
            display_player_status(player_stats)
        
        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:")
            display_inventory(inventory)
            print("Clues:")
            print("\n".join(f"- {clue}" for clue in clues) if clues else "No clues.")

if __name__ == "__main__":
    main()
