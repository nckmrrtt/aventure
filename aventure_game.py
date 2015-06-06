"""

AVENTUREGAME

"""

import logging #LOG: uncomment all lines containing this comment to enable error logging to a test file
logging.basicConfig(level=logging.DEBUG, filename='AVENTUREGAME_debug.log') #LOG

########### imports n stuff ###########

import random
import getpass
import config
import hashlib
import cPickle as pickle

########### local ###########

import words
import helpful
import items_lists

########### logistics ###########

def head_asplode():
    raise HeadAsplodeError('YOU HEAD ASPLODE')
   
def encounter_monster(categories=None):
    global monsters_defeated
    result = fight(categories)
    if result == 'death':
        raw_input('You defeated ' +str(monsters_defeated) + ' monsters before dying a grisly death!\n')
        return 'death'
    else:
        return

def fight(who_fight=None):
    """
    returns 'win' or 'lose', or 'death'
    modifies monsters_defeated

    who_fight can be list of categories or a specific monster
    """
    global monsters_defeated
    
    if isinstance(who_fight,helpful.Being):
        ###specific monster
        enemy = who_fight

    elif isinstance(who_fight,list):
        ###list of categories
        enemy = items_lists.random_monster(random.choice(who_fight))

    else:
        ###else picks a monster at random, not boss though
        enemy = items_lists.random_monster()

    # print 'fighting:\n' + enemy.advanced_str()
    encountered = words.being_adj().capitalize() + ' ' + str(enemy)
    raw_input(str(player) + ' encounters a ' + encountered + '!\n')
    choice = helpful.pick_item(['yes','no','inventory'],'Fight?','inventory')

    while choice == 'inventory':
        inspect_inventory()
        choice = helpful.pick_item(['yes','no','inventory'],'Fight?','inventory')

    if choice == 'yes':

        while enemy.get_health() > 0 and player.get_health() > 0:
            #player attacks
            item = helpful.pick_item(player.get_inventory(), 'What to use?')
            player.use(item)
            attack = item.get_damage()
            defend = item.get_health()

            if attack > 0:
                enemy.hit(item)
                raw_input('You dealt ' +str(attack) + ' damage!')
            elif defend > 0:
                raw_input('You gained ' + str(defend) + ' HP!')
            else:
                raw_input('That was pretty dumb.\n')
            
            if enemy.get_health() > 0: #if the enemy is still alive

                ###enemy attacks, using random item in enemy's inventory
                enemy_choice = random.choice(enemy.get_inventory())
                player.hit(enemy_choice)
                raw_input(str(enemy).capitalize() + ' used ' + str(enemy_choice) + '!\n')
                raw_input('You lost ' + str(enemy_choice.get_damage()) + ' health!\n')
                
            player.set_health(max(0,player.get_health())) #make health nonnegative
            enemy.set_health(max(0,enemy.get_health()))

            print('Player Health: ' + str(player.get_health()) + '\n')
            raw_input(str(enemy) + ' Health: ' + str(enemy.get_health()) + '\n')
        
        if enemy.get_health() == 0:
            winner = str(player)
            money = enemy.get_money()
            print('You looted the following items:\n' + enemy.get_inv_string())
            raw_input('and gained ' + str(money) + ' smackaroonies.\n')
            player.gain_money(money)
            player.grab_items(enemy.get_inventory())
            result = 'win'
            monsters_defeated += 1

        if player.get_health() == 0:
            winner = str(enemy)
            result = 'death'

        print(winner + ' wins!\n')

    elif choice == 'no':

        ouch = random.randrange(0,2)
        if enter_two == config.confus(config.config2):
            ouch = 0
            global cheated
            cheated = True
            print '<yolo>'
        if ouch:
            enemy_choice = random.choice(enemy.get_inventory())
            player.hit(enemy_choice)
            print 'You got away, but were hit by the ' + \
            str(enemy) +"'s " + str(enemy_choice) +'!' + '\n'
            raw_input('You sustained ' + str(enemy_choice.get_damage()) +' damage.\n')
            if player.get_health() <= 0:
                return 'death'
        else:
            raw_input('You got away safely!\n\nThat was close!\n')
        result = 'lose'

    return result

