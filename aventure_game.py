#!/usr/bin/env python
"""

AVENTUREGAME

"""

import logging #LOG: uncomment all lines containing this comment to enable error logging to a file
logging.basicConfig(level=logging.DEBUG, filename='debug.log') #LOG

########### imports n stuff ###########

import random
import getpass
import config
import hashlib
import cPickle as pickle

########### desktop/programs/python ###########

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
	enemy = items_lists.random_monster(who_fight)

    else:
	###else picks a monster at random, not boss though
	enemy = items_lists.random_monster()

    if debug:
	print '<\n\nfighting:\n' + enemy.advanced_str() +'\n>\n'


    encountered = str(enemy)
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
	    if defend > 0:
		raw_input('You gained ' + str(defend) + ' HP!')
	    if attack == 0 and defend == 0:
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
	print '\n'.join([player.get_name() + ' ' + player.get_title(), \
			  '='*len(player.get_name() + ' ' + player.get_title()), \
			  'Health: ' + str(player.get_health())])
	while choice != 'done':
	    choices = list(player.get_inventory())
	    choices += ['done']
	    intro = '\nType item name/number for more info...\n\nInventory:'
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
	print ' 	       +---------+'
	print '    ' + map_0
	print '    ' + map_1
	print '    ' + map_2
	print ' 	       +---------+'
	raw_input('')

    else:
	raw_input('You have no world map :(')
    return

def pick_place(choices_arg, question='Where to next?',inv=True):
    """
    pretty much identical to pick_item. at least, it started that way.
    break_before breaks before inventory
    """
    original_question = question

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

	if debug:

	    if chosen[0:4] == "loc ":
		raw_input("<debug jumping...>\n")
		return chosen[4:]
	    elif chosen[0:5] == "fight":
		raw_input("<debug fighting...>\n")
		encounter_monster()
		continue

	    elif chosen[0:5] == "money":

		try:
		    gained = int(chosen[6:])
		except:
		    gained = 100

		player.gain_money(gained)
		raw_input("<debug money+" + str(gained) + ">\n")
		continue

	    elif chosen[0:6] == "health":

		try:
		    gained = int(chosen[7:])
		except:
		    gained = 100

		player.gain_health(gained)
		raw_input("<debug health+" + str(gained) + ">\n")
		continue

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
	    if question == 'Where to next?':
		question = 'Where to?'
	    else:
		question = original_question
	    staying = True
	if final == 'inventory':
	    inspect_inventory()
	    if question == 'Where to next?':
		question = 'Where to?'
	    else:
		question = original_question
	    staying = True

    return final

########### journeying ###########

