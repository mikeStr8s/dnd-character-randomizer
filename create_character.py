import json
from pprint import pprint
from Character import Character
import random


def main():
    char = Character('Name')
    choose_race(char)
    choose_subrace(char)
    roll_dice(char)
    choose_class(char)
    pprint(char.__dict__)


def choose_class(character):
    with open('5e-SRD-Classes.json') as file:
        file_data = json.load(file)

    class_index = random.SystemRandom().randint(0, len(file_data) - 1)
    class_data = file_data[class_index]
    character.classname = class_data['name']
    character.hit_die = 'd{}'.format(class_data['hit_die'])
    for entry in class_data['starting_proficiency_options']:
        get_starting_proficiency_options(character, entry)
    get_starting_proficiencies(character, class_data)
    for entry in class_data['saving_throws']:
        character.saving_throws.append(entry['name'])
    choose_equipment(character)


def choose_equipment(character):
    with open('5e-SRD-StartingEquipment.json') as file:
        file_data = json.load(file)

    equip_data = None
    for entry in file_data:
        if entry['class']['name'] == character.classname:
            equip_data = entry

    for item in equip_data['starting_equipment']:
        character.equipment.append({'item': item['item']['name'], 'qty': item['quantity']})

    num_choices = equip_data['choices_to_make']
    choice_fields = []
    for x in range(1, num_choices + 1):
        choice_string = 'choice_{}'.format(num_choices)
        choice_fields.append(choice_string)
        num_choices -= 1

    choose_from = []
    for choice in choice_fields:
        for entry in equip_data[choice]:
            choose_from.append(entry)

    get_equipment_options(character, choose_from)


def get_equipment_options(character, data):
    # Logic to randomly select optional starting proficiencies, if available
    if len(data) > 0:
        for entry in data:
            num_choices = entry['choose']
            choices = entry['from']
            for x in range(0, num_choices):
                rand_index = random.SystemRandom().randint(0, len(choices) - 1)
                selected_choice = choices.pop(rand_index)
                # Add proficiency to character
                character.equipment.append(
                    {'item': selected_choice['item']['name'], 'qty': selected_choice['quantity']})


def roll_dice(character):
    rolls = []
    for x in range(0, 6):
        roll = 0
        smallest_roll = 1234567890
        for y in range(0, 4):
            curr = random.SystemRandom().randint(1, 6)
            if curr < smallest_roll:
                smallest_roll = curr
            roll += curr
        rolls.append(roll - smallest_roll)

    attribs = ['str', 'dex', 'con', 'int', 'wis', 'cha']
    while len(attribs) > 0:
        rand_index1 = random.SystemRandom().randint(0, len(attribs) - 1)
        rand_index2 = random.SystemRandom().randint(0, len(attribs) - 1)
        character.add_bonus({attribs.pop(rand_index1): rolls.pop(rand_index2)})


def choose_subrace(character):
    with open('5e-SRD-Subraces.json') as file:
        file_data = json.load(file)

    # Logic for finding valid subraces for the character race, if available
    valid_subraces = []
    for subrace in file_data:
        if subrace['race']['name'] == character.racename:
            valid_subraces.append(subrace)

    if len(valid_subraces) > 0:
        rand_index = random.SystemRandom().randint(0, len(valid_subraces) - 1)
        chosen_subrace = valid_subraces[rand_index]
        character.subracename = chosen_subrace['name']
        add_subrace_attributes(character, chosen_subrace)

        # Add traits to character
        for trait in chosen_subrace['racial_traits']:
            character.traits.append(trait['name'])

        # Logic to randomly select optional traits, if available
        try:
            to = chosen_subrace['racial_trait_options']
            if len(to) > 0:
                num_choices = to['choose']
                choices = to['from']
                for x in range(0, num_choices):
                    rand_index = random.SystemRandom().randint(0, len(choices) - 1)
                    selected_choice = choices.pop(rand_index)
                    # Add randomly selected trait
                    character.traits.append(selected_choice['name'])
        except KeyError:
            print('No trait options for this race, skipping')


def add_subrace_attributes(character, subrace):
    character.add_bonus(get_ability_bonuses(subrace))
    get_starting_proficiencies(character, subrace)
    get_starting_proficiency_options(character, subrace['starting_proficiency_options'])
    get_languages(character, subrace)
    get_language_options(character, subrace)


def get_ability_bonuses(data):
    # Logic to find what ability bonuses to apply to the character
    attribs = ['str', 'dex', 'con', 'int', 'wis', 'cha']
    added_bonus = {}
    for x in data['ability_bonuses']:
        if x > 0:
            added_bonus[attribs[data['ability_bonuses'].index(x)]] = x

    return added_bonus


def get_starting_proficiencies(character, data):
    # Logic to find what racial skills/proficiencies to add to the character if available
    sp = data['starting_proficiencies']
    if len(sp) > 0:
        for prof in sp:
            if 'Skill' in prof['name']:
                racial_skill = prof['name'].replace('Skill: ', '')
                # Add skill to character
                character.skills.append(racial_skill)
            else:
                # Add proficiency to character
                character.proficiencies.append(prof['name'])


def get_starting_proficiency_options(character, data):
    # Logic to randomly select optional starting proficiencies, if available
    if len(data) > 0:
        num_choices = data['choose']
        choices = data['from']
        for x in range(0, num_choices):
            rand_index = random.SystemRandom().randint(0, len(choices) - 1)
            selected_choice = choices.pop(rand_index)
            # Add randomly selected proficiency
            if 'Skill' in selected_choice['name']:
                racial_skill = selected_choice['name'].replace('Skill: ', '')
                # Add skill to character
                character.skills.append(racial_skill)
            else:
                # Add proficiency to character
                character.proficiencies.append(selected_choice['name'])


def get_languages(character, data):
    # Add languages to character
    for language in data['languages']:
        character.languages.append(language['name'])


def get_language_options(character, data):
    # Logic to randomly select optional languages, if available
    lo = data['language_options']
    if len(lo) > 0:
        num_choices = lo['choose']
        choices = lo['from']
        for x in range(0, num_choices):
            rand_index = random.SystemRandom().randint(0, len(choices) - 1)
            selected_choice = choices.pop(rand_index)
            # Add randomly selected language
            character.languages.append(selected_choice['name'])


def choose_race(character):
    with open('5e-SRD-Races.json') as file:
        file_data = json.load(file)

    race_index = random.SystemRandom().randint(0, 8)
    race_data = file_data[race_index]
    character.racename = race_data['name']
    character.speed = race_data['speed']
    character.size = race_data['size']
    get_starting_proficiencies(character, race_data)
    get_starting_proficiency_options(character, race_data['starting_proficiency_options'])
    get_languages(character, race_data)
    get_language_options(character, race_data)
    character.add_bonus(get_ability_bonuses(race_data))

    # Add traits to character
    for trait in race_data['traits']:
        character.traits.append(trait['name'])

    # Logic to randomly select optional traits, if available
    try:
        to = race_data['trait_options']
        if len(to) > 0:
            num_choices = to['choose']
            choices = to['from']
            for x in range(0, num_choices):
                rand_index = random.SystemRandom().randint(0, len(choices) - 1)
                selected_choice = choices.pop(rand_index)
                # Add randomly selected trait
                character.traits.append(selected_choice['name'])
    except KeyError:
        print('No trait options for this race, skipping')


if __name__ == "__main__":
    main()
