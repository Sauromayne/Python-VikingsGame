# Nicholas Podsiadlo
# SNHU
# 4/18/2021
import random


# display instructions to the player
def show_instructions():
    # print a main menu and the commands
    print("Viking Text Adventure Game:")
    print(
        "Collect 6 God talismans to win the game, or be defeated by Ivar the Boneless."
    )
    print("Move commands: go South, go North, go East, go West.")
    print("Add to Inventory: get 'item name'.")
    print("Inputs can be entered in upper or lower case.")
    print("Type 'help' at anytime to display these instructions again.\n")


# Display the players current status
def player_status(inventory, current_location, strength, lives):
    if lives > 0:
        print("\nYou are in {}".format(current_location))
        print("Inventory : {}".format(inventory))
        print("Current strength: {}".format(strength))
        print("Current lives: {}".format(lives))
        print("-" * 20, "\n")
        return input("Enter your move: ")


# function to move between the dictionary rooms
def move(player_input, location, rooms):
    # direction player wants to move
    direction = player_input
    # check if direction is in the dictionary for this room
    if direction in rooms[location]:
        # set location to the value relating to the key of the direction and return the value
        location = rooms[location][direction]
        return location
    # direction was not found in the dictionary so cant go that way, return the unchanged location
    else:
        print(
            "\nYou cannot move {} from {}, please try a different direction".format(
                direction, location
            )
        )
        return location


# function to get an item if one is available
def get_item(player_input, location, rooms, inventory, strength):
    # set the desired item to the players input
    item = player_input

    # check if the current room has any items
    if "item" in rooms[location]:
        # room has an item, check if its the same item the player input
        if item == rooms[location]["item"]:
            # put the item in inventory if its here
            inventory.append(item)
            # remove the item from the dictionary so the player can't get duplicates
            del rooms[location]["item"]
            # inform the player that they have grabbed the item and are growing stronger
            print(
                "As you grab the {} you can sense the power of your army increasing!".format(
                    item
                )
            )
            # increase the players strength by one
            strength += 1
            # return the new inventory
            return [inventory, strength]
        else:
            # inform player the item wasn't found
            print("Sorry {} is not in {}. (Check your spelling)".format(item, location))
            return [inventory, strength]

    # if the item is not found, inform player and make no adjustments to the inventory
    else:
        print("Sorry {} is not in {}. (Check your spelling)".format(item, location))
        return [inventory, strength]


# function to check if a room has an item
def has_item(location, rooms):
    # check if the current room has any items
    if "item" in rooms[location]:
        # display the items name to the player
        print("\nThere is an item here: {}".format(rooms[location]["item"]))
    else:
        print()


# check if a room has an enemy and that it is not None
def has_enemy(location, rooms, lives, strength):
    if (
        "enemy" in rooms[location]
        and rooms[location]["enemy"] is not None
        and rooms[location]["enemy"] != "Ivar the Boneless"
    ):
        # display the name of the enemy
        print(
            "\nYou have arrived in {} and must first face Ivar's {}!".format(
                location, rooms[location]["enemy"]
            )
        )
        # start combat, enemy found
        lives = start_combat(location, lives, strength, rooms[location]["enemy"], rooms)
        return lives
    else:
        return lives


# check if the room has boss to perform inventory check
def has_boss(location, rooms, lives, strength, inventory, player_won):
    # check if room has boss (need all 6 talismans to face boss)
    if rooms[location]["enemy"] == "Ivar the Boneless":
        print(
            "\nYou have breached Kattegat's defenses and stand upon the mighty Ivar the Boneless!\n"
            "You must have all 6 God talismans to fight,\n"
            "Checking inventory...\n"
        )
        print(inventory, "\n")
        # make sure the player has all the talismans before starting combat
        if len(inventory) == 6:
            print("You have all the talismans, you are ready to fight Ivar!")
            lives = start_combat(
                location, lives, strength, rooms[location]["enemy"], rooms
            )
            if lives > 0:
                player_won = True
        else:
            lives = 0
            print(
                "You did not have all the Talismans, you stand no chance and Ivar beheads you!"
            )

    return [player_won, lives]


