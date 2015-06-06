"""
Some helpful classes and functions and stuff for AVENTUREGAME 
"""

import operator
import random
import json

class Being:

    def __init__(self,name,health=100,inventory=[],money=0,score=1):
        self.name = name #str
        self.health = health #int
        self.inventory = inventory #list of Item objects
        self.money = money #ca$h monies
        self.score = 1;

    def __str__(self):
        return str(self.name)

    def copy(self,new_name=None,new_health=None,new_inv=None,new_money=None):
        """
        returns a deepcopy of the being, optionally renames n stuff
        """
        if not new_name:
            new_name = self.get_name()
        if not new_health:
            new_health = self.get_health()
        if not new_inv:
            new_inv = [item.copy() for item in self.get_inventory()]
        if not new_money:
            new_money = self.get_money()
        new = Being(new_name,new_health,new_inv,new_money)
        return new

    def get_name(self):
        return self.name

    def set_name(self,new_name):
        self.name = new_name
    
    def get_health(self):
        return self.health

    def set_health(self,num):
        self.health = num

    def gain_health(self,amount):
        self.health += amount

    def lose_health(self,amount):
        self.health -= amount

    def get_money(self):
        return self.money

    def set_money(self,money):
        self.money = money

    def gain_money(self,amount):
        self.money += amount

    def lose_money(self,amount):
        self.money -= amount

    def set_score(self,score):
        self.score = score

    def get_score(self,score):
        return self.score

    def gain_score(self,score):
        self.score += score

    def lose_score(self,score):
        self.score -= score

    def use(self,item,times=1):
        """
        they get to cheat, no use checks
        """
        item.use(times)

    def hit(self,item):
        self.lose_health(item.get_damage())

    def get_inventory(self):
        return self.inventory

    def get_inv_string(self):
        inv_string = ''
        for index in range(len(self.inventory)):
            inv_string += '  ' + str(self.inventory[index]) + '\n'
        return inv_string

    def grab_items(self,items):
        '''takes a list of Item objects'''
        map(self.inventory.append,items)

    def drop_items(self,items):
        '''takes a list of Item objects'''
        for index in range(len(items)):
            if items[index] in self.inventory:
                self.inventory.remove(items[index])
            else:
                print("oops oops, you don't have a "+str(items[index]))

    def grab(self,item):
        '''takes one Item object'''
        self.inventory.append(item)

    def drop(self,item):
        '''takes one Item object'''
        if item in self.inventory:
            self.inventory.remove(item)
        else:
            print("oops, you don't have a " + str(item))

    def advanced_str(self):
        return(self.name + '\n' \
                         + '='*len(self.name) + '\n' \
                         + 'Health: ' + str(self.get_health()) + '\n' \
                         + 'Inventory:' + '\n' \
                         + self.get_inv_string()
               )

class Player(Being):

    def __init__(self,name,health=100,inventory=[],money=0,score=0):

        self.title = 'the Worthless'
        self.name = name #str
        self.health = health #int
        self.inventory = inventory #list of Item objects
        self.money = money #get dat money
        self.score = 0;

    # def get_attr(self,attr): ###perhaps
    #     return self.attrs[attr]

    # def set_attr(self,attr,change):
    #     self.attrs[attr] = change

    # def gain_attr(self,attr,amount):
    #     self.attrs[attr] += amount

    # def lose_attr(self,attr,amount):
    #     self.attrs[attr] -= amount

    def get_title(self):
        return self.title

    def set_title(self,title):
        self.title = title


    def use(self,item,times=1):
        if item.get_health() > 0:
            self.gain_health(item.get_health())
        item.use(times)
        raw_input('You used your ' + str(item) + '.\n')
        if item.get_uses_left() <= 0:
            if str(item).lower() == 'boomerang':
                raw_input("That ain't coming back...\n")
            else:
                raw_input('Your ' + str(item) + ' is out of uses!\n')
            self.drop(item)
        

    def advanced_str(self):
        return('\n'.join([self.name + ' ' + self.title, \
                          '='*len(self.name + ' ' + self.title), \
                          'Health: ' + str(self.get_health()), \
                          'Money: $' +str(self.get_money()), \
                          'Inventory:', self.get_inv_string()]
                          )
                )