def visit(location):
    """
    this function (and every function after it in this section)
    should return a string name of the next place to visit

    dying is no return
    """
    if debug:
	print "<visiting " + str(location) + ">\n"

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
    map_0 = map_0[:12] + '|	    |' + map_0[24:]
    map_1 = map_1[:12] + '|	    |' + map_1[24:]
    map_2 = map_2[:12] + '|	    |' + map_2[24:]

    locations_list = func_map.keys()

    if location not in locations_list:

	try:
	    func = eval(location)
	except:
	    print '<invalid location>\n'

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
    |	      |
    |	 T    |
    |	      |
    +---------+
    """
    global tavern_name
    global bartender_name
    global press_enter, enter_two, enter_four

    global map_1
    map_1 = map_1[:12] + '|    T    |' + map_1[24:]

    if not tavern_name:
	tavern_name = 'The ' + words.tavern_adj().capitalize() + ' ' + \
		      words.noun().capitalize() + ' Tavern'
	bartender_name = items_lists.random_bartender_name()
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
		['beer','buy map','buy','sell','mirror','box','woods','improve_weapons'],
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
	elif next == 'improve_weapons':
	    improve_weapons()
	else:
	    return next

	raw_input('You return to the bar.\n')
	raw_input('The bartender winks at you.\n')

def beer():
    """
    should only be called from in the tavern
    """
    global cheated, enter_four

    if enter_four == config.confus(config.config4):
	player.grab(helpful.Item('SixPack',17,0,0,6))
	cheated = True
	print '<achievement unlocked>\n'
	enter_four = ''

    if player.get_money() >= 100:

	player.gain_health(17)
	player.lose_money(17)

	raw_input('You take out your money.\n')
	raw_input(words.possesivize(bartender_name) + " eyes widen at your stack of bills.\n")
	raw_input('"I guess we have this stuff, if you really need a drink."\n')

	raw_input("The 'beer' healed you a bit.\n")
	raw_input('It also cost $17.\n')

    else:
	print bartender_name + ' chuckles and looks pointedly at his empty tip jar.\n'
	raw_input('"' +"Beer's expensive, kid." + '"\n')
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

def improve_weapons():
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
	    choice = helpful.pick_item(["$100","$10","Haha. No."],"Donate to Boris?")
	    if choice == "$100":
		if player.get_money() > 100:
		    player.lose_money(100)
		    BORIS_CRED += 50
		else:
		    BORIS_CRED -= 10
		    raw_input("Yikes. You don't have that much. Oops. Boris is a little sad.\n\nHe agrees to help you though.\n")
	    elif choice == "$10":
		if player.get_money() > 10:
		    player.lose_money(10)
		    BORIS_CRED += 2
		else:
		    BORIS_CRED -=2
		    raw_input("Yikes. You don't have that much. Oops. Boris is a little sad.\n\nHe agrees to help you though.\n")
	    else:
		BORIS_CRED -= 10
    else:
	raw_input('"WELL THEN. GOODBYE."\n')
	BORIS_CRED -= 5
	return

    improve = "poop"
    while improve != "Done":
	improve = helpful.pick_item(player.get_inventory() + ['"Never mind, I want a refund."'],'"WHAT WOULD YOU LIKE TO IMPROVE?"\n')
	if improve == '"Never mind, I want a refund."':
	    raw_input('"NO REFUNDS."\n')
	    BORIS_CRED -= 1
	    continue
	if BORIS_CRED > 900000:
	    incd = 100
	elif BORIS_CRED > 100:
	    incd = 10
	else:
	    incd = 4

	if improve.get_damage() > 0:
	    improve.inc_damage(incd)
	    which = "DAMAGE"
	elif improve.get_health() > 0:
	    improve.inc_health(incd)
	    which = "HEALTH"
	else:
	    raw_input("UM. NOPE. PICK SOMETHING ELSE.\n")

	print '"OKAY, I IMPROVED YER ' + str(improve).upper() + ' BY ' + str(incd) + ' POINTS OF ' + (which) + '."\n'
	raw_input(improve.advanced_str())
	raw_input('\n"YOU' + "'" + 'RE WELCOME."\n')
	improve = "Done" #break

def traveler():
    """
    TODO: getts the traveler?
    """
    raw_input('A wizened old traveler\n')\

def advice():
    """
    TODO
    """
    raw_input('A sign on the counter reads: "Advice $1".\n')
    raw_input('The bartender leans in close and whispers:\n')
    # raw_input('...\n')
    raw_input('"There is an old man hidden in the forest. You must talk to him."\n')
    # return 'tavern'

def old_man_hut():
    """
    TODO
    """
    raw_input('You are suddenly transported inside a small hut, seemingly made of bamboo.\n')
    raw_input("There's a teakettle on the stove, and some fresh cookies on a plate in front of you.\n")
    raw_input("Suddenly, a crazy old man rushes in and stabs you.\n")
    return 'death'

### cool places ###

def arena():
    """
    location
    arena where you fight until you die hahahaha
    """
    global monsters_defeated, arena_boss

    if not arena_boss:
	arena_boss = items_lists.random_monster('boss_monsters')
	if debug:
	    print '<arena boss = ' + str(arena_boss) + '>\n'

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

    while next_bongo == 'poop':
	#if we enter a valid code (or press done), we leave this loop
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

	if bongo_code_8 == '25746c694387e5114dbb3b99fb9aeb5c':
	    raw_input('Something is rustling in the bushes.\n')
	    raw_input('You pull some weeds aside to reveal an enormous, rusty cage.\n')
	    raw_input("There's a pretty mean-looking bull inside. Thankfully, he's asleep.\n")
	    raw_input("Don't touch the cage, though.\n")
	    touch = pick_item((["y","n"],["Touch it!","Don't touch it!"]),"Touch it?")
	    if touch == "y":
		return 'old_man_hut'
	    else:
		raw_input('Good choice.\n')

	elif bongo_code_8 == 'da07700b3beac79629b0648855c9d165':
	    player.grab(helpful.Item('Raw Meat',0,12,7))
	    raw_input('Some raw meat falls from a tree! Yummy!\n')

	elif bongo_code_7 == 'b3188adab3f07e66582bbac456dcd212':
	    player.grab(helpful.Item('Cabbage',5,0,3,1))
	    raw_input('A plant appears!\n')
	elif bongo_code_7 == '54a28e933e22fbabf29e267dd3f5c908':
	    raw_input('A giant computer appears!\n')
	    raw_input("No, really, it's like the size of your house. No idea how you're going to carry that.\n")
	    player.grab(helpful.Item('Massive Computer',0,0,5000))
	elif bongo_code_6 == '50b845418f04cc6ff299ab3de28261fa':
	    raw_input('Your ' + str(item) + " glows with a pulsating green light.\n\nIt's been improved!")
	    """TODO IMPROVE THAT"""

	else:
	    next_bongo = "poop" #keep playing those bongos!

	# print 'bongocode',bongo_code_6,bongo_code_8
	# print 'bongostring',bongo_string


    raw_input("You leave the mystical bongo circle, but to your amazement, " + \
	      "the sky is a bizarre green color, and the woods have shifted around you.\n")
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
    |	      |
    |	 X    |
    |	      |
    +---------+
    """
    global woods_0_0_name, map_1
    map_1 = map_1[:12] + '|    X    |' + map_1[24:]

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
    |	 X    |
    |	      |
    |	      |
    +---------+
    """
    global woods_0_1_name,map_0
    map_0 = map_0[:12] + '|    X    |' + map_0[24:]
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
    |	      |
    |	      |
    |	 X    |
    +---------+
    """
    global woods_0_n1_name,map_2
    map_2 = map_2[:12] + '|    X    |' + map_2[24:]
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
    |	      |
    |	    X |
    |	      |
    +---------+
    """
    global woods_1_0_name,map_1
    map_1 = map_1[:12] + '|	  X |' + map_1[24:]
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
    |	    X |
    |	      |
    |	      |
    +---------+
    """
    global woods_1_1_name,map_0
    map_0 = map_0[:12] + '|	  X |' + map_0[24:]
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
    |	      |
    |	      |
    |	    X |
    +---------+
    """
    global woods_1_n1_name,map_2
    map_2 = map_2[:12] + '|	  X |' + map_2[24:]
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
    |	      |
    | X       |
    |	      |
    +---------+
    """
    global woods_n1_0_name,map_1
    map_1 = map_1[:12] + '| X	    |' + map_1[24:]
    try:
	print "You enter " + woods_n1_0_name + ".\n"
    except:

	woods_n1_0_name = words.woods_name()
	print "You enter " + woods_n1_0_name + ".\n"

    raw_input("Uh oh...\n")

    monsta_here = round(random.random() +.3)
    if monsta_here:
	result = encounter_monster(['small_monsters','medium_monsters'])
	if result == 'death':
	    return result
    else:
	print "You smell smoke, and a faint whiff of burning flesh.\n"
	print "There's a giant mountain in the distance. It looks pretty climbable.\n"
	raw_input("Something ominous is definitely lurking here, though...\n")

    next = (
	    ['woods_0_0','woods_n1_1','woods_n1_n1'], #TODO ,'mountain_base'],
	    ["East","North","South"] # TODO,"Mountain"]
	    )

    return pick_place(next,'Where to next?')

