"""
Some items for AVENTUREGAME 
""" 

import math
import random

import helpful
import words

master_weapons_dict = {

	'goofy_weapons':	[
						helpful.Item('Rusty Spoon',0,10),
						helpful.Item('Rusty Fork',0,10),
						helpful.Item('Rusty Knife',0,20)
						],

	'thrown_weapons':	[
						helpful.Item('Banana',0,15,None,1),
						helpful.Item('Artichoke',0,12,None,1),
						helpful.Item('Boomerang',0,13,None,1),
						helpful.Item('Rock',0,4,None,1)
						],

	'animal_weapons':	[
						helpful.Item('Fang',0,20),
						helpful.Item('Claw',0,20),
						helpful.Item('Tentacle',0,20)
						],

	'short_weapons':	[
						helpful.Item('Dagger',0,30),
						helpful.Item('Club',0,30),
						helpful.Item('Hammer',0,30),
						helpful.Item('Mace',0,30)
						],

	'long_weapons':		[
						helpful.Item('Warstaff',0,40),
						helpful.Item('Shovel',0,40,17),
						helpful.Item('Icepick',0,40),
						helpful.Item('Axe',0,35),
						helpful.Item('Trident',0,40)
						],

	'ranged_weapons':	[
					    helpful.Item('Crossbow',0,50),
					    helpful.Item('Longbow',0,50),
					    helpful.Item('Musket',0,65),
					    helpful.Item('Slingshot',0,25)
						],

	'power_weapons':	[
						helpful.Item('Bamboo Staff',0,60),
						helpful.Item('Katana',0,60),
						helpful.Item('Scythe',0,55),
						helpful.Item('Greatsword',0,60)
						]
	}

boss_weapons =			[
						helpful.Item('Fireball',0,100,None,40),
						helpful.Item('Scorch',0,100,None,40),
						helpful.Item('Didgeridoo',0,100,None,40)
						]

def random_weapon(category=None):

	#add support for dict or single thingo

	if not category:
		category = random.choice(master_weapons_dict.keys())
	if category == 'boss_weapons':
		weapons_list = boss_weapons
	else:
		weapons_list = master_weapons_dict[category]
	weapon = random.choice(weapons_list)

	damage_offset = random.randint(-10,10)
	damage = weapon.get_damage() + damage_offset

	cost = max(1,int(2**(damage/10.0+3)) + random.randint(-10,10))

	name = weapon.get_name()
	name = name.title()

	if 29 < damage:
		if damage < 49:
			name = words.weapon_adj() + ' ' + name
			name = name.title()
			# print '1: ',name
	if 49 < damage:
		if damage < 60:
			name = name.title() + ' ' + words.weapon_suffix()
			# print '2: ',name
	if 60 < damage:
		name = words.weapon_adj() + ' ' + name.title()
		name = name + ' ' + words.weapon_suffix()
		is_normal_weapon = random.randint(0,8)
		if not is_normal_weapon: #WOMBO COMBO
			name = words.prestige_weapon_adj().title() + ' ' + name
			damage += 20
			cost += int(2**(damage/10.0+3) + random.randint(0,100))
		# print '3: ',name

	new = weapon.copy(name,0,damage,cost)
	return new

###this list is in order of power
###each index +1 gives lots more health and lots more damage
master_monsters_dict = {

						#name, health, inventory list, loot
	
	'tiny_monsters':	[
						helpful.Being('Spider',40,[helpful.Item('Venom Sac',0,30)]),
						helpful.Being('Cat',35,[helpful.Item('Claw',0,20)]),
						helpful.Being('Rat',45,[helpful.Item('Claw',0,20)])
						],

	'small_monsters':	[ 
						helpful.Being('Goblin',50,None,30),
						helpful.Being('Hobgoblin',50,None,30),
						helpful.Being('Orc',55,None,35)
						],

	'medium_monsters':	[
						helpful.Being('Goop Monster',75,None,80),
						helpful.Being('Cave Troll',80,None,100),
						helpful.Being('Tiger',75,[helpful.Item('Tiger Fang',0,50)])
						],

	'large_monsters':	[
						helpful.Being('Mountain Troll',95,None,200),
						helpful.Being('Basilisk',100,[helpful.Item('Basilisk Fang',0,60,275)]),
						helpful.Being('Balrog',125,[helpful.Item('Flaming Whip',0,65,300),helpful.Item('Flaming Greatsword',0,70,300)],400)
						],

	'snow_monsters':	[
						helpful.Being('Demon Snowman',75,[helpful.Item('Icicle',0,40)]),
						helpful.Being('Snow Leopard',80,[helpful.Item('Leopard Fang',0,60)]),
						helpful.Being('Yeti',75,[helpful.Item('Massive Icicle',0,75)])
						]

	}

boss_list =				[
						helpful.Being('Goblin King',700,[
														 helpful.Item('Skull Staff',0,101)
														]),
						helpful.Being('Dragon',700),
						helpful.Being('Giant Kumquat Monster',700)
						]

def random_monster(choosefrom=None):
	"""
	takes a string, which is the monster category,
	or a list of strings, which are monster categories
	"""

	if not choosefrom:
		choosefrom = random.choice(master_monsters_dict.keys())

	if choosefrom == 'boss_monsters':
		monster_list = boss_list
	else:
		if isinstance(choosefrom,list):
			category = random.choice(choosefrom)
		elif isinstance(choosefrom,str):
			category = choosefrom
		else:
			print "<something went wrong, notify admin>\n"

		#will crash if input is wrong type
		monster_list = master_monsters_dict[category]
	
	monster = random.choice(monster_list)

	inventory_amount = 1
	if not random.randint(0,4):
		inventory_amount += 1
	if not random.randint(0,7):
		inventory_amount += 1
	new_inventory = []

	if not monster.get_inventory():

		while inventory_amount > 0:
			
			if category == 'tiny_monsters':
				weapon_category = random.choice(['goofy_weapons','thrown_weapons'])
			elif category == 'small_monsters':
				weapon_category = random.choice(['animal_weapons','short_weapons'])
			elif category == 'medium_monsters':
				weapon_category = random.choice(['long_weapons','ranged_weapons'])
			elif category == 'large_monsters':
				weapon_category = random.choice(['ranged_weapons','power_weapons'])
			elif category == 'boss_monsters':
				weapon_category = 'boss_weapons'
			
			if weapon_category == 'boss_weapons':
				weapon = random.choice(boss_weapons)
			else:
				weapon = random_weapon(weapon_category)

			new_weapon = weapon.copy()
			new_inventory.append(new_weapon)
			inventory_amount -= 1

	else:
		new_inventory = monster.get_inventory()

	new_health = monster.get_health() + random.randint(-5,5)
	new_monster = monster.copy(None,new_health,new_inventory)
	return new_monster

bartender_name_list = [
					   'Mysterious Bearded Man','Chuck Wagon','Merlin','Bob Ross','Harpo Dooblat','Squim Rigbo'
					   ]

def random_bartender_name():
	return random.choice(bartender_name_list)

npc_name_list = [
				 'Nustellan LaMetrons','Joe','Thorgood Trollsmash','Alfredo Berlosconinni','Mr. Rogers'
				 ]

def random_npc():
	return helpful.Being(random.choice(npc_name_list))

if __name__ == '__main__':

	for i in range(4):
		# r = random_weapon('thrown_weapons')
		# print r.advanced_str() + '\n'
		monster = random_monster()
		print monster.advanced_str()




