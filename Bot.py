import random
import Actions
def cut(num, max_num = 63, min_num = 0):
    if num > max_num:
        return num - max_num - 1
    elif num < min_num:
        return num + max_num + 1
    else:
        return num

class Organic:
    def __init__(self, life = 5000000):
        self.life = life
    
    def __str__(self):
        return str([self.life])
    
    def turn(self):
        self.life -= 1
        if self.life == 0:
            return 'die'
        else:
            return ''

class Bot:
    def __init__(self, genes = '', sun_level = 3, curr_action = 0, energy = 25, direction = 1, minerals_level = 0):
        
        self.genes = list(genes)
        if genes == '':
            for i in range(64):
                self.genes.append(25)
        
        self.minerals_level = 3
        self.aggressiveness = 0
        self.max_difference = 1
        self.passive_energy_drain = 5
        self.current_action = curr_action
        self.sun_level = sun_level
        self.energy = energy
        self.direction = direction
        self.minerals_level = minerals_level

    def __str__(self):
        info = []
        info.append(self.genes)
        info.append([])
        info[1].append(self.sun_level)
        info[1].append(self.current_action)
        info[1].append(self.energy)
        info[1].append(self.direction)
        return str(info)
    
    def __eq__(self, other):
        difference = 0
        for i in range(len(self.genes)):
            if self.genes[i] != other.genes[i]:
                difference += 1
        if difference <= self.max_difference:
            return True
        else:
            return False
    
    def mutate(self):
        self.genes[random.randint(0,63)] = random.randint(0,63)
           
    def action(self):
        directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
        action = Actions.actions
        if self.energy > 250:
            self.energy -= 200
            return ['budd_otn', self.genes[cut(self.current_action + 1)], self.direction, self.genes, self.sun_level, 0, 25, self.direction]
        elif self.energy < 0:
            return ['die']
        
        for i in range(len(action)):
            if self.genes[self.current_action] >= action[i]['min_num'] and self.genes[self.current_action] <= action[i]['max_num']:    
                if action[i]['name'] == 'photosynthesis':
                    self.energy += self.sun_level * action[i]['energy']
                elif action[i]['name'] == 'get_minerals':
                    self.energy += self.minerals_level * action[i]['energy']
                else:
                    self.energy += action[i]['energy']
                    
                
                if action[i]['name'] == 'turn_otn':
                    self.set_direction(self.genes[cut(self.current_action + 1)] % 8, True)
                elif action[i]['name'] == 'turn_abs':
                    self.set_direction(self.genes[cut(self.current_action + 1)] % 8, False)
                elif action[i]['name'] == 'action++':
                    self.jump_action(self.genes[self.current_action])
                elif action[i]['name'] == 'how_much_energy':
                    if self.energy > self.genes[cut(self.current_action + 1)] * 3:
                        self.receive_jump_action(2)
                    else:
                        self.receive_jump_action(1)
                elif action[i]['name'] == 'eat_otn' or action[i]['name'] == 'eat_abs':
                    self.aggressiveness = 20
                return [action[i]['name'], directions[cut(self.direction, 7, 0)], self.genes[cut(self.current_action + 1)], self.direction]
                    
    def jump_action(self, num):
        self.current_action += num
        self.current_action = cut(self.current_action)
    
    def receive_jump_action(self, num):
        self.jump_action(self.genes[cut(self.current_action + num)])
        
    def set_direction(self, num, add = False):
        if add:
            self.direction = cut(self.direction + num, 7, 0)
        else:
            self.direction = num
    
    def add_energy(self, energy, set_ = False):
        if set_:
            self.energy = energy
        else:
            self.energy += energy

    def reduce_aggressiveness(self):
        if self.aggressiveness > 0:
            self.aggressiveness -= 1
    
    def change_energy_sources(self, sun_level = 3, minerals_level = 3):
        self.sun_level = sun_level
        self.minerals_level = minerals_level
    
    def get_energy(self):
        return self.energy