def inspect_inventory(sell=False):
    """
    can inspect or sell items from inventory
    """
    choice = 'poop'

    if sell:
        while choice != 'done':
            choices = list(player.get_inventory())
            choices += ['done']
            choice = helpful.pick_item(choices,'Sell something?','done')
            # if choice == 'done':
            if str(choice) == 'mythical kumquat':
                raw_input("You can't sell your " + str(choice) + "!\n")
            elif choice == 'done':
                return
            else:
                cost = choice.get_cost()
                question = 'Sell your ' + str(choice) + ' for $' + str(cost) + '?'
                sell_yn = helpful.pick_item(['yes','no'],question)
                if sell_yn == 'yes':
                    cost = choice.get_cost()
                    player.gain_money(cost)
                    player.drop(choice)
                    raw_input('You sold your ' + str(choice) + '. ' + \
                              "That's $" + str(cost) + ' more in your pocket.\n')

    else: #if not selling
        while choice != 'done':
            choices = list(player.get_inventory())
            choices += ['done']
            intro = 'Type item name/number for more info...\n\nInventory:'        
            choice = helpful.pick_item(choices,intro,'done')
            if choice == 'done':
                return
            raw_input(choice.advanced_str())
            if choice.get_health() > 0:
                use_yn = helpful.pick_item(['yes','no'],'Use this item?')
                if use_yn == 'yes':
                    player.use(choice)

def inspect_map():
    if world_map:
        print '    +---------+'
        print '    ' + map_0
        print '    ' + map_1
        print '    ' + map_2
        print '    +---------+'
        raw_input('')

    else:
        raw_input('You have no world map :(')
    return 

def pick_place(choices_arg, question='Where to next?',inv=True):
    """
    pretty much identical to pick_item. at least, it started that way.
    break_before works (or at least, it should), it breaks before inventory
    """
    
    choices_alt = []
    
    if isinstance(choices_arg,list):
        choices = list(choices_arg)
        if inv:
            choices += ['inventory','map']
    
    elif isinstance(choices_arg,tuple):
        choices = choices_arg[0]
        choices_alt = choices_arg[1]
        if inv:
            choices += ['inventory','map']
            choices_alt += ['inventory','map']

    staying = True
        
    while staying:

        print question + '\n'

        if choices_alt:
            for index in range(len(choices_alt)): #print alternate choices in menu form
                if str(choices[index]) == 'inventory':
                    print
                print(str(index+1) + ': ' + str(choices_alt[index]))

        else:
            for index in range(len(choices)): #print choices in menu form
                if str(choices[index]) == 'inventory':
                    print
                print(str(index+1) + ': ' + str(choices[index]))

        print('') #get some blank line in here yo
        chosen = raw_input('').lower()
        
        try:
            final = ''
            for index in range(len(choices)): #check if they typed a number
                item = choices[index]
                if index == int(chosen)-1:
                    final = item
                    staying = False
            if final == '':
                print 'Nice Try.\n' #if they type a number not in range
                question = 'Try again, foo.'
        except:
            final = ''
            if choices_alt:
                for index in range(len(choices_alt)): #check if they typed letters
                    item = choices_alt[index]
                    if chosen == str(item).lower():
                        final = choices[index]
                        staying = False

            else:
                for index in range(len(choices)): #check if they typed letters
                    item = choices[index]
                    if chosen == str(item).lower():
                        final = item
                        staying = False
            if final == '':
                print 'Nice Try.\n' #if they misspelled
                question = 'Try again, foo.'

        if final == 'map':
            inspect_map()
            question = 'Where to?'
            staying = True
        if final == 'inventory':
            inspect_inventory()
            question = 'Where to?'
            staying = True

    return final

########### journeying ###########