def woods_n1_1():
    """
    dangerous corner woods
    +---------+
    | X       |
    |	      |
    |	      |
    +---------+
    """
    global woods_n1_1_name,map_0
    map_0 = map_0[:12] + '| X	    |' + map_0[24:]
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
    |	      |
    |	      |
    | X       |
    +---------+
    """
    global woods_n1_n1_name,map_2
    map_2 = map_2[:12] + '| X	    |' + map_2[24:]
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

    next = (
	    ['tunnel_0','tunnel_1','tunnel_strange'],
	    ['Left branch','Right branch','Strange markings']
	    )

    return pick_place(next,'Which tunnel?')

def tunnel_0():
    """
    you enter this tunnel from main_tunnel
    """
    print "TODO TUNNEL 0"
    return 'main_tunnel'

def tunnel_1():
    """
    you enter this tunnel from main_tunnel
    """
    print "TODO TUNNEL 1"
    return 'main_tunnel'

def tunnel_strange():
    """
    you enter this tunnel from main_tunnel
    """
    print "TODO TUNNEL S"
    return 'main_tunnel'

def tunnel_maze_0():
    """
    you enter this tunnel from a hole in the ground
    """
    #raw_input('This tunnel is completely dark and incredibly small, cramped, and narrow.\n')
    raw_input('You feel around for a way out.\n')
    out = random.shuffle(['tunnel_maze_1','tunnel_maze_2'])

    next = (
	    out,
	    ['crawl left', 'crawl right']
	    )

    return pick_place(next,'Which tunnel?')

def tunnel_maze_1():
    """
    you enter this tunnel from a hole in the ground
    """
    raw_input('This tunnel is completely dark and incredibly small, cramped, and narrow.\n')
    raw_input('You feel around for a way out.\n')
    out = random.shuffle(['tunnel_maze_0','tunnel_maze_2'])

    next = (
	    out,
	    ['crawl left', 'crawl right']
	    )

    return pick_place(next,'Which tunnel?')

def tunnel_maze_2():
    """
    you enter this tunnel from a hole in the ground
    """
    raw_input('This tunnel is completely dark and incredibly small, cramped, and narrow.\n')
    raw_input('You feel around for a way out.\n')
    out = random.shuffle(['tunnel_maze_0','tunnel_maze_1'])

    next = (
	    out,
	    ['crawl left', 'crawl right']
	    )

    return pick_place(next,'Which tunnel?')

def tunnel_maze_central():
    """
    you enter this tunnel from a hole in the ground
    """
    raw_input('This tunnel is completely dark and incredibly small, cramped, and narrow.\n')
    raw_input('You feel around for a way out.\n')
    out = random.shuffle(['tunnel_maze_0','tunnel_maze_1'])

    next = (
	    out,
	    ['crawl left', 'crawl right']
	    )

    return pick_place(next,'Which tunnel?')

### mountains ###

def mountain_base():
    """
    you enter the mountain base from woods_n1_0
		+---------+
		|	  |
	       X|	  |
		|	  |
		+---------+

    """
    global map_1; map_1 = map_1[:11] + 'X' + map_1[12:]

    print "Yikes, this mountain is huge.\n"
    raw_input("You might be able to climb it, but it will be dangerous.\n")

    next = (
	    ['woods_n1_0','mountain_1'],
	    ["Back to the woods","Onwards"]
	    )

    go_here = pick_place(next,'Climb time?')

    map_1 = map_1[:11] + ' ' + map_1[12:]

    return go_here

def mountain_1():
    """
    up from mountain_base
		+---------+
	      ^ |	  |
	      X |	  |
	      ^ |	  |
		+---------+

    """
    global map_0; map_0 = map_0[:10] + '^' + map_0[11:]
    global map_1; map_1 = map_1[:10] + 'X' + map_1[11:]
    global map_2; map_2 = map_2[:10] + '^' + map_2[11:]

    raw_input("Giant, impassable snowy peaks tower over you.\n")
    raw_input("The snow soaks through your thin boots, and a cold wind chills your bones.\n")
    raw_input("Going north or south is virtually impossible.\n")

    next = (
	    ['back','forwards'],
	    ["Turn back","Wearily trudge onwards"]
	    )

    go_here = pick_place(next,'Continue on this perilous journey?')

    if go_here == 'back':
	raw_input("You return to the woods bloodied and tired. That mountain really took a toll on you.\n")
	player.set_health(round(player.get_health*.9))
	go_here = 'woods_n1_0'
    else:
	raw_input("You perish in the snow.\n")
	go_here = 'death'

    map_1 = map_1[:10] + ' ' + map_1[11:]

    return go_here

### death ###

def death():
    """
    yolo
    """
    raw_input('YOUR HEAD AAAAASPLOOOOODE!\n')

    if cheated:
	raw_input('cheaters never win\n')
	raw_input('suxtosuck\n')
	hiscores = helpful.hiscore(str(player),0)
    else:
	if debug:
	    hiscores = helpful.hiscore("<debug>",0)
	else:
	    hiscores = helpful.hiscore(str(player),monsters_defeated)

    raw_input(hiscores)

    return None

"""

