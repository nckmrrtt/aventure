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

    adverb_list = [
                   'Neon','Bright','Light','Dark'
                  ]

    adverb = round(random.random() -.2)
    new = random.choice(colors_list)
    if adverb:
        new_adverb = ''
        new_adverb += random.choice(adverb_list)
        new = new_adverb+ ' ' + new

    return new

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
    new = color()
    tavern_adj_toggle = round(random.random() -.1)
    if tavern_adj_toggle:
        new = tavern_adj() + ' ' + new
    return ("The " + new + " Woods").title()

def noun():
    noun_list = ['Puppy','Cow','Watermelon','Sofa','Bucket','Chicken',
                 'Skeleton','Squirrel','Soup','Tooth','Earlobe']

    return random.choice(noun_list)

def pluralize(noun):
    if noun[len(noun)-1] == "y":
        noun = noun[:-1] + "ie"
    noun = noun + "s"
    return noun

if __name__ == '__main__':
    # print [noun() for i in range(5)]
    # print [pluralize(noun()) for i in range(5)]
    for i in range(10):
        print weapon_adj()
        # print woods_name()
        # print value