def visit(location):
    """
    this function (and every function after it in this section)
    should return a string name of the next place to visit
    
    dying is no return
    """
    
    func_map = {
                'woods':woods_0_0,
                'purchase beer':beer,
                'purchase weapons':buy,
                'sell stuff':sell,
                'purchase map':buy_map,
                'map':inspect_map
                }
    
    global locations_list
    global press_enter
    global map_0, map_1, map_2

    # reset map
    map_0 = '|         |' + map_0[12:]
    map_1 = '|         |' + map_1[12:]
    map_2 = '|         |' + map_2[12:]

    locations_list = func_map.keys()
    
    if location not in locations_list:
        
        try:
            func = eval(location)
        except:
            print 'you dumb, bro'
            return 'death'

    else:
        func = func_map[location]

    crazy_spot = 0

    if location[0:5] == 'woods': #only go into the portal/bongos from the woods
        crazy_spot = random.randint(0,15)
        if crazy_spot == 1:
            func = bongos
        if crazy_spot == 2:
            func = portal

    return func()

### tavern stuff ###

def tavern():
    """
    where all the cool kids hang out 
    +---------+
    |         |
    |    T    |
    |         |
    +---------+
    """
    global tavern_name
    global bartender_name
    global press_enter, enter_two, enter_four

    global map_1
    map_1 = '|    T    |' + map_1[12:]

    if not tavern_name:
        tavern_name = 'The ' + words.tavern_adj().capitalize() + ' ' + \
                      words.noun().capitalize() + ' Tavern'
        bartender_name = random.choice(items_lists.npc_name_list)
        enter_two = getpass.getpass('You enter ' + tavern_name + '.\n')
        raw_input('The bartender, ' + bartender_name + ', grins at you.\n')
        raw_input('"Greetings, ' + str(player) + '."')
        enter_four = getpass.getpass('"' + "We're out of beer." +'"\n')
        if press_enter == config.confus(config.config0):
            player.grab(config.config1)
            global cheated
            cheated = True

    else:
        raw_input('You enter ' + tavern_name + '.\n')
        raw_input('The bartender, ' + bartender_name + ', grins at you.\n')
        raw_input('"You again, ' + str(player) + ' ?"')
        raw_input('"Yup, ' + "we're still out of beer." + '"\n')

    in_tavern = True
    
    while in_tavern:

        choices = (
                ['beer','buy map','buy','sell','mirror','box','woods','imp_weapons'],
                ['purchase beer','purchase map','purchase weapons','sell stuff','mirror','intriguing box','back to the woods','creepy guy']
                  )

        next = pick_place(choices,'What next?')

        if next == 'beer':
            beer()
        elif next == 'buy map':
            buy_map()
        elif next == 'buy':
            buy()
        elif next == 'sell':
            sell()
        elif next == 'mirror':
            mirror()
        elif next == 'box':
            box()
        elif next == 'imp_weapons':
            imp_weapons()
        else:
            return next

        raw_input('You return to the bar.\n')
        raw_input('The bartender winks at you.\n')

def beer():
    """
    should only be called from in the tavern
    """
    global cheated

    if enter_four == config.confus(config.config4):
        player.grab(helpful.Item('SixPack',10,0,0,6))
        cheated = True
        print '<achievement unlocked>\n'

    if player.get_money() >= 17:

        player.set_health(100)
        player.lose_money(17)

        raw_input('You take out your money.\n')
        raw_input(bartender_name + ' chuckles.\n')
        raw_input('"I guess we have this stuff, if you really need a drink."\n')

        raw_input("The 'beer' healed you!\n")
        raw_input('It also cost $17.\n')
        
    else:
        print bartender_name + ' chuckles and looks pointedly at his empty tip jar.\n'
        raw_input('"' +"We're out of beer." + '"\n')
        raw_input('"Nice try."\n')

def buy_map():
    """
    should only call from the tavern
    """
    
    global world_map

    if world_map:
        raw_input('You already have one!')
    elif player.get_money() >= 10:
        raw_input('You bought a map for $10! Woohoo!\n')
        player.lose_money(10)
        world_map = True
    else:
        raw_input('"You seem to be a bit low in the money department..."\n')