places TODO:

    organize tavern. make town -> tavern? then we can have other buildings in town. yeah. sounds good.

    improve portal? make it go cool places, not just hard places.
    improve bongos

    volcano
	descend into underworld?

    tunnel maze

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
    global debug; debug = False
    global monsters_defeated; monsters_defeated = 0;
    global bongo_string; bongo_string = 'sevenya'

    global world_map #well I hope so
    world_map = False
    global map_0; map_0 = '		|	  |    '
    global map_1; map_1 = '		|	  |    '
    global map_2; map_2 = '		|	  |    '

    global tavern_name; tavern_name = ''
    global bartender_name; bartender_name = ''
    global traveler_name; traveler_name = ''
    global arena_boss; arena_boss = ''
    global BORIS_CRED; BORIS_CRED = 0

    global cheated; cheated = False
    global in_tavern; in_tavern = False

    ### the story begins ###

    print('\n'*100) #clear screen

    print '	     AVENTUREGAME!	    \n'
    print '< use numbers/letters to choose >\n'
    press_enter = getpass.getpass( '<	 press enter to continue    >\n' )
    print('\n'*100)

    if press_enter[0:4] =='yolo':
	hardcore = True ###TODO remove this and make this actually do things, like double score, etc
	cheated = True
	raw_input('<hardcore mode activated>\n')

    name = raw_input('Name?\n\n')
    if name == '':
	name = 'Nameless One'
    if name == 'debug':
	name = 'Valiant Beta Tester'
	print "<debug mode activated>\n"
	debug = True

    player = helpful.Player(name) #name character

    if debug:
	print "Helpful debug commands:\n\n"
	print "money int\nhealth int\nloc place\nfight\n\n"
	raw_input("\n")

    else:
	raw_input('\nWelcome, '+ str(player) +'!\n')
	raw_input('You wake up slightly dizzy and very thirsty. You are sitting on a dirt path.\n')
	raw_input('You have no idea how you got here, or even who you are.\n')
	raw_input('The last thing you remember is an old man telling you...\n')
	raw_input("Telling you...\n")
	raw_input("Wow, you really can't remember anything. Your head hurts a lot.\n")
	raw_input("You can't remember exactly what he told you. Something about dragons.\n")
	raw_input("There's a weird fruit next to you. It has a note on it:\n")
	raw_input("  MYTHICAL KUMQUAT\n" + \
		  "		     \n" + \
		  "  (do not lose me)\n")
	raw_input("There's also a basket of supplies. You should take some.\n")

    print ('\n'*10)

    bag =      [
	       items_lists.random_weapon('short_weapons'),
	       items_lists.random_weapon('short_weapons'),
	       items_lists.random_weapon('short_weapons'),
	       items_lists.random_weapon('long_weapons'),
	       items_lists.random_weapon('long_weapons'),
	       helpful.Item('laser',0,50,0,12)
	       ]

    random.shuffle(bag)
    num_choices = 1
    if not hardcore:
	num_choices = 3

    while num_choices > 0:
	text = str(num_choices) + ' starting weapons left to choose!'
	if num_choices == 1:
	    text = 'Last one!'
	item = helpful.pick_item(bag,text)
	bag.remove(item)
	player.grab(item)
	print 'You acquired a ' + str(item) + '.\n'
	num_choices -= 1

    if not hardcore:
	bag =  [
	       helpful.Item('apple',50,0,5,1),
	       helpful.Item('pizza',10,0,14.99,8),
	       helpful.Item('turnip',28,0,2,1)
	       ]
	item = helpful.pick_item(bag,'Now choose a foodstuff!')
	player.grab(item)

    raw_input('Let the adventure begin!\n')

    player.grab(helpful.Item('mythical kumquat',0,0,1000))
    enter_two = ''
    enter_four = ''

    next_location = 'woods' #start here

    while next_location: #the main journey loop! aaaaand we're off

	# raw_input('next up: ' + str(next_location) + '\n')
	next_location = visit(next_location)

if __name__ == '__main__':

    while 1:
	try:
		start_game()
	except:
	    print '\nWe ran into an error.\n'
	    print 'Admin will be notified.\n'
	    logging.exception("AventureGameError:") #LOG

	choice_count = 0
	choice = "n"
	choices = (["y","n"],["yes","no"])
	question = "Play again? (y/n)"

	while choice == "n":
	    choice_count += 1
	    choice = helpful.pick_item(choices,question)
	    if choice_count < 3:
		question = "No, really.\n"
	    elif choice_count < 7:
		question = "I'm serious. Play again.\n"
	    elif choice_count < 15:
		question = "Just press yes.\n"
	    elif choice_count < 25:
		question = "Please.\n"
	    elif choice_count < 35:
		question = "Stop it.\n"
	    elif choice_count < 45:
		question = "You're the worst kind of person.\n"
	    elif choice_count < 46:
		question = "Do you want to not play again?\n"
		choices = (["n","y"],["yes","no"])
	    elif choice_count < 47:
		raw_input("Listen.\n\nYou need to quit being so immature.\n")
		question = "Wow"
		choices = (["n","n"],["poop","poop"])
	    else:
		question+= "w"
