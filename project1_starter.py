"""
COMP 163 - Project 1: Character Creator & Saving/Loading
Name: Ashton Partridge
Date: 10/22/2025

AI Usage: [Document any AI assistance used]
Example: AI helped with file I/O error handling logic in save_character function
"""

import os

def create_character(name, character_class):
    """
    Creates a new character dictionary with calculated stats
    Returns: dictionary with keys: name, class, level, strength, magic, health, gold
    
    Example:
    char = create_character("Aria", "Mage")
    # Should return: {"name": "Aria", "class": "Mage", "level": 1, "strength": 5, "magic": 15, "health": 80, "gold": 100}
    """

    stats = calculate_stats(character_class, 1) # Returns a tuple of the calculated stats for a character at level 1
    return {"name": name, "class": character_class, "level": 1, "strength": stats[0], "magic": stats[1], "health": stats[2], "gold": 100, "exp": 0}

def create_backstory(name, character_class): # Selects a preset backstory made for each class 
    origins = {"warrior":"A great warrior that was tired of the mundain village life and now seeks gold and glory", "mage": "A student of one of the four Great Wizards of the relm, now you seek to be more powerful then they could ever be.",
                      "rogue": "As a petty thief on the rat filled streets you decide to take your skills to the next level, what that means is up to you.", "cleric":"As a member of The Guardians of Life you serve to protect the innocent and heal the neady, you venture to spread your wisdom and cures."}
    print(f"Your name is {name}. {origins[character_class]}")
    return origins[character_class]

def calculate_stats(character_class, level): # Calculates character stats based on their class and level
    """
    Calculates base stats based on class and level
    Returns: tuple of (strength, magic, health)
    
    Design your own formulas! Ideas:
    - Warriors: High strength, low magic, high health
    - Mages: Low strength, high magic, medium health  
    - Rogues: Medium strength, medium magic, low health
    - Clerics: Medium strength, high magic, high health
    """

    character_class = character_class.lower() # Force lower the class name so we can assign the proper class
    level_multiplier = 1 + (level/10) # The multiplier determines how much the stat will be increased by per level
    class_stats = {"warrior":{"strength": 20, "magic": 5, "health": 100}, "mage": {"strength": 10, "magic": 30, "health": 70},
                      "rogue": {"strength": 15, "magic": 15, "health": 50}, "cleric":{"strength": 15, "magic": 20, "health": 120}}
    if not class_stats.get(character_class): # If class is not found then default to warrior class
        character_class = "warrior"
    # Calculate the defualt stats with the multiplier
    stats_with_multi = {"strength": class_stats[character_class]["strength"] * level_multiplier, "magic": class_stats[character_class]["magic"] * level_multiplier, "health": class_stats[character_class]["health"] * level_multiplier}
    return (round(stats_with_multi["strength"], 2), round(stats_with_multi["magic"], 2), int(stats_with_multi["health"]))
    


def save_character(character, filename): # Saves the character stats to a file
    """
    Saves character to text file in specific format
    Returns: True if successful, False if error occurred
    
    Required file format:
    Character Name: [name]
    Class: [class]
    Level: [level]
    Strength: [strength]
    Magic: [magic]
    Health: [health]
    Gold: [gold]
    """
    # TODO: Implement this function
    # Remember to handle file errors gracefully
    #save_file = open(filename,"w")
    
    if len(character) <= 6: # Checks that all required save data is present if not then don't attempt to save
        print("ERROR: Save data too short")
        return False
    elif (not os.path.exists(filename)) and filename.find("/") > -1: # Checks if a given save path does or does not exist, if it doesnt then dont save
        print("ERROR: File does not exist")
        return False
    with open(filename, "w") as file: # Creates a new file or if file exists writes over existing data
        if not character['name'].isascii(): # Checks if given name has normal characters
            print("ERROR: Name cannot include special characters")
            return False
        string_to_write = f"Character Name: {character['name']}\nClass: {character['class']}\nLevel: {character['level']}\nStrength: {character['strength']}\nMagic: {character['magic']}\nHealth: {character['health']}\nGold: {character['gold']}\nExp: {character['exp']}"
        file.write(string_to_write)
        
        return True

def load_character(filename): # Loads data from save file
    """
    Loads character from text file
    Returns: character dictionary if successful, None if file not found
    """
    # TODO: Implement this function
    # Remember to handle file not found errors
    if not os.path.exists(filename): #If file does not exist then print error
        print("ERROR: File does not exist")
        return None
    with open(filename, "r") as file: # If file exists read the file and load the data
        loaded_data = {}
        contents = file.read()
        data_list = contents.split("\n")
        for info in data_list: # This entire loop runs through each line and puts the shortened data into a dictionary
            sub_list = info.split(":")
            data = sub_list[-1]
            data = data.strip()
            if data.find(".") > 0 and not data.isalpha(): # Check is data is a decimal number
                data = float(data)
            elif data.isdigit(): # The remaining data with numbers are set to ints
                data = int(data)
            elif len(sub_list[0]) > 1: # Data saved under something like "Character Name" are set to only use the last part such as "Name"
                sub_list = sub_list[0].split(" ")
                sub_list[0] = sub_list[-1]

            loaded_data[sub_list[0].lower()] = data
        return loaded_data
        

def display_character(character): # Prints the character stats
    """
    Prints formatted character sheet
    Returns: None (prints to console)
    
    Example output:
    === CHARACTER SHEET ===
    Name: Aria
    Class: Mage
    Level: 1
    Strength: 5
    Magic: 15
    Health: 80
    Gold: 100
    """
    print("=== CHARACTER SHEET ===")
    print(f"Name: {character['name']}")
    print(f"Class: {character['class']}")
    print(f"Level: {character['level']}")
    print(f"Strength: {character['strength']}")
    print(f"Magic: {character['magic']}")
    print(f"Health: {character['health']}")
    print(f"Gold: {character['gold']}")
    print(f"Experience: {character['exp']}")

def calc_exp(character, exp_gain): # Adds experience to the character dictionary and if exp is at needed level requirements then it increases the level of the character
    exp_needed = character['level'] + 1 * 2900
    character['exp'] += exp_gain
    if character['exp'] >= exp_needed:
        character['exp'] -= exp_needed
        level_up(character)

def level_up(character): # Levels up the character
    """
    Increases character level and recalculates stats
    Modifies the character dictionary directly
    Returns: None
    """
   
    character["level"] += 1 # Increase our level
    new_stats = calculate_stats(character["class"],character["level"]) # Get the updated character stats
    # Print the new stats compared to the old ones
    print("=== LEVELED UP ===")
    print(f"Level: {character['level']-1} -> {character['level']}")
    print(f"Strength: {character['strength']} -> {new_stats[0]}")
    print(f"Magic: {character['magic']} -> {new_stats[1]}")
    print(f"Health: {character['health']} -> {new_stats[2]}")
    # Replace the old stats with the new stats
    character["strength"] = new_stats[0]
    character["magic"] = new_stats[1]
    character["health"] = new_stats[2]

# Main program area (optional - for testing your functions)
if __name__ == "__main__":
    print("=== CHARACTER CREATOR ===")
    print("Test your functions here!")
    
    # Example usage:
    char = create_character("Hero", "Mage")
    display_character(char)
    save_character(char, "my_character.txt")
    loaded = load_character("my_character.txt")
    level_up(char)