def buy():
    
    raw_input('"Buying stuff, eh? ' + "Let's see what I got." +'"\n')

    choice = 'poop'

    if player.get_money() == 0:
        raw_input('"Hey, you have no money! Nice try!"\n')
        choice = 'done buying'

    while choice != 'done buying':

        sale = items_lists.random_weapon()
        markup = sale.copy(None,None,None,sale.get_cost()*2)
        # print 'yolo'
        raw_input(markup.advanced_str())

        purchasable = False
        if player.get_money() >= markup.get_cost():
            purchasable = True
        if purchasable:
            choice = helpful.pick_item(['yes','more options','done buying'],'Buy ' + str(sale) + '?')
            if choice == 'done buying':
                break
            if choice == 'yes':
                player.grab(sale)
                player.lose_money(markup.get_cost()) #see that shady deal? ooh so shady

        else: #too expensive
            raw_input('"Never mind... You seem to be a bit short on cash."\n')
            choice = helpful.pick_item(['more options','done buying'],'Keep shopping?')

        if choice == 'done buying':
            break

        print '"We also have this fine item..."\n'

def sell():
    raw_input('"Selling stuff, eh? ' + "Let's see what you got." +'"\n')
    inspect_inventory(True)

def mirror():
    """
    wooo
    """
    raw_input("You walk to a mirror hanging on the wall " + \
              "and admire your rugged visage.\n")
    raw_input(player.advanced_str())
    # raw_input('') #TODO see if this is better

def box():
    """
    leave thing for next player?
    """
    raw_input("There's a note on a wooden box:\n\n" + \
              '"Take an item, leave an item..."\n')
    choices = (
              ['box','done'],
              ['leave something in the box','ignore']
              )

    choice = helpful.pick_item(choices,'Do it.')

    if choice == 'box':

        gotem = pickle.load(open("box.txt", "rb"))
        # gotem = helpful.Item('test_item')

        item = 'mythical kumquat'
        question = 'What to leave in the box?'

        while str(item) == 'mythical kumquat':
            item = helpful.pick_item(player.get_inventory(),question)
            question = 'No, really.'

        pickle.dump(item, open("box.txt", "wb"))
        player.drop(item)
        player.grab(gotem)

        raw_input('You trade your ' + str(item) + ' for the item in the box:\n')
        print gotem.advanced_str()

def imp_weapons():
    global BORIS_CRED
    raw_input("You walk towards the creepy-looking man with red glowing eyes.\n")
    if BORIS_CRED > 100:
        print('"WELCOME, FRIEND. GOOD TO SEE YOU AGAIN."\n')
    else:
        print('"WELCOME TO THE MAGIC ANVIL. MY NAME IS BORIS."\n')
    #learn more and more about boris
    #get good prices with boris
    #one day, he'll come with you to fight and win glory woohoo
    talk = helpful.pick_item(["Okay.","No."],'"MY SERVICES COST A MILLION DOLLARS."')
    
    if talk == "Okay.":
        if player.get_money() > 1000000:
            player.lose_money(1000000)
            raw_input("WOW. THAT IS SO MUCH MONEY. THANK YOU. WHATEVER YOU WANT, FOR FREE.")
            BORIS_CRED += 1000000
        elif BORIS_CRED > 100:
            raw_input("NO CHARGE FOR FRIENDS OF BORIS.\n")
            BORIS_CRED += 2
        else:
            raw_input('"' + "YOU OBVIOUSLY DON'T HAVE A MILLION DOLLARS. THAT'S OKAY THOUGH." +'"\n')
            choice = pick_item(["$100","$10","Haha. No."],"Donate to Boris?")
            if choice == "$100":
                player.lose_money(100)
                BORIS_CRED += 50
            elif choice == "$10":
                player.lose_money(10)
                BORIS_CRED += 2
            else:
                BORIS_CRED -= 10 
    else:
        raw_input('"WELL THEN. GOODBYE."\n')
        BORIS_CRED -= 5
        return

    while talk != "Done":
        improve = helpful.pick_item(player.get_inventory() + ['"Never mind, I want a refund."'],'"WHAT WOULD YOU LIKE TO IMPROVE?"\n')
        if choice == '"Never mind, I want a refund."':
            raw_input('"NO REFUNDS."\n')
            BORIS_CRED -= 1
            continue
        if BORIS_CRED > 900000:
            improve.inc_damage(100)
        elif BORIS_CRED > 100:
            improve.inc_damage(10)
        else:
            improve.inc_damage(5)
        raw_input('"OKAY, I IMPROVED YER ' + str(improve) + '"\n')
        print(improve.advanced_str())
        raw_input('"YOU' + "'" + 'RE WELCOME."\n')

def traveler():
    """ TODO """
    raw_input('A wizened old traveler ')\

def advice():
    """
    TODO
    """
    raw_input('A sign on the counter reads: "Advice $1".\n')
    raw_input('The bartender leans in close and whispers:\n')
    # raw_input('...\n')
    raw_input('"There is an old man hidden in the forest. You must talk to him."\n')
    # return 'tavern'

### cool places ###

def arena():
    """
    location
    arena where you fight until you die hahahaha
    """
    global monsters_defeated, arena_boss

    if not arena_boss:
        arena_boss = items_lists.random_monster('boss_monsters')
        # print '<arena boss = ' + str(arena_boss) + '>\n'

    raw_input("You enter a terrifyingly massive arena.\n")
    raw_input("Thousands of bloodthirsty fans are screaming your name.\n")
    raw_input("Suddenly, the doors behind you close with a slam.\n")
    raw_input("There's no escape.\n")

    boss_win = False
    arena_monsters_encountered = 0

    while player.get_health() > 0 and not boss_win:
        arena_monsters_encountered += 1
        if arena_monsters_encountered % 10:
            fight()
        else: #every 10th monster, fight the boss
            boss_fight = fight(arena_boss)
            if boss_fight == 'win':
                boss_win = True

    if boss_win:
        raw_input("The dying monster's body crashes through the floor, revealing " + \
                  "a cavernous tunnel underneath the arena...\n")
        raw_input("The fans are getting restless, demanding another fight. You seize " + \
                  "your opportunity quickly and enter the enormous tunnel.\n")
        return 'main_tunnel'

    else:
        raw_input('You defeated ' +str(monsters_defeated) + ' monsters before dying a grisly death!\n')
        return 'death'

def portal():
    """
    location
    """
    raw_input("Oops.\n")
    raw_input("You trip and fall into a mysterious portal...\n")
    raw_input("...\n")
    raw_input("...\n")
    raw_input("You wake up in a pair of " + words.color().lower() + \
              " shoes and a " + words.color().lower() + " hat.\n")
    raw_input("That's odd.\n")
    next = [
            'woods_1_1','woods_n1_1','woods_1_n1','woods_n1_n1','arena'
            ]
    return random.choice(next)

def bongos():
    
    global bongo_string

    raw_input("You stumble upon a large set of bongo drums!\n")

    next_bongo = 'poop'

    while next_bongo != 'done':
        next_bongo = helpful.pick_item(['a','b','c','d','e','f','g','done'],'Bongo?','done')
        if next_bongo == 'done':
            break
        bongo_string += next_bongo
        if len(bongo_string) > 8:
            bongo_string = bongo_string[1:]
        print 'The bongo booms a glorious "' + next_bongo + \
                  '" that rings through the woods ominously.\n'

        bongo_code_8 = hashlib.md5(bongo_string).hexdigest()
        bongo_code_7 = hashlib.md5(bongo_string[1:]).hexdigest()
        bongo_code_6 = hashlib.md5(bongo_string[2:]).hexdigest()

        if bongo_code_8 == '':
            print 'yolo'
        elif bongo_code_7 == 'b3188adab3f07e66582bbac456dcd212':
            raw_input('a plant appears')
        elif bongo_code_7 == '54a28e933e22fbabf29e267dd3f5c908':
            raw_input('a giant computer appears')

        # print 'bongocode',bongo_code_6,bongo_code_8
        # print 'bongostring',bongo_string


    raw_input("You leave the mystical bongo circle, but to your amazement, " + \
              "the woods have shifted around you.\n")
    next = [
            'woods_1_1','woods_n1_1','woods_1_n1','woods_n1_n1','arena'
            ]
    goto = random.choice(next)
    return goto

