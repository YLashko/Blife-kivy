import Bot
import Actions
import random
from noise_generator import cut_noise, ret_min_map, ret_sun_map, AA, round_, inc_contrast, create_noise
directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
default_stats = {'bots':0, 'aggressiveness':0, 'green':0, 'blue':0, 'energy':0, 'deaths':0, 'born':0, 'looks':0, 'shares':0, 'turns':0, 'moves':0}
def cut(num, max_num = 7, min_num = 0):
    if num > max_num:
        return num - max_num - 1
    elif num < min_num:
        return num + max_num + 1
    else:
        return num

class Map:
    def __init__(self, size = (180,120), sun_level = 12):
        self.size = size
        self.sun_level = sun_level
        self.stats = default_stats
        self.new(self.size, self.sun_level)

    def spawn_bot(self, position, genes = '', sun_level = 3, curr_action = 0, energy = 25, direction = 1):
        self.map[position[0]][position[1]] = Bot.Bot(genes, sun_level, curr_action, energy, direction)

    def main_cycle(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if type(self.map[x][y]) == Bot.Bot:
                    if self.recording:
                        self.stats['bots'] += 1
                        self.stats['energy'] += self.map[x][y].get_energy()
                        self.stats['aggressiveness'] += self.map[x][y].aggressiveness
                        if self.map[x][y].energy_source == 1:
                            self.stats['green'] += 1
                        elif self.map[x][y].energy_source == 2:
                            self.stats['blue'] += 1
                    self.bot_turn(self.map[x][y], x, y)
                elif type(self.map[x][y]) == Bot.Organic:
                    org_func = self.map[x][y].turn()
                    if org_func == 'die':
                        self.map[x][y] = 0
        if self.recording:
            if self.stats_counter >= self.recording_step:
                self.divide_and_write_stats(self.stats_filename, self.recording_step)
                self.stats_counter = 0
            self.stats_counter += 1

    def bot_turn(self, bot, pos_x, pos_y):
        action_points = 1
        actions = 0
        self.map[pos_x][pos_y].look = False
        self.map[pos_x][pos_y].add_energy(-7)
        self.map[pos_x][pos_y].change_energy_sources(self.sun_map[pos_x][pos_y], self.minerals_map[pos_x][pos_y])
        while action_points > 0 and actions <= 15:
            action = bot.action()
            if action[0] == 'die': #erasing bot
                self.map[pos_x][pos_y] = Bot.Organic()
                if self.recording:
                    self.stats['deaths'] += 1
            
            elif action[0] == 'budd_otn': #spawning new bot
                coords = [cut(pos_x + directions[cut(cut(action[2] + action[1] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[2] + action[1] % 8))][1], self.size[1] - 1)]
                can_spawn_on_dir = True
                if not isinstance(self.map[coords[0]][coords[1]], Bot.Bot) and not isinstance(self.map[coords[0]][coords[1]], Bot.Organic):
                    if self.map[coords[0]][coords[1]] == 0:
                        self.spawn_bot([coords[0], coords[1]], action[3], action[4], action[5], action[6], action[7])
                        if random.randint(1,3) <= 1:
                            self.map[coords[0]][coords[1]].mutate()
                        if self.recording:
                            self.stats['born'] += 1
                    else:
                        can_spawn_on_dir = False
                else:
                    can_spawn_on_dir = False
                if not can_spawn_on_dir:
                    ran_dir_choose = []
                    for i in range(-1,2):
                        for o in range(-1,2):
                            if type(self.map[cut(pos_x + i, self.size[0] - 1)][cut(pos_y + o, self.size[1] - 1)]) != Bot.Bot and type(self.map[cut(pos_x + i, self.size[0] - 1)][cut(pos_y + o, self.size[1] - 1)]) != Bot.Organic:
                                if self.map[cut(pos_x + i, self.size[0] - 1)][cut(pos_y + o, self.size[1] - 1)] == 0:
                                    ran_dir_choose.append([cut(pos_x + i, self.size[0] - 1), cut(pos_y + o, self.size[1] - 1)])
                    if len(ran_dir_choose) > 0:
                        rand = random.randint(0, len(ran_dir_choose) - 1)
                        self.spawn_bot(ran_dir_choose[rand], action[3], action[4], action[5], action[6], action[7])
                        if random.randint(1,3) <= 1:
                            self.map[ran_dir_choose[rand][0]][ran_dir_choose[rand][1]].mutate()
                        if self.recording:
                            self.stats['born'] += 1
                    else:
                        self.map[pos_x][pos_y] = Bot.Organic()
                        if self.recording:
                            self.stats['deaths'] += 1
                
            elif action[0] == 'move_otn':
                coords = [cut(pos_x + directions[cut(cut(action[3] + action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[3] + action[2] % 8))][1], self.size[1] - 1)]
                if isinstance(self.map[coords[0]][coords[1]], Bot.Bot):
                    if self.map[coords[0]][coords[1]] == self.map[pos_x][pos_y]:
                        num = 1
                    else:
                        num = 2
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 3
                elif self.map[coords[0]][coords[1]] == 1:
                    num = 4
                else:
                    num = 5
                self.map[pos_x][pos_y].receive_jump_action(num)
                
                if not isinstance(self.map[coords[0]][coords[1]], Bot.Bot):
                    if self.map[coords[0]][coords[1]] == 0:
                        self.map[coords[0]][coords[1]] = self.map[pos_x][pos_y]
                        self.map[pos_x][pos_y] = 0
                        if self.recording:
                            self.stats['moves'] += 1
            
            elif action[0] == 'move_abs': 
                coords = [cut(pos_x + directions[cut(cut(action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[2] % 8))][1], self.size[1] - 1)]
                if isinstance(self.map[coords[0]][coords[1]], Bot.Bot):
                    if self.map[coords[0]][coords[1]] == self.map[pos_x][pos_y]:
                        num = 1
                    else:
                        num = 2
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 3
                elif self.map[coords[0]][coords[1]] == 1:
                    num = 4
                else:
                    num = 5
                self.map[pos_x][pos_y].receive_jump_action(num)
                
                if not isinstance(self.map[coords[0]][coords[1]], Bot.Bot):
                    if self.map[coords[0]][coords[1]] == 0:
                        self.map[coords[0]][coords[1]] = self.map[pos_x][pos_y]
                        self.map[pos_x][pos_y] = 0
                        if self.recording:
                            self.stats['moves'] += 1
            
            elif action[0] == 'turn_abs':
                action_points += 1
                self.map[pos_x][pos_y].jump_action(1)
                if self.recording:
                    self.stats['turns'] += 1
                
            elif action[0] == 'turn_otn':
                action_points += 1
                self.map[pos_x][pos_y].jump_action(1)
                if self.recording:
                    self.stats['turns'] += 1
            
            elif action[0] == 'look':
                coords = [cut(pos_x + directions[cut(cut(action[3] + action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[3] + action[2] % 8))][1], self.size[1] - 1)]
                if isinstance(self.map[coords[0]][coords[1]], Bot.Bot):
                    if self.map[coords[0]][coords[1]] == self.map[pos_x][pos_y]:
                        num = 1
                    else:
                        num = 2
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 3
                elif self.map[coords[0]][coords[1]] == 1:
                    num = 4
                else:
                    num = 5
                self.map[pos_x][pos_y].receive_jump_action(num)
                if self.recording:
                    self.stats['looks'] += 1
                self.map[pos_x][pos_y].look = True
                action_points += 1
                
            elif action[0] == 'eat_otn' or action[0] == 'eat_abs':
                if action[0] == 'eat_otn':
                    coords = [cut(pos_x + directions[cut(cut(action[3] + action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[3] + action[2] % 8))][1], self.size[1] - 1)]
                else:
                    coords = [cut(pos_x + directions[cut(cut(action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[2] % 8))][1], self.size[1] - 1)]
                if isinstance(self.map[coords[0]][coords[1]], Bot.Bot):
                    num = 1
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 3
                elif self.map[coords[0]][coords[1]] == 1:
                    num = 4
                else:
                    num = 5
                self.map[pos_x][pos_y].receive_jump_action(num)
                
                if isinstance(self.map[coords[0]][coords[1]], Bot.Bot):
                    self.map[coords[0]][coords[1]] = 0
                    self.map[pos_x][pos_y].add_energy(80)
                    if self.recording:
                        self.stats['deaths'] += 1
                elif isinstance(self.map[coords[0]][coords[1]], Bot.Organic):
                    self.map[coords[0]][coords[1]] = 0
                    self.map[pos_x][pos_y].add_energy(70)
                    
            elif action[0] == 'share_otn' or action[0] == 'share_abs':
                if action[0] == 'share_otn':
                    coords = [cut(pos_x + directions[cut(cut(action[3] + action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[3] + action[2] % 8))][1], self.size[1] - 1)]
                else:
                    coords = [cut(pos_x + directions[cut(cut(action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[2] % 8))][1], self.size[1] - 1)]
                if type(self.map[coords[0]][coords[1]]) == Bot.Bot:
                    energy = int((self.map[pos_x][pos_y].get_energy() + self.map[coords[0]][coords[1]].get_energy())/2)
                    self.map[coords[0]][coords[1]].add_energy(energy, True)
                    self.map[pos_x][pos_y].add_energy(energy, True)
                action_points += 1
                if self.recording:
                    self.stats['shares'] += 1
                self.map[pos_x][pos_y].jump_action(1)
            
            elif action[0] == 'how_much_energy':
                action_points += 1
                
            elif action[0] == 'if_surrounded':
                surrounded = 0
                for i in range(-1,2):
                    for o in range(-1,2):
                        if type(self.map[cut(pos_x + i, self.size[0] - 1)][cut(pos_y + o, self.size[1] - 1)]) == Bot.Bot or type(self.map[cut(pos_x + i, self.size[0] - 1)][cut(pos_y + o, self.size[1] - 1)]) == Bot.Organic:
                            surrounded += 1
                if surrounded == 9:
                    self.map[pos_x][pos_y].receive_jump_action(2)
                else:
                    self.map[pos_x][pos_y].receive_jump_action(3)
                action_points += 1
                
            elif action[0] == 'photosynthesis' or action[0] == 'get_minerals':
                self.map[pos_x][pos_y].jump_action(1)
                
            elif action[0] == 'nrg_source':
                if self.sun_map[pos_x][pos_y] > self.minerals_map[pos_x][pos_y]:
                    self.map[pos_x][pos_y].receive_jump_action(1)
                else:
                    self.map[pos_x][pos_y].receive_jump_action(2)
                action_points += 1
            
            
            action_points -= 1
            if (action_points == 0 or actions > 15) and isinstance(self.map[pos_x][pos_y], Bot.Bot):
                self.map[pos_x][pos_y].reduce_aggressiveness()
            actions += 1


    def divide_and_write_stats(self, filename = 'stats', step = 200):
        self.stats['energy'] /= self.stats['bots']
        self.stats['aggressiveness'] /= self.stats['bots']
        self.stats['looks'] /= step
        self.stats['moves'] /= step
        self.stats['shares'] /= step
        self.stats['turns'] /= step
        self.stats['bots'] /= step
        self.stats['green'] /= step
        self.stats['blue'] /= step
        self.stats['deaths'] /= step
        self.stats['born'] /= step
        with open(f'./stats/files/{filename}.txt', 'a') as file:
            file.write(str(self.stats) + '\n')
        self.stats = default_stats
    
    def generate_energy_map(self):
        noise = create_noise(self.size[0], self.size[1])
        noise = AA(noise)
        noise = AA(noise)
        for _ in range(3):
            noise = inc_contrast(noise)
        noise = round_(noise)
        noise = cut_noise(noise, 255, 0)
        self.sun_map = ret_sun_map(noise)
        self.minerals_map = ret_min_map(noise)
    
    def save(self, file_name):
        with open(file_name, 'w') as file:
            file.write(str(self.sun_map) + '\n')
            file.write(str(self.minerals_map) + '\n')
            for i in range(self.size[0]):
                for o in range(self.size[1]):
                    if type(self.map[i][o]) == Bot.Bot:
                        file.write(f'{["bot", str(self.map[i][o])]}\n')
                    elif type(self.map[i][o]) == Bot.Organic:
                        file.write(f'{["organic", str(self.map[i][o])]}\n')
                    else:
                        file.write(f'{["number", self.map[i][o]]}\n')
    
    def load(self, file_name):
        with open(file_name, 'r') as file:
            c_y = 0
            c_x = 0
            buf_num = 0
            for line in file:
                arr = eval(line)
                if buf_num == 0:
                    self.sun_map = arr
                    self.size = [len(arr), len(arr[0])]
                    self.map = []
                    for x in range(self.size[0]):
                        self.map.append([])
                        for y in range(self.size[1]):
                            if y != 0 and y != self.size[1] - 1:
                                self.map[x].append(0)
                            else:
                                self.map[x].append(1)
                elif buf_num == 1:
                    self.minerals_map = arr
                else:
                    if arr[0] == 'number':
                        self.map[c_x][c_y] = arr[1]
                    elif arr[0] == 'organic':
                        arr[1] = eval(arr[1])
                        self.map[c_x][c_y] = Bot.Organic(arr[1][0])
                    elif arr[0] == 'bot':
                        arr[1] = eval(arr[1])
                        self.spawn_bot([c_x, c_y], arr[1][0], arr[1][1][0], arr[1][1][1], arr[1][1][2], arr[1][1][3])
                    c_y += 1
                    if c_y == self.size[1]:
                        c_y = 0
                        c_x += 1
                buf_num += 1
        
    def new(self, size = [100, 75], sun_level = 12):
        self.recording_step = 100
        self.stats_counter = 0
        self.stats_filename = ''
        self.recording = False
        self.size = size
        self.sun_level = sun_level
        self.sun_map = []
        self.minerals_map = []
        self.map = []
        for x in range(self.size[0]):
            self.map.append([])
            self.sun_map.append([])
            self.minerals_map.append([])
            for y in range(self.size[1]):
                if y != 0 and y != self.size[1] - 1:
                    self.map[x].append(0)
                else:
                    self.map[x].append(1)
                
                if y > int(self.size[1]/2):
                    self.sun_map[x].append(0)
                    self.minerals_map[x].append(sun_level)
                else:
                    self.sun_map[x].append(sun_level)
                    self.minerals_map[x].append(0)
        self.spawn_bot([1,1])

    def set_recording(self, value):
        self.recording = value