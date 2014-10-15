"""
Some words for AVENTUREGAME
"""

import random
                
def being_adj():
    
    adj_list = [
                'tall','shivering','fat','lemon-lime',
                'flabbergasted','unhappy','giant',
                'flappy','lopsided','soapy','obese'
                ]

    return random.choice(adj_list)

def color():

    colors_list = [
                   'Purple','Magenta','Greenish','Blue','Red',
                   'Yellow','Orange','Green','Pinkish','Cyan',
                   'Fuchsia','Aquamarine','Crimson','Jade',
                   'Grey','Lime'
                  ]

    return random.choice(colors_list)

def extra_adj():

    adverb_list = [
                   'Neon','Bright','Light','Dark','Shimmering','Elven'
                  ]

    return random.choice(adverb_list)

def weapon_adj():
    
    adj_list = [
                'Glistening','Spiked','Crooked','Bloody','Orc',
                'Gnarled','Speckled','Elvish','Bonecrushing'
                ]

    return random.choice(adj_list)

def prestige_weapon_adj():

    adj_list = [
                'Legendary','Mythical','Elite','Noteworthy'
                ]

    return random.choice(adj_list)

def weapon_suffix():

    suffix_list = [
                   'of the North','of Power','of Terror','of Peace','of Fire',
                   'of Merlin', 'of Doom', 'of Ice', 'of the Ancients'
                   ]

    return random.choice(suffix_list)

def tavern_adj():
    
    adj_list = [
                'rusty','greasy','obese','disgruntled','slimy','untasty',
                'bloodred','filthy','irksome','ugly','dismembered','menacing',
                'evil'
                ]

    return random.choice(adj_list)

def woods_name():
    adverb = round(random.random() -.2)
    new = color()
    if adverb:
        new_adverb = extra_adj()
        new = new_adverb + ' ' + new
    tavern_adj_toggle = round(random.random() -.1)

    if tavern_adj_toggle:
        new = tavern_adj() + ' ' + new
    return ("The " + new + " Woods").title()

def noun():
    noun_list = ['Puppy','Cow','Watermelon','Sofa','Bucket','Chicken',
                 'Skeleton','Squirrel','Soup','Tooth','Earlobe']

    return random.choice(noun_list)

def pluralize(noun):
    """
    pluralize a string
    pup -> pups
    puppy -> puppies
    """
    if noun[len(noun)-1] == "y":
        noun = noun[:-1] + "ie"
    noun = noun + "s"
    return noun

def possesivize(name):
    """
    possesify a string
    joe -> joe's
    moses -> moses'
    """
    name += "'"
    if name[len(name)-2] != "s":
        name += "s"
    return name


if __name__ == '__main__':
    # print [noun() for i in range(5)]
    # print [pluralize(noun()) for i in range(5)]
    for i in range(10):
        # print weapon_adj()
        print woods_name()
        # print value