### woods ###

def woods_0_0():
    """
    main, central woods
    +---------+
    |         |
    |    X    |
    |         |
    +---------+
    """
    global woods_0_0_name, map_1
    map_1 = '|    X    |' + map_1[12:]

    try:
        print "You're in " + woods_0_0_name + "!\n"
    except:
        woods_0_0_name = words.woods_name()
        print "You enter " + woods_0_0_name + "!\n"

    raw_input('Well-traveled paths lead north and south, ' + \
              'and darker, twisting paths lead east and west.\n\n' + \
              "There's also an odd-looking building in " + \
              "the distance. Maybe it's a tavern?")

    next = (
            ['woods_0_1','woods_1_0','woods_0_n1','woods_n1_0','tavern'],
            ["North","East","South","West","Tavern"]
            )

    return pick_place(next,'Where to next?')

def woods_0_1():
    """
    quieter, northern woods
    +---------+
    |    X    |
    |         |
    |         |
    +---------+
    """
    global woods_0_1_name,map_0
    map_0 = '|    X    |' + map_0[12:]
    try:
        raw_input("You enter " + woods_0_1_name + "!\n")
    except:
        woods_0_1_name = words.woods_name()
        raw_input("You enter " + woods_0_1_name + "!\n")

    monsta_here = round(random.random() -.2)
    if monsta_here:
        result = encounter_monster(['tiny_monsters'])
        if result == 'death':
            return result
    else:
        raw_input("Not much here.\n")

    next =  (
            ['woods_0_0','woods_1_1','woods_n1_1'],
            ["South","East","West"]
            )

    return pick_place(next,'Where to next?')

def woods_0_n1():
    """
    quieter, southern woods
    +---------+
    |         |
    |         |
    |    X    |
    +---------+
    """
    global woods_0_n1_name,map_2
    map_2 = '|    X    |' + map_2[12:]
    try:
        raw_input("You enter " + woods_0_n1_name + "!\n")
    except:
        
        woods_0_n1_name = words.woods_name()
        raw_input("You enter " + woods_0_n1_name + "!\n")
    monsta_here = round(random.random() -.2)
    if monsta_here:
        result = encounter_monster(['tiny_monsters','small_monsters'])
        if result == 'death':
            return result
    else:
        raw_input("Not much here.\n")
    next =  (
            ['woods_0_0','woods_1_n1','woods_n1_n1'],
            ["North","East","West"]
            )

    return pick_place(next,'Where to next?')  

def woods_1_0():
    """
    shady eastern woods
    +---------+
    |         |
    |       X |
    |         |
    +---------+
    """
    global woods_1_0_name,map_1
    map_1 = '|       X |' + map_1[12:]
    try:
        print "You enter " + woods_1_0_name + ".\n"
    except:
        
        woods_1_0_name = words.woods_name()
        print "You enter " + woods_1_0_name + ".\n"

    monsta_here = round(random.random() +.3)
    if monsta_here:
        result = encounter_monster(['small_monsters','medium_monsters'])
        if result == 'death':
            return result
    else:
        raw_input("There's a giant colosseum in the distance...\n")
    
    next = (
            ['woods_0_0','woods_1_1','woods_1_n1','arena'],
            ["West","North","South","Arena"]
            )

    return pick_place(next,'Where to next?')

