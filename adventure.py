'''
This module implements an adventure game.
'''
import random
def display_player_status(player_stats):
    """Display player's health and attack status"""
    print(f"Health: {player_stats['health']}, Attack: {player_stats['attack']}")
def display_inventory(inventory):
    """Displays the player's current inventory"""
    if not inventory:
        print("Your inventory is empty.", end="")
    else:
        print("Your inventory:")
        for index, item in enumerate(inventory, 1):
            print(f"{index}. {item}")
def display_player_status(player_stats):
    print(f"Player Health: {player_stats['health']}, Attack: {player_stats['attack']}")

def discover_artifact(player_stats, artifacts, artifact_name):
    if artifact_name in artifacts:
        artifact = artifacts.pop(artifact_name)
        print(f"You found {artifact_name}: {artifact['description']}")
        if artifact['effect'] == "increases health":
            player_stats['health'] = min(100, player_stats['health'] + artifact['power'])
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
        print(f"Effect: {artifact['effect']} (+{artifact['power']})")
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    for room in dungeon_rooms:
        room_name, item, challenge_type, challenge_outcome = room
        print(f"Entering: {room_name}")
        
        if room_name == "Cryptic Library":
            print("A vast library filled with ancient, cryptic texts.")
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            found_clues = random.sample(possible_clues, 2)
            
            for clue in found_clues:
                clues = find_clue(clues, clue)
            
            if "staff_of_wisdom" in inventory:
                print("With the Staff of Wisdom, you understand the clues and can bypass a puzzle in another room.")
        
        if challenge_type == "puzzle" and "staff_of_wisdom" not in inventory:
            print(challenge_outcome[1])
            player_stats['health'] -= challenge_outcome[2]
        elif challenge_type == "puzzle":
            print("You use your knowledge to bypass the challenge!")
        
    return player_stats, inventory, clues

def combat_encounter(player_stats, monster_health, has_treasure):
    while monster_health > 0 and player_stats['health'] > 0:
        print("You attack the monster!")
        monster_health -= player_stats['attack']
        if monster_health > 0:
            print("The monster retaliates!")
            player_stats['health'] -= 10
        
    if player_stats['health'] > 0:
        print("You defeated the monster!")
        return has_treasure
    else:
        print("You were defeated...")
        return None

def main():
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]
    
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    
    artifacts = {
        "amulet_of_vitality": {"description": "Glowing amulet, life force.", "power": 15, "effect": "increases health"},
        "ring_of_strength": {"description": "Powerful ring, attack boost.", "power": 10, "effect": "enhances attack"},
        "staff_of_wisdom": {"description": "Staff of wisdom, ancient.", "power": 5, "effect": "solves puzzles"}
    }
    
    has_treasure = random.choice([True, False])
    display_player_status(player_stats)
    
    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat:
            inventory.append("treasure")
        
        if random.random() < 0.3:
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
                display_player_status(player_stats)
        
        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts)
            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:", inventory)
            print("Clues:", clues if clues else "No clues.")

if __name__ == "__main__":
    main()

def handle_path_choice(player_stats):
    """Player chooses a path, affecting health."""
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
    """Player attacks the monster."""
    print(f"You strike the monster for {player_stats['attack']} damage!")
    return monster_health - player_stats['attack']

def monster_attack(player_stats):
    """Monster attacks the player."""
    damage = 20 if random.random() < 0.5 else 10
    print(f"The monster hits you for {damage} damage!")
    player_stats['health'] -= damage
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
    """Handles discovery of artifacts and applies their effects."""
    if artifact_name in artifacts:
        artifact = artifacts.pop(artifact_name)  #Remove artifact after discovery
        print(f"You found {artifact_name}: {artifact['description']}")
        if artifact['effect'] == "increases health":
            player_stats['health'] = min(100, player_stats['health'] + artifact['power'])
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
        print(f"Effect: {artifact['effect']} (+{artifact['power']})")
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Adds a new clue if it's not already known."""
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue)  # Using add() method for sets
        print(f"You discovered a new clue: {new_clue}")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Handles dungeon exploration, including the Cryptic Library."""
    room = random.choice(dungeon_rooms)
    print(f"You enter: {room[0]}")

    if room[0] == "Cryptic Library":
        print("A vast library filled with ancient, cryptic texts.")
        possible_clues = [
            "The treasure is hidden where the dragon sleeps.",
            "The key lies with the gnome.",
            "Beware the shadows.",
            "The amulet unlocks the final door."
        ]
        selected_clues = random.sample(possible_clues, 2)
        for clue in selected_clues:
            clues = find_clue(clues, clue)
        if "staff_of_wisdom" in inventory:
            print("With the Staff of Wisdom, you understand the meaning of these clues!")
    return player_stats, inventory, clues


def check_for_treasure(has_treasure):
    """Check if player has the treasure."""
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def acquire_item(inventory,item):
    """Add items to the inventory."""
    inventory.append(item)
    print(f"You acquired a {item}!")
    updated_inventory_list = [item]
    return updated_inventory_list

def main():
    """Main function"""
    dungeon_rooms = [
    ("A dusty old library", "key", "puzzle",\
     ("You solved the puzzle!", "The puzzle remains unsolved.", -5)),
    ("A narrow passage with a creaky floor", None, "trap",\
      ("You skillfully avoid the trap!", "You triggered a trap!", -10)),
    ("A grand hall with a shimmering pool", "healing potion", "none", None),
    ("A small room with a locked chest", "treasure", "puzzle",\
     ("You cracked the code!", "The chest remains stubbornly locked.", -5))]
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_viality": {
            "description": "A glowing amulet that enhances your life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "A powerful ring that boosts your attack damage.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "A staff imbued with ancient wisdom.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }
    has_treasure = random.choice([True, False])
    display_player_status(player_stats)
    player_stats = handle_path_choice(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat is not None:
            check_for_treasure(treasure_obtained_in_combat)

        if random.random() < 0.3 and artifacts:
            artifact_name = random.choice(list(artifacts.keys()))
            player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
            display_player_status(player_stats)

        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon\
                (player_stats, inventory, dungeon_rooms, clues)
            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:", inventory)
            print("Clues:", clues if clues else "No clues.")

if __name__ == "__main__":
    main()