class Item:

    def __init__(self,name,health=0,damage=10,cost=None, uses_left=None):
        self.name = name
        self.health = max(0,health)
        if health:
            self.damage = 0
            if not cost:
                self.cost = max(1,int(2**(health/15.0+3)) + random.randint(-10,10))
            else:
                self.cost = cost
        else:
            self.damage = max(0,damage)
            if not cost:
                self.cost = max(1,int(2**(damage/10.0+3)) + random.randint(-10,10))
            else:
                self.cost = cost

        if uses_left:
            self.uses_left = uses_left
        else:
            self.uses_left = float('Inf')

    def __str__(self):
        return self.name

    def copy(self,new_name=None,new_health=None,new_damage=None,new_cost=None,new_uses=None):
        """
        optionally re-init
        """
        if not new_name:
            new_name = self.get_name()
        if not new_health:
            new_health = self.get_health()
        if not new_damage:
            new_damage = self.get_damage()
        if not new_cost:
            new_cost = self.get_cost()
        if not new_uses:
            new_uses = self.get_uses_left()
        new = Item(new_name,new_health,new_damage,new_cost,new_uses)
        return new

    def advanced_str(self):

        if self.get_uses_left() == float('Inf'):
            uses_line = 'Uses: infinite'
        else:
            uses_line = 'Uses: ' + str(self.get_uses_left()) +' remaining'

        return('\n'.join([self.get_name(), \
                          '='*len(self.get_name()), \
                          'Health: ' + str(self.get_health()), \
                          'Damage: ' + str(self.get_damage()), \
                          'Cost: $' + str(self.get_cost()), \
                          uses_line
                          ]))

    def use(self,times=1):
        if self.uses_left != float('Inf'):
            self.uses_left -= times

    def get_health(self):
        return self.health

    def set_health(self,health):
        self.health = health

    def get_name(self):
        return str(self.name)

    def set_name(self,new_name):
        self.name = new_name

    def get_damage(self):
        return self.damage

    def set_damage(self,damage):
        self.damage = damage

    def inc_damage(self,increase):
        self.damage += increase

    def get_cost(self):
        return self.cost

    def set_cost(self,cost):
        self.cost = cost

    def get_uses_left(self):
        return self.uses_left

    def set_uses_left(self,uses_left):
        self.uses_left = int(uses_left)

def pick_item(choices_arg, question='Which one?',break_before=None):
    """
    hmmm
    """
    
    choices_alt = []
    
    if isinstance(choices_arg,list):
        choices = choices_arg
    
    elif isinstance(choices_arg,tuple):
        choices = choices_arg[0]
        choices_alt = choices_arg[1]

    staying = True

    while staying:
    
        print question + '\n'

        if choices_alt:
            for index in range(len(choices_alt)): #print alternate choices in menu form
                if str(choices_alt[index]) == break_before:
                    print
                print(str(index+1) + ': ' + str(choices_alt[index]))

        else:
            for index in range(len(choices)): #print choices in menu form
                if str(choices[index]) == break_before:
                    print
                print(str(index+1) + ': ' + str(choices[index]))

        print('') #get some blank line in here yo
        chosen = raw_input('').lower()

        # global debug ###TODO MAKE THIS WORK
        # if debug:
        #     if chosen[0:5] == "money":
        #         raw_input("<debug money+100>\n")
        #         player.gain_money(100)
        #         continue
        #     elif chosen[0:6] == "health":
        #         raw_input("<debug health+100>\n")
        #         player.gain_health(100)
        #         continue
        
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
                    item = str(choices_alt[index]).lower()
                    item2 = str(choices[index]).lower()
                    if chosen == item or chosen == item2:
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

    return final

def hiscore(new_name,new_score):

    try:
        pairs = json.load(open("hiscores.txt", "rb"))
    except:
        pairs = [["Gutis", 54], ["jcho", 8], ["The Superior John", 8], ["Katana", 7], ["Batman", 55]]

    if new_name != "<debug>":
        pairs = [[new_name,new_score]] + pairs

    pairs = sorted(pairs,key=operator.itemgetter(1)) #sort by score
    pairs.reverse()
    pairs = pairs[:min(len(pairs),30)] #if we get to 10 (no, how about 30) we start bumping people off!

    hiscore_string = ''
    for idx in range(len(pairs)):
        hiscore_string += '{0:25} ... {1:10d}\n'.format(pairs[idx][0], pairs[idx][1])

    json.dump(pairs, open("hiscores.txt", "wb"))

    return hiscore_string

if __name__ == '__main__':

    bobbo = Player('bob')
    dagz = Item('plum',60,0,None,2)
    print dagz.advanced_str()

    chico = Being('',50,[dagz])

    print hiscore('Kenny',4)