def woods_1_1():
    """
    dangerous corner woods
    +---------+
    |       X |
    |         |
    |         |
    +---------+
    """
    global woods_1_1_name,map_0
    map_0 = '|       X |' + map_0[12:]
    try:
        raw_input("You enter " + woods_1_1_name + ".\n")
    except:
        
        woods_1_1_name = words.woods_name()
        raw_input("You enter " + woods_1_1_name + ".\n")
    monsta_here = round(random.random() + .4)
    if monsta_here:
        result = encounter_monster(['medium_monsters','large_monsters'])
        if result == 'death':
            return result
    else:
        raw_input("Not much here.\n")
    
    next = (
            ['woods_1_0','woods_0_1'],
            ["South","West"]
            )

    return pick_place(next,'Where to next?')

def woods_1_n1():
    """
    dangerous corner woods
    +---------+
    |         |
    |         |
    |       X |
    +---------+
    """
    global woods_1_n1_name,map_2
    map_2 = '|       X |' + map_2[12:]
    try:
        raw_input("You enter " + woods_1_n1_name + ".\n")
    except:
        
        woods_1_n1_name = words.woods_name()
        raw_input("You enter " + woods_1_n1_name + ".\n")
    monsta_here = round(random.random() + .4)
    if monsta_here:
        result = encounter_monster(['medium_monsters','large_monsters'])
        if result == 'death':
            return result
    else:
        raw_input("Not much here.\n")
    
    next = (
            ['woods_1_0','woods_0_n1'],
            ["North","West"]
            )

    return pick_place(next,'Where to next?')

def woods_n1_0():
    """
    shady western woods
    +---------+
    |         |
    | X       |
    |         |
    +---------+
    """
    global woods_n1_0_name,map_1
    map_1 = '| X       |' + map_1[12:]
    try:
        print "You enter " + woods_n1_0_name + ".\n"
    except:
        
        woods_n1_0_name = words.woods_name()
        print "You enter " + woods_n1_0_name + ".\n"

    raw_input("There's a giant colosseum in the distance...\n")

    monsta_here = round(random.random() +.3)
    if monsta_here:
        result = encounter_monster(['small_monsters','medium_monsters'])
        if result == 'death':
            return result
    else:
        raw_input("Hmm... something ominous is definitely lurking here...\n")
    
    next = (
            ['woods_0_0','woods_n1_1','woods_n1_n1','arena'],
            ["East","North","South","Arena"]
            )

    return pick_place(next,'Where to next?')

def woods_n1_1():
    """
    dangerous corner woods
    +---------+
    | X       |
    |         |
    |         |
    +---------+
    """
    global woods_n1_1_name,map_0
    map_0 = '| X       |' + map_0[12:]
    try:
        raw_input("You enter " + woods_n1_1_name + ".\n")
    except:
        woods_n1_1_name = words.woods_name()
        raw_input("You enter " + woods_n1_1_name + ".\n")
    monsta_here = round(random.random()+.4) #usually there's a monsta here
    if monsta_here:
        result = encounter_monster(['medium_monsters','large_monsters'])
        if result == 'death':
            return result
        question = 'You survived. Nice. Where to next?'
    else:
        raw_input("That's odd...\n")
        raw_input("There's usually a monster here.\n")
        question = "Oh well. Where to next?"

    next = (
            ['woods_n1_0','woods_0_1'],
            ["South","East"]
            )

    return pick_place(next,question)

def woods_n1_n1():
    """
    dangerous corner woods
    +---------+
    |         |
    |         |
    | X       |
    +---------+
    """
    global woods_n1_n1_name,map_2
    map_2 = '| X       |' + map_2[12:]
    try:
        raw_input("You enter " + woods_n1_n1_name + ".\n")
    except:
        woods_n1_n1_name = words.woods_name()
        raw_input("You enter " + woods_n1_n1_name + ".\n")
    monsta_here = 1 ###yep, there's always a monster here
    if monsta_here:
        result = encounter_monster(['medium_monsters','large_monsters'])
        if result == 'death':
            return result
    else:
        raw_input("Wait, what? nope nope nope you broke something, bro.\n")
    
    next = (
            ['woods_n1_0','woods_0_n1'],
            ["North","East"]
            )

    return pick_place(next,'Where to next?')