# combat works with a die roll. combat ends when the player wins or loses all their lives
def start_combat(location, lives, strength, enemy, rooms):
    player_won = "n"
    # combat continues until the player has won
    while player_won == "n" and lives > 0:
        # roll the die to determine the players roll
        print("\nPlayer starting strength: {}".format(strength))
        print("Rolling for player...\n")
        player_roll = strength + roll_die()
        print("Player Total: {}\n".format(player_roll))

        # figure out the enemies starting strength
        enemy_strength = rooms[enemy]["strength"]
        # roll the die for the enemy
        print("\nEnemy starting strength: {}".format(enemy_strength))
        print("Rolling for enemy..\n")
        enemy_roll = enemy_strength + roll_die()
        print("Enemy total: {}\n".format(enemy_roll))

        # player won the roll
        if player_roll > enemy_roll:
            if enemy != "Ivar the Boneless":
                print(
                    f"After a long battle you come out victorious! {player_roll} vs {enemy_roll}. "
                    "You can now grab any items here.\n"
                )
                # set enemy value to None as they have been defeated in this room
                rooms[location]["enemy"] = None
            # display a different message if defeated by ivar
            else:
                print(
                    f"You have bested {enemy} in single combat! ({player_roll} vs {enemy_roll})"
                )
                print(
                    f"For his crimes against Norway you perform a blood eagle ritual while "
                    f"all the citizens of {location} cheer you on.\n"
                )

            player_won = "y"
        # rolls were tied, roll again
        elif player_roll == enemy_roll:
            print(f"The roll was a tie ({player_roll} vs {enemy_roll})")
            print("The battle continues....\n")
        # player lost the roll
        else:
            lives -= 1  # player lost the fight, lose a life
            if enemy != "Ivar the Boneless":
                print("You have been wounded in battle!")
                print(
                    f"({enemy_roll} vs {player_roll}) You have {lives} lives remaining.\n"
                )
                if lives > 0:
                    print("The battle continues...\n")
            else:
                print(
                    f"{enemy} is a relentless opponent, you must focus in order to win this battle!"
                )
                print(
                    f"({enemy_roll} vs {player_roll}) You have {lives} lives remaining.\n"
                )
                if lives > 0:
                    print("The battle continues...\n")

    # return the amount of lives left
    return lives


# create a function to role the die in case you want to make future adjustments to the die roll
# for example, more die, or using d20 instead of 6 sided die.
def roll_die():
    input("Type 'r' to roll\n")
    result = random.randint(1, 6)
    print("Rolled {}\n".format(result))
    return result


if __name__ == "__main__":
    # define empty inventory list
    inventory = []
    lives = 5  # starting lives is 5
    strength = 3  # starting strength is 3
    player_won = False
    return_list = []

    # A dictionary linking a room to other rooms
    # and linking one item for each room except the Start town (Hedeby) and the town containing the villain
    rooms = {
        "Hedeby": {
            "South": "North Sea",
            "North": "Norwegian Sea",
            "East": "Kattegat Fjord",
            "West": "Lost at Sea",
            "enemy": None,
        },
        "North Sea": {
            "North": "Hedeby",
            "East": "Francia",
            "West": "England",
            "item": "Balder Talisman",
            "enemy": None,
        },
        "England": {
            "East": "North Sea",
            "item": "Loki Talisman",
            "enemy": "Warriors",
        },  # contains warriors
        "Francia": {
            "West": "North Sea",
            "item": "Freyja Talisman",
            "enemy": "Warriors",
        },  # contains warriors
        "Lost at Sea": {"East": "Hedeby", "enemy": "Kraken"},  # contains Kraken
        "Norwegian Sea": {
            "South": "Hedeby",
            "West": "Greenland",
            "item": "Thor Talisman",
            "enemy": None,
        },
        "Greenland": {
            "East": "Norwegian Sea",
            "item": "Odin Talisman",
            "enemy": "Warriors",
        },  # contains warriors
        "Kattegat Fjord": {
            "West": "Hedeby",
            "North": "Kattegat",
            "item": "Tyr Talisman",
            "enemy": "Ballista",
        },  # contains ballista
        "Kattegat": {"enemy": "Ivar the Boneless"},  # boss room
        # define more nested dictionaries within rooms to store enemy strength values
        "Warriors": {"strength": 4},
        "Ballista": {"strength": 7},
        "Kraken": {"strength": 8},
        "Ivar the Boneless": {"strength": 10},
    }

    # game is starting, show instructions to the player
    show_instructions()

    # players starting location is Hedeby
    current_location = "Hedeby"

    # gameplay loop that runs all of the previously defined functions
    while not player_won:
        # check if current location has enemies
        lives = has_enemy(current_location, rooms, lives, strength)

        # check if current location has boss enemy
        return_list = has_boss(
            current_location, rooms, lives, strength, inventory, player_won
        )
        # store the values that were returned from has_boss
        player_won = return_list.pop(0)
        lives = return_list.pop(0)

        # check after fights to see the the player won or is dead
        if player_won:
            break
        if player_won is False and lives == 0:
            break

        # check if current location has items
        has_item(current_location, rooms)

        # show player status, returns players choice
        choice = player_status(inventory, current_location, strength, lives)

        # if elif else branch to determine what the player wants to do
        if choice.split()[0].lower() == "go":
            current_location = move(choice.split()[1].title(), current_location, rooms)
        elif choice.split()[0].lower() == "get":
            inventory = get_item(
                choice.split(" ", 1)[1].title(),
                current_location,
                rooms,
                inventory,
                strength,
            )
            strength = inventory[-1]
            # we have stored our strength value so now we need to get it out of the inventory list
            inventory.pop()
            # our inventory is stored in a list at the starting index
            # this is due to both inventory and strength being returned in a list
            inventory = inventory[0]
        elif choice.split()[0].lower() == "help":
            show_instructions()
        # inform player if their input wasn't valid
        else:
            print("Invalid input, try again")

    # since we have broken from the gameplay loop check if the player still has lives to determine if they have won
    if lives > 0:
        print(
            "Congratulations you have defeated Ivar and taken back control of Kattegat! "
            "You have been crowned King of all Norway and will surely be remembered as a "
            "great leader and warrior."
        )
    else:
        print(
            "Unfortunately Ivar has defeated you and Norway will surely suffer for many generations."
        )
        print("GAME OVER :(")