### tunnels ###

def main_tunnel():
    """
    you enter this tunnel from the arena
    """
    raw_input('The tunnel is dark, and water begins dripping on your head.\n')
    raw_input('There are several branching tunnels, one of which is covered in strange markings.\n')

### death ###

def death():
    """
    yolo
    """
    raw_input('YOUR HEAD AAAAASPLOOOOODE!\n')
    if not cheated:
        hiscores = helpful.hiscore(str(player),monsters_defeated)
    else:
        raw_input('cheaters never win\n')
        raw_input('#suxtosuck\n')
        hiscores = helpful.hiscore(str(player),0)

    raw_input(hiscores)

    return None

"""

places TODO:

    add new place functions above, make sure you update func_map you fool

    improve portal?
    improve bongos

    volcano

    escape arena with boss

    improve max health?
    improve damage

"""

########### leggo ###########

def rigorous():
    return 'lehmann'

def start_game():

    ###configure
    config.config()

    global press_enter, enter_two, enter_four
    global hardcore; hardcore = False
    global player
    global monsters_defeated
    global bongo_string

    global world_map #well I hope so
    global map_0
    global map_1
    global map_2

    global tavern_name
    global bartender_name
    global traveler_name
    global arena_boss
    global BORIS_CRED

    global cheated

    hardcore = False
    monsters_defeated = 0
    bongo_string = 'sevenya'

    world_map = False
    map_0 = '|         |    '
    map_1 = '|         |    '
    map_2 = '|         |    '

    tavern_name = ''
    bartender_name = ''
    traveler_name = ''
    arena_boss = ''
    BORIS_CRED = 0

    in_tavern = False
    cheated = False

    ### the story begins ###

    print('\n'*100) #clear screen

    print '          AVENTUREGAME!          \n'
    print '< use numbers/letters to choose >\n'
    press_enter = getpass.getpass( '<    press enter to continue    >\n' )
    print('\n'*100)

    if press_enter[0:4] =='yolo':
        hardcore = True
        cheated = True ###TODO remove this and make this actually do things, like double score, etc
        raw_input('<hardcore mode activated>\n')

    name = raw_input('Name?\n\n')
    if name == '':
        name = 'Nameless One'
    player = helpful.Player(name) #name character

    raw_input('\nWelcome, '+ str(player) +'!\n')
    print 'You are a poor orphan, determined to make your way in the world.\n'
    raw_input('You have nothing but the clothes on your back (which you stole) ' + \
              'and an odd-looking fruit.\n')
    raw_input("You've heard rumors of a giant, horrifying dragon terrorizing the " + \
              'land.\n\nIf you can defeat him, surely you will be remembered ' + \
              'as more than just a smelly, penniless orphan.\n')
    raw_input('Good luck!\n')

    print ('\n'*10)
    bag =      [
               items_lists.random_weapon('short_weapons'),
               items_lists.random_weapon('long_weapons'),
               helpful.Item('apple',50,0,5,1),
               helpful.Item('pizza',10,0,14.99,8),
               helpful.Item('laser',0,50,0,15)
               ]

    num_choices = 3
    while num_choices > 0:
        item = helpful.pick_item(bag,str(num_choices) + ' starting items left to choose!')
        bag.remove(item)
        player.grab(item)
        print 'You acquired a ' + str(item) + '.\n'
        num_choices -= 1

    raw_input('Let the adventure begin!\n')

    player.grab(helpful.Item('mythical kumquat',0,0,1000))
    enter_two = ''
    enter_four = ''

    next_location = 'woods' #start here
    
    while next_location: #the main journey loop! aaaaand we're off

        # raw_input('next up: ' + str(next_location) + '\n')
        next_location = visit(next_location)

if __name__ == '__main__':

    try:
        start_game()
    except:
        print '\nWe ran into an error.\n'
        print 'Admin will be notified.\n'
        logging.exception("AventureGameError:") #LOG


