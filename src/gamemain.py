#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unit
from unit import origin_attribute
import random
from random import choice
import time
MAXROUND = 1000
name=['base','meat','hacker','superman','battle_tank','bolt_tank','nuke_tank','uav','eagle',
            'hack_lab','bid_lab','car_lab','elec_lab','radiation_lab','uav_lab','aircraft_lab',
           'build_lab','finance_lab','material_lab','nano_lab','teach_building','bank']
type=[0,1,1,1,2,2,2,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4]
attack_percentage={
                    unit.MACHINEGUN: {unit.FORT:0.25,unit.UNARMORED:2.00,unit.LIGHT:1.00,unit.MEDIUM:0.75,unit.HEAVY:0.50},
                    unit.ELEC:       {unit.FORT:0.75,unit.UNARMORED:0.00,unit.LIGHT:1.50,unit.MEDIUM:1.00,unit.HEAVY:0.50},
                    unit.ARTILLERY:  {unit.FORT:1.00,unit.UNARMORED:0.50,unit.LIGHT:1.00,unit.MEDIUM:1.25,unit.HEAVY:0.75},
                    unit.PENETRATING:{unit.FORT:1.00,unit.UNARMORED:0.25,unit.LIGHT:0.75,unit.MEDIUM:0.75,unit.HEAVY:1.50},
                    unit.EXPLOSION:  {unit.FORT:1.50,unit.UNARMORED:0.75,unit.LIGHT:0.50,unit.MEDIUM:0.50,unit.HEAVY:1.25}
                    }
class GameMain:
    units = {}  # 单位dict key:unit_id value:unitobject
    hqs = []  # 主基地
    buildings = []  # 中立建筑
    # turn_flag = 0  # 谁的回合
    is_end = False
    check_winner = 3 #胜利者
    ai0_healing_flag = 0
    ai1_healing_flag = 0
    ai0_eagle_flag = 0  # 鹰式战机技能2是否启用
    ai1_eagle_flag = 0  # 鹰式战机技能2是否启用
    ai0_shield_flag = [0,-1,-1]
    ai1_shield_flag = [0,-1,-1]
    turn_num = 0  # 回合数
    phase_num = 0  # 回合阶段指示
    skill_instr_0 = []  # ai0的当前回合指令
    skill_instr_1 = []  # ai1的当前回合制令
    produce_instr_0 = []  # 指令格式为[building_id,building_id,]
    produce_instr_1 = []
    move_instr_0 = []  # 指令格式[[unit_id,position_x,position_y],[unit_id,position_x,position_y]]
    move_instr_1 = []
    capture_instr_0 = []  # 指令格式[[unit_id,building_id][unit_id,building_id][]]
    capture_instr_1 = []
    buff = {
        unit.FLAG_0: {
            unit.BASE: {'health_buff': 0.0, 'attack_buff': 0.0, 'tech_buff': 0.0, 'defense_buff': 0.0,
                            'shot_range_buff': 0.0, 'economy_buff': 0.0},
            unit.INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                            'shot_range_buff': 0.0, 'produce_buff': 0.0},
            unit.VEHICLE: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                           'shot_range_buff': 0.0, 'produce_buff': 0.0},
            unit.AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                            'shot_range_buff': 0.0, 'produce_buff': 0.0}
        },
        unit.FLAG_1: {
            unit.BASE: {'health_buff': 0.0, 'attack_buff': 0.0, 'tech_buff': 0.0, 'defense_buff': 0.0,
                            'shot_range_buff': 0.0, 'economy_buff': 0.0},
            unit.INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                            'shot_range_buff': 0.0, 'produce_buff': 0.0},
            unit.VEHICLE: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                           'shot_range_buff': 0.0, 'produce_buff': 0.0},
            unit.AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                            'shot_range_buff': 0.0, 'produce_buff': 0.0}
        }
    }
    total_id = 0  # 总共的项目的id编号
    resource = {}  # 双方金钱、科技、剩余人口容量记录
    amount_limit = {
        0: {'eagle': False, 'nuke_tank': False, 'superman': False},
        1: {'eagle': False, 'nuke_tank': False, 'superman': False}
    }  # 记录eagle superman 和 nuketank的最大上限是否达到

    def __init__(self):
        map = []
        x_pos = y_pos = 0
        while x_pos < 10000:
            map.append(1)
            x_pos = x_pos + 1

        def map_use(x_place, y_place):
            map[x_place * 10 + y_place] = 0
            map[x_place * 10 + y_place + 1] = 0
            map[x_place * 10 + y_place - 1] = 0
            map[(1 + x_place) * 10 + y_place] = 0
            map[(x_place - 1) * 10 + y_place] = 0

        def map_judge(x_place, y_place):
            if x_place < 5 or x_place >= 95 or y_place < 5 or y_place >= 95:
                return False
            if map[x_place * 10 + y_place] == 1 and map[x_place * 10 + y_place + 1] == 1 and map[
                                        x_place * 10 + y_place - 1] == 1 and map[(1 + x_place) * 10 + y_place] == 1 and \
                            map[(x_place - 1) * 10 + y_place] == 1:
                return True
            else:
                return False

        ai_id0 = 0
        ai_id1 = 1
        # 地图生成模块
        # 初始化self.resource
        self.resource = {ai_id0: {"tech": 1600, "money": 4000, "remain_people": 100},
                         ai_id1: {"tech": 1600, "money": 4000, "remain_people": 100}}
        # 在一定范围内random出一个基地并中心对称 并伴随生成bank 和teaching building 各一个
        box_base0_x = random.randint(2, 7)
        box_base0_y = random.randint(2, 3)
        # box_base1_x = 10 - box_base0_x
        # box_base1_y = 5 - box_base0_y
        player0_x = box_base0_x * 10 + random.randint(1, 8)
        player0_y = box_base0_y * 10 + random.randint(1, 8)
        player1_x = 99 - player0_x
        player1_y = 99 - player0_y
        # show on the map
        map_use(player0_x, player0_y)
        map_use(player0_x, player0_y + 2)
        map_use(player0_x, player0_y - 2)
        map_use(player1_x, player1_y)
        map_use(player1_x, player1_y + 2)
        map_use(player1_x, player1_y - 2)

        base0 = unit.UnitObject(self.total_id, ai_id0, 'base', [player0_x, player0_y], self.buff)
        self.units[self.total_id] = base0
        self.hqs.append(base0)
        self.total_id += 1
        base1 = unit.UnitObject(self.total_id, ai_id1, 'base', [player1_x, player1_y], self.buff)
        self.units[self.total_id] = base1
        self.hqs.append(base1)
        self.total_id += 1
        tech0 = unit.UnitObject(self.total_id, ai_id0, 'teach_building', [player0_x, player0_y + 2], self.buff)
        self.units[self.total_id] = tech0
        self.total_id += 1
        tech1 = unit.UnitObject(self.total_id, ai_id1, 'teach_building', [99 - player0_x, 97 - player0_y], self.buff)
        self.units[self.total_id] = tech1
        self.total_id += 1
        bank0 = unit.UnitObject(self.total_id, ai_id0, 'bank', [player0_x, player0_y - 2], self.buff)
        self.units[self.total_id] = bank0
        self.total_id += 1
        bank1 = unit.UnitObject(self.total_id, ai_id1, 'bank', [99 - player0_x, 101 - player0_y], self.buff)
        self.units[self.total_id] = bank1
        self.total_id += 1
        # random银行和教学楼并中心对称
        # 除去出生地附近 教学楼和银行总数为12或11（一半地图） 各自数目不定
        bank_and_teach = 12
        # box_x = 0
        # box_y = 0
        while (bank_and_teach > 0):
            type_rand = random.randint(0, 1)  # 0产生教学楼，1产生银行
            if type_rand == 0:
                tech_x = random.randint(1, 98)
                tech_y = random.randint(1, 98)
                while (map_judge(tech_x, tech_y) == False):
                    tech_x = random.randint(1, 98)
                    tech_y = random.randint(1, 98)
                tech_1_x = 99 - tech_x
                tech_1_y = 99 - tech_y
                map_use(tech_x, tech_y)
                map_use(tech_1_x, tech_1_y)

                tech0 = unit.UnitObject(self.total_id, -1, 'teach_building',
                                        [tech_x, tech_y], self.buff)
                self.units[self.total_id] = tech0
                self.buildings.append(tech0)
                self.total_id += 1
                tech1 = unit.UnitObject(self.total_id, -1, 'teach_building',
                                        [tech_1_x, tech_1_y], self.buff)
                self.units[self.total_id] = tech1
                self.buildings.append(tech1)
                self.total_id += 1
            if type_rand == 1:
                bank_x = random.randint(1, 98)
                bank_y = random.randint(1, 98)
                while (map_judge(bank_x, bank_y) == False):
                    bank_x = random.randint(1, 98)
                    bank_y = random.randint(1, 98)
                bank_1_x = 99 - bank_x
                bank_1_y = 99 - bank_y
                map_use(bank_x, bank_y)
                map_use(bank_1_x, bank_1_y)

                bank0 = unit.UnitObject(self.total_id, -1, 'bank',
                                        [bank_x, bank_y], self.buff)
                self.units[self.total_id] = bank0
                self.buildings.append(bank0)
                self.total_id += 1
                bank1 = unit.UnitObject(self.total_id, -1, 'bank',
                                        [bank_1_x, bank_1_y], self.buff)
                self.buildings.append(bank1)
                self.units[self.total_id] = bank1
                self.total_id += 1
            bank_and_teach -= 1
        # 生成11个具有特定技能的建筑 不进行building_id编号和占有方编号
        building_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        total_building = 11
        while (total_building > 0):
            building_x = random.randint(1, 98)
            building_y = random.randint(1, 98)
            while (map_judge(building_x, building_y) == False):
                building_x = random.randint(1, 98)
                building_y = random.randint(1, 98)
            building_type = choice(building_list)
            if building_type == 1:
                hack_lab0 = unit.UnitObject(self.total_id, -1, 'hack_lab', [building_x, building_y], self.buff)
                self.buildings.append(hack_lab0)
                self.units[self.total_id] = hack_lab0
                self.total_id += 1
                hack_lab1 = unit.UnitObject(self.total_id, -1, 'hack_lab', [99 - building_x, 99 - building_y],
                                            self.buff)
                self.units[self.total_id] = hack_lab1
                self.buildings.append(hack_lab1)
                self.total_id += 1
            if building_type == 2:
                bid_lab0 = unit.UnitObject(self.total_id, -1, 'bid_lab', [building_x, building_y], self.buff)
                self.buildings.append(bid_lab0)
                self.units[self.total_id] = bid_lab0
                self.total_id += 1
                bid_lab1 = unit.UnitObject(self.total_id, -1, 'bid_lab', [99 - building_x, 99 - building_y],
                                           self.buff)
                self.buildings.append(bid_lab1)
                self.units[self.total_id] = bid_lab1
                self.total_id += 1
            if building_type == 3:
                car_lab0 = unit.UnitObject(self.total_id, -1, 'car_lab', [building_x, building_y], self.buff)
                self.buildings.append(car_lab0)
                self.units[self.total_id] = car_lab0
                self.total_id += 1
                car_lab1 = unit.UnitObject(self.total_id, -1, 'car_lab', [99 - building_x, 99 - building_y],
                                           self.buff)
                self.units[self.total_id] = car_lab1
                self.buildings.append(car_lab1)
                self.total_id += 1
            if building_type == 4:
                elec_lab0 = unit.UnitObject(self.total_id, -1, 'elec_lab', [building_x, building_y], self.buff)
                self.buildings.append(elec_lab0)
                self.units[self.total_id] = elec_lab0
                self.total_id += 1
                elec_lab1 = unit.UnitObject(self.total_id, -1, 'elec_lab', [99 - building_x, 99 - building_y],
                                            self.buff)
                self.buildings.append(elec_lab1)
                self.units[self.total_id] = elec_lab1
                self.total_id += 1
            if building_type == 5:
                radiation_lab0 = unit.UnitObject(self.total_id, -1, 'radiation_lab', [building_x, building_y],
                                                 self.buff)
                self.buildings.append(radiation_lab0)
                self.units[self.total_id] = radiation_lab0
                self.total_id += 1
                radiation_lab1 = unit.UnitObject(self.total_id, -1, 'radiation_lab',
                                                 [99 - building_x, 99 - building_y], self.buff)
                self.buildings.append(radiation_lab1)
                self.units[self.total_id] = radiation_lab1
                self.total_id += 1
            if building_type == 6:
                uav_lab0 = unit.UnitObject(self.total_id, -1, 'uav_lab', [building_x, building_y], self.buff)
                self.buildings.append(uav_lab0)
                self.units[self.total_id] = uav_lab0
                self.total_id += 1
                uav_lab1 = unit.UnitObject(self.total_id, -1, 'uav_lab', [99 - building_x, 99 - building_y],
                                           self.buff)
                self.buildings.append(uav_lab1)
                self.units[self.total_id] = uav_lab1
                self.total_id += 1
            if building_type == 7:
                aircraft_lab0 = unit.UnitObject(self.total_id, -1, 'aircraft_lab', [building_x, building_y], self.buff)
                self.buildings.append(aircraft_lab0)
                self.units[self.total_id] = aircraft_lab0
                self.total_id += 1
                aircraft_lab1 = unit.UnitObject(self.total_id, -1, 'aircraft_lab', [99 - building_x, 99 - building_y],
                                                self.buff)
                self.units[self.total_id] = aircraft_lab1
                self.buildings.append(aircraft_lab1)
                self.total_id += 1
            if building_type == 8:
                build_lab0 = unit.UnitObject(self.total_id, -1, 'build_lab', [building_x, building_y], self.buff)
                self.buildings.append(build_lab0)
                self.units[self.total_id] = build_lab0
                self.total_id += 1
                build_lab1 = unit.UnitObject(self.total_id, -1, 'build_lab', [99 - building_x, 99 - building_y],
                                             self.buff)
                self.units[self.total_id] = build_lab1
                self.buildings.append(build_lab1)
                self.total_id += 1
            if building_type == 9:
                finance_lab0 = unit.UnitObject(self.total_id, -1, 'finance_lab', [building_x, building_y], self.buff)
                self.buildings.append(finance_lab0)
                self.units[self.total_id] = finance_lab0
                self.total_id += 1
                finance_lab1 = unit.UnitObject(self.total_id, -1, 'finance_lab', [99 - building_x, 99 - building_y],
                                               self.buff)
                self.units[self.total_id] = finance_lab1
                self.buildings.append(finance_lab1)
                self.total_id += 1
            if building_type == 10:
                material_lab0 = unit.UnitObject(self.total_id, -1, 'material_lab', [building_x, building_y], self.buff)
                self.buildings.append(material_lab0)
                self.units[self.total_id] = material_lab0
                self.total_id += 1
                material_lab1 = unit.UnitObject(self.total_id, -1, 'material_lab', [99 - building_x, 99 - building_y],
                                                self.buff)
                self.units[self.total_id] = material_lab1
                self.buildings.append(material_lab1)
                self.total_id += 1
            if building_type == 11:
                nano_lab0 = unit.UnitObject(self.total_id, -1, 'nano_lab', [building_x, building_y], self.buff)
                self.buildings.append(nano_lab0)
                self.units[self.total_id] = nano_lab0
                self.total_id += 1
                nano_lab1 = unit.UnitObject(self.total_id, -1, 'nano_lab', [99 - building_x, 99 - building_y],
                                            self.buff)
                self.units[self.total_id] = nano_lab1
                self.buildings.append(nano_lab1)
                self.total_id += 1
            building_list.remove(building_type)
            total_building -= 1
        pass

    def win_determine(self):
        # 胜利判定
        # 胜利判定:0 ai_id0 wins; 1 ai_id1 wins; 2 tie; 3 game goes on
        unit_obj = list(self.units.values())  # 所有的单位
        if self.hqs[0].health_now * self.hqs[1].health_now > 0 and self.hqs[0].health_now + self.hqs[
            1].health_now > 0:  # 如果双方主基地都正Hp
            return 3
        else:
            if self.hqs[0].health_now < self.hqs[1].health_now:
                return 1
            if self.hqs[0].health_now > self.hqs[1].health_now:
                return 0
            if self.hqs[0].health_now == self.hqs[1].health_now:#HP相等
                if self.resource[0]["remain_people"]<self.resource[1]["remain_people"]:
                    return 0
                elif self.resource[0]["remain_people"]>self.resource[1]["remain_people"]:
                    return 1
                elif self.resource[0]["tech"] + self.resource[0]["money"]>self.resource[1]["tech"] + self.resource[1]["money"]:
                    return 0
                elif self.resource[0]["tech"] + self.resource[0]["money"]<self.resource[1]["tech"] + self.resource[1]["money"]:
                    return 1
                else:
                    return 2

    def timeup_determine(self):
        # 超时胜利判定
        if self.turn_num <= MAXROUND:
            return 3
        if self.turn_num > MAXROUND:  # 如果超过了最大回合数
            unit_obj = list(self.units.values())
            if self.hqs[0].health_now < self.hqs[1].health_now:
                return 1
            if self.hqs[0].health_now > self.hqs[1].health_now:
                return 0
            if self.hqs[0].health_now == self.hqs[1].health_now:#HP相等
                if self.resource[0]["remain_people"]<self.resource[1]["remain_people"]:
                    return 0
                elif self.resource[0]["remain_people"]>self.resource[1]["remain_people"]:
                    return 1
                elif self.resource[0]["tech"] + self.resource[0]["money"]>self.resource[1]["tech"] + self.resource[1]["money"]:
                    return 0
                elif self.resource[0]["tech"] + self.resource[0]["money"]<self.resource[1]["tech"] + self.resource[1]["money"]:
                    return 1
                else:
                    return 2

    def cleanup_phase(self):
        # 单位死亡判定
        # id_collection = [0,1]  # 寻找传入ai_id对应的value
        # for ai_id in id_collection:
        tempcache=self.units.copy()
        for unit_id in tempcache.keys():
            things = self.units[unit_id]
            if self.units[unit_id].health_now <= 0 or things.hacked_point >= things.health_now:
                del self.units[unit_id]  # 从字典的value列表中把死亡单位删除
                if things.Get_type_name() == 1:
                    self.resource[things.flag]['remain_people'] += origin_attribute['meat']['people_cost']
                    continue
                if things.Get_type_name() == 2:
                    self.resource[things.flag]['remain_people'] += origin_attribute['hacker']['people_cost']
                    continue
                if things.Get_type_name() == 3:
                    self.resource[things.flag]['remain_people'] += origin_attribute['superman']['people_cost']
                    self.amount_limit[things.flag]['superman'] = False
                    continue
                if things.Get_type_name() == 4:
                    self.resource[things.flag]['remain_people'] += origin_attribute['battle_tank']['people_cost']
                    continue
                if things.Get_type_name() == 5:
                    self.resource[things.flag]['remain_people'] += origin_attribute['bolt_tank']['people_cost']
                    continue
                if things.Get_type_name() == 6:
                    self.amount_limit[things.flag]['nuke_tank'] = False
                    self.resource[things.flag]['remain_people'] += origin_attribute['nuke_tank']['people_cost']
                    continue
                if things.Get_type_name() == 7:
                    self.resource[things.flag]['remain_people'] += origin_attribute['uav']['people_cost']
                    continue
                if things.Get_type_name() == 8:
                    self.resource[things.flag]['remain_people'] += origin_attribute['eagle']['people_cost']
                    self.amount_limit[things.flag]['eagle'] = False
                    continue
        pass

    def skill_phase(self, order):
        # 技能结算
        def Get_id_information(id):
            for k in self.units:
                if (k == id):
                    return self.units[k]
            return -1

        def Get_distance(my_position, enemy_position):
            x = my_position[0] - enemy_position[0]
            y = my_position[1] - enemy_position[1]
            return abs(x)+abs(y)

        def Get_distance2(my_position, enemy_position):#核子坦克距离计算用
            x = my_position[0] - enemy_position[0]
            y = my_position[1] - enemy_position[1]
            return (x*x+y*y)**0.5

        #主基地技能1
        def base_skill1(id, attack_range_x,attack_range_y):
            attack_range = [attack_range_x,attack_range_y]
            my_information = Get_id_information(id)
            if (my_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time1
                distance = Get_distance(my_information.position, attack_range)
                my_attack_type = origin_attribute['base']['attack_type']
                if (skill_cd >= origin_attribute['base']['skill_cd_1'] and distance <= my_information.shot_range_now):
                    for k in self.units:
                        enemy_position = self.units[k].position
                        enemy_defense_type = origin_attribute[name[self.units[k].Get_type_name()]]['defense_type']
                        if (enemy_position == attack_range):
                            self.units[k].reset_attribute(self.buff,health=self.units[k].health_now - my_information.attack_now * (1 - self.units[k].defense_now / 1000)*attack_percentage[my_attack_type][enemy_defense_type])
                            my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
                        elif (Get_distance(enemy_position,attack_range) == 1):
                            self.units[k].reset_attribute(self.buff,health=self.units[k].health_now - 0.5 * my_information.attack_now * (1 - self.units[k].defense_now / 1000)*attack_percentage[my_attack_type][enemy_defense_type])
                            my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
                        elif (Get_distance(enemy_position,attack_range) == 2):
                            self.units[k].reset_attribute(self.buff,health=self.units[k].health_now - 0.25 * my_information.attack_now * (1 - self.units[k].defense_now / 1000)*attack_percentage[my_attack_type][enemy_defense_type])
                            my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
        # 黑客技能1
        def hacker_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            if (my_information != -1 and enemy_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time1
                distance = Get_distance(my_information.position, enemy_information.position)
                if (skill_cd >= origin_attribute['hacker']['skill_cd_1'] and distance <= my_information.shot_range_now):
                    if (my_information.flag != enemy_information.flag) and (enemy_information.Get_unit_type() == 2):
                        enemy_information.reset_attribute(self.buff,hacked_point=enemy_information.hacked_point + 15)
                        my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
                    elif (my_information.flag == enemy_information.flag) and (enemy_information.Get_unit_type() == 2):
                        enemy_information.reset_attribute(self.buff,hacked_point=enemy_information.hacked_point - 15)
                        my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 改造人战士技能1
        def superman_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            if (my_information != -1 and enemy_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time1
                distance = Get_distance(my_information.position, enemy_information.position)
                my_attack_type = origin_attribute['superman']['attack_type']
                enemy_defense_type = origin_attribute[name[enemy_information.Get_type_name()]]['defense_type']
                if (skill_cd >= origin_attribute['superman']['skill_cd_1'] and distance <= my_information.shot_range_now and (my_information.flag != enemy_information.flag)):
                    if (my_information.motor_type == 0) and (enemy_information.Get_unit_type() == 0 or enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 2):
                        enemy_information.reset_attribute(self.buff,health=enemy_information.health_now - my_information.attack_now * (1 - enemy_information.defense_now / 1000)*attack_percentage[my_attack_type][enemy_defense_type])
                        my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
                    elif (my_information.motor_type == 1) and (enemy_information.Get_unit_type() != 4):
                        enemy_information.reset_attribute(self.buff,health=enemy_information.health_now - my_information.attack_now * (1 - enemy_information.defense_now / 1000)*attack_percentage[my_attack_type][enemy_defense_type])
                        my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 改造人战士技能2
        def superman_skill2(id):
            my_information = Get_id_information(id)
            if (my_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time2
                if (skill_cd >= origin_attribute['superman']['skill_cd_2']):
                    #print(my_information.max_speed_now)
                    my_information.reset_attribute(self.buff, speed=12.0,healing_rate=0.02, motor_type=1,skill_last_release_time2=self.turn_num)
                    #print(my_information.max_speed_now)
                    #self.superman_skill_release_time[my_information.flag] = self.turn_num

        # 主站坦克技能1
        def battle_tank_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            if (my_information != -1 and enemy_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time1
                distance = Get_distance(my_information.position, enemy_information.position)
                my_attack_type = origin_attribute['bolt_tank']['attack_type']
                enemy_defense_type = origin_attribute[name[enemy_information.Get_type_name()]]['defense_type']
                if (skill_cd >= origin_attribute['battle_tank']['skill_cd_1'] and distance <= my_information.shot_range_now and (my_information.flag != enemy_information.flag)):
                    if (enemy_information.Get_unit_type() == 2 or enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 0):
                        enemy_information.reset_attribute(self.buff, health=enemy_information.health_now - my_information.attack_now * (1 - enemy_information.defense_now / 1000)*attack_percentage[my_attack_type][enemy_defense_type])
                        my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 电子对抗坦克技能1 修改计算公式
        def bolt_tank_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            if (my_information != -1 and enemy_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time1
                distance = Get_distance(my_information.position, enemy_information.position)
                my_attack_type = origin_attribute['bolt_tank']['attack_type']
                enemy_defense_type = origin_attribute[name[enemy_information.Get_type_name()]]['defense_type']
                if (skill_cd >= origin_attribute['bolt_tank']['skill_cd_1'] and distance <= my_information.shot_range_now):
                    if (my_information.flag != enemy_information.flag) and (enemy_information.Get_unit_type() == 3):
                        enemy_information.reset_attribute(self.buff,health=enemy_information.health_now - my_information.attack_now * (1 - enemy_information.defense_now / 1000)*attack_percentage[my_attack_type][enemy_defense_type])
                        my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
                    elif (my_information.flag != enemy_information.flag) and (enemy_information.Get_unit_type() == 2):
                        enemy_information.reset_attribute(self.buff, is_disable=True,disable_since=self.turn_num)
                        my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 核子坦克技能1
        def nuke_tank_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            if (my_information != -1 and enemy_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time1
                distance = Get_distance(my_information.position, enemy_information.position)
                my_attack_type = origin_attribute['nuke_tank']['attack_type']
                enemy_defense_type = origin_attribute[name[enemy_information.Get_type_name()]]['defense_type']
                if (skill_cd >= origin_attribute['nuke_tank']['skill_cd_1'] and distance <= my_information.shot_range_now and (my_information.flag != enemy_information.flag)):
                    if (enemy_information.Get_unit_type() == 2 or enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 0):
                        enemy_information.reset_attribute(self.buff, health=enemy_information.health_now - my_information.attack_now * (1 - enemy_information.defense_now / 1000)*attack_percentage[my_attack_type][enemy_defense_type])
                        my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 核子坦克技能2
        def nuke_tank_skill2(id, attack_range_x, attack_range_y):
            attack_range = [attack_range_x, attack_range_y]
            my_information = Get_id_information(id)
            if (my_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time2
                distance = Get_distance(my_information.position, attack_range)
                if (skill_cd >= origin_attribute['nuke_tank']['skill_cd_2'] and distance <= my_information.shot_range_now):
                    for k in self.units:
                        enemy_position = self.units[k].position
                        if (Get_distance2(enemy_position, attack_range) < 2):
                            self.units[k].reset_attribute(self.buff, health=self.units[k].health_now - 450)
                            my_information.reset_attribute(self.buff, skill_last_release_time2=self.turn_num)

        # 无人战机技能1
        def uav(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            if (my_information != -1 and enemy_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time1
                distance = Get_distance(my_information.position, enemy_information.position)
                my_attack_type = origin_attribute['uav']['attack_type']
                enemy_defense_type = origin_attribute[name[enemy_information.Get_type_name()]]['defense_type']
                if (skill_cd >= origin_attribute['uav']['skill_cd_1'] and distance <= my_information.shot_range_now and (my_information.flag != enemy_information.flag)):
                    if (enemy_information.Get_unit_type() == 3 or enemy_information.Get_unit_type() == 2 or enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 0):
                        enemy_information.reset_attribute(self.buff,health=enemy_information.health_now - my_information.attack_now * ( 1 - enemy_information.defense_now / 1000)*attack_percentage[my_attack_type][enemy_defense_type])
                        my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 鹰式战斗机技能1
        def eagle_skill1(id, attack_range_x,attack_range_y):
            attack_range = [attack_range_x,attack_range_y]
            my_information = Get_id_information(id)
            if (my_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time1
                distance = Get_distance(my_information.position, attack_range)
                my_attack_type = origin_attribute['eagle']['attack_type']
                if (skill_cd >= origin_attribute['eagle']['skill_cd_1'] and distance <= my_information.shot_range_now):
                    for k in self.units:
                        enemy_position = self.units[k].position
                        enemy_defense_type = origin_attribute[name[self.units[k].Get_type_name()]]['defense_type']
                        if (enemy_position == attack_range):
                            self.units[k].reset_attribute(self.buff,health=self.units[k].health_now - my_information.attack_now * (1 - self.units[k].defense_now / 1000)*attack_percentage[my_attack_type][enemy_defense_type])
                            my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 鹰式战斗机技能2
        def eagle_skill2(id, attack_range_x1,attack_range_y1,attack_range_x2, attack_range_y2):
            attack_range1 = [attack_range_x1,attack_range_y1]
            attack_range2 = [attack_range_x2,attack_range_y2]
            my_information = Get_id_information(id)
            if (my_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time2
                distance1 = Get_distance(my_information.position, attack_range1)
                distance2 = Get_distance(my_information.position, attack_range2)
                if (skill_cd >= origin_attribute['eagle']['skill_cd_2'] and distance1 <= my_information.shot_range_now and distance2 <= my_information.shot_range_now):
                    for k in self.units:
                        enemy_position = self.units[k].position
                        if (enemy_position == attack_range1 or enemy_position == attack_range2):
                            self.units[k].reset_attribute(self.buff, health=self.units[k].health_now - 400)
                    my_information.reset_attribute(self.buff, speed=my_information.max_speed_now + 5, skill_last_release_time2=self.turn_num)
                    if my_information.flag == 0:
                        self.ai0_eagle_flag = 1
                    if my_information.flag == 1:
                        self.ai1_eagle_flag = 1

        # 建筑学院技能2
        def construct_skill2(id, attack_range_x1, attack_range_y1):
            my_information = Get_id_information(id)
            if (my_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time2
                if skill_cd >= origin_attribute['build_lab']['skill_cd_2']:
                    for k in self.units:
                        enemy_position_x1 = self.units[k].position[0]
                        enemy_position_y1 = self.units[k].position[1]
                        distance= abs(abs(attack_range_x1-enemy_position_x1)-abs(attack_range_y1-enemy_position_y1))
                        if distance <= 1 and (self.units[k].Get_unit_type() == 1 or self.units[k].Get_unit_type() == 2):
                            self.units[k].reset_attribute(self.buff, health=self.units[k].health_now - 250)
                    my_information.reset_attribute(self.buff, skill_last_release_time2=self.turn_num)

        # 社会心理学院技能2
        def society_skill2(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            if (my_information != -1 and enemy_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time2
                if (skill_cd >= origin_attribute['finance_lab']['skill_cd_2'] and my_information.flag != enemy_information.flag):
                    if (enemy_information.Get_unit_type() == 3 or enemy_information.Get_unit_type() == 2 or enemy_information.Get_unit_type() == 1):
                        if(enemy_information.Get_type_name() != 3 and enemy_information.Get_type_name() != 6 and enemy_information.Get_type_name() != 8):
                            if  self.resource[my_information.flag]['remain_people'] + unit.origin_attribute[name[enemy_information.Get_type_name()]]['people_cost'] < 100:
                                self.resource[my_information.flag]['remain_people'] += unit.origin_attribute[name[enemy_information.Get_type_name()]]['people_cost']
                                self.resource[enemy_information.flag]['remain_people'] -= unit.origin_attribute[name[enemy_information.Get_type_name()]]['people_cost']
                                enemy_information.reset_attribute(self.buff, flag = my_information.flag)
                    my_information.reset_attribute(self.buff, skill_last_release_time2=self.turn_num)

        # 特殊材料学院技能2
        def material_skill2(id, target_id):
            my_information = Get_id_information(id)
            target_information = Get_id_information(target_id)
            if (my_information != -1 and target_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time2
                if (skill_cd >= origin_attribute['material_lab']['skill_cd_2']):
                    target_information.reset_attribute(self.buff, defense = 1000, skill_last_release_time2=self.turn_num)
                    if target_information.flag == 0:
                        self.ai0_shield_flag = [1,target_id,self.turn_num]
                    elif target_information.flag == 1:
                        self.ai1_shield_flag = [1,target_id,self.turn_num]
                    my_information.reset_attribute(self.buff, skill_last_release_time2=self.turn_num)

        # 纳米研究科技技能2
        def nano_skill2(id, produce_num):
            my_information = Get_id_information(id)
            if (my_information != -1):
                skill_cd = self.turn_num - my_information.skill_last_release_time2
                ai_id = my_information.flag
                if produce_num >= 1 and produce_num <= 8:
                    produce_name=name[produce_num]
                    produce_type=type[produce_num]
                    if (skill_cd >= origin_attribute['nano_lab']['skill_cd_2']):
                        if self.resource[ai_id]['remain_people'] < unit.origin_attribute[produce_name]['people_cost'] or self.resource[ai_id]['money'] < unit.origin_attribute[produce_name][ 'money_cost'] * (1 - self.buff[ai_id][produce_type]['produce_buff']) or self.resource[ai_id]['tech'] < unit.origin_attribute[produce_name]['tech_cost'] * (1 - self.buff[ai_id][produce_type]['produce_buff']):
                            pass
                        elif produce_num != 3 and produce_num != 6 and produce_num != 8:
                            weapon = unit.UnitObject(self.total_id, ai_id, produce_name,my_information.position,self.buff)
                            self.resource[ai_id]['remain_people'] -= unit.origin_attribute[produce_name]['people_cost']
                            self.resource[ai_id]['money'] -= int(unit.origin_attribute[produce_name]['money_cost'] * (1 - self.buff[ai_id][produce_type]['produce_buff']))
                            self.resource[ai_id]['tech'] -= int(unit.origin_attribute[produce_name]['tech_cost'] * (1 - self.buff[ai_id][produce_type]['produce_buff']))
                            self.units[self.total_id] = weapon
                            self.total_id += 1
                        elif self.amount_limit[ai_id][produce_name] == False:
                            weapon = unit.UnitObject(self.total_id, ai_id, produce_name, my_information.position,self.buff)
                            self.resource[ai_id]['remain_people'] -= unit.origin_attribute[produce_name]['people_cost']
                            self.resource[ai_id]['money'] -= int(unit.origin_attribute[produce_name]['money_cost'] * (1 - self.buff[ai_id][produce_type]['produce_buff']))
                            self.resource[ai_id]['tech'] -= int(unit.origin_attribute[produce_name]['tech_cost'] * (1 - self.buff[ai_id][produce_type]['produce_buff']))
                            self.units[self.total_id] = weapon
                            self.total_id += 1
                            self.amount_limit[ai_id][produce_name] = True
                        my_information.reset_attribute(self.buff, skill_last_release_time2=self.turn_num)

        for k in range(len(order)):
            #print("-------------------------------")
            #print(len(order))
            #print(Get_id_information(order[k][1]).Get_type_name())
            if (Get_id_information(order[k][1]).Get_type_name() == 0 and  len(order[k]) >= 4):#'base'
                base_skill1(order[k][1], order[k][2], order[k][3])
            elif (Get_id_information(order[k][1]).Get_type_name() == 5):#'bolt_tank'
                bolt_tank_skill1(order[k][1], order[k][2])
                #print('use skill1')
            elif (Get_id_information(order[k][1]).Get_type_name() == 2):#'hacker'
                hacker_skill1(order[k][1], order[k][2])
                #print('use skill2')
            elif (Get_id_information(order[k][1]).Get_type_name() == 7):#'uav'
                uav(order[k][1], order[k][2])
                #print('use skill3')
            elif (Get_id_information(order[k][1]).Get_type_name() == 4):#'battle_tank'
                battle_tank_skill1(order[k][1], order[k][2])
                #print('use skill4')
            elif (Get_id_information(order[k][1]).Get_type_name() == 6 and order[k][0]==1):#'nuke_tank'
                nuke_tank_skill1(order[k][1], order[k][2])
                #print('use skill5')
            elif (Get_id_information(order[k][1]).Get_type_name() == 6 and order[k][0]==2 and len(order[k])>=4):#'nuke_tank'
                nuke_tank_skill2(order[k][1], order[k][2],order[k][3])
                #print('use skill6')
            elif (Get_id_information(order[k][1]).Get_type_name() == 8 and order[k][0]==1 and len(order[k])>=4):#'eagle'
                eagle_skill1(order[k][1], order[k][2],order[k][3])
                #print('use skill7')
            elif (Get_id_information(order[k][1]).Get_type_name() == 8 and order[k][0]==2 and len(order[k])>=6):#'eagle'
                eagle_skill2(order[k][1], order[k][2], order[k][3],order[k][4], order[k][5])
                #print('use skill8')
            elif (Get_id_information(order[k][1]).Get_type_name() == 3 and order[k][0]==1):#'superman'
                superman_skill1(order[k][1], order[k][2])
                #print('use skill9')
            elif (Get_id_information(order[k][1]).Get_type_name() == 3 and order[k][0]==2):#'superman'
                superman_skill2(order[k][1])
                #print('use skill0')
            elif (Get_id_information(order[k][1]).Get_type_name() == 16 and len(order[k])>=4):
                construct_skill2(order[k][1],order[k][2],order[k][3])
            elif (Get_id_information(order[k][1]).Get_type_name() == 17):
                society_skill2(order[k][1],order[k][2])
            elif (Get_id_information(order[k][1]).Get_type_name() == 18):
                material_skill2(order[k][1],order[k][2])
            elif (Get_id_information(order[k][1]).Get_type_name() == 19):
                nano_skill2(order[k][1],order[k][2])
        pass

    def move_phase(self):
        # 移动指令结算
        flag = 1
        id_collection = list(self.units.values())  # 寻找传入ai_id对应的value(unitobject)
        for things in self.move_instr_0:
            flag = 1
            for obj in id_collection:
                if obj.unit_id == things[0]:  # 如果unit_id 相符
                    if obj.Get_unit_type() == 0 or obj.Get_unit_type() == 4 or obj.flag != 0:
                        pass
                    else:
                        x = things[1]
                        y = things[2]
                        x1 = obj.position[0]
                        y1 = obj.position[1]
                        if x >= 100 or y >= 100 or x < 0 or y < 0:
                            pass
                        elif abs(x1 - x) + abs(y1 - y) <= obj.max_speed_now:
                            for obj_1 in id_collection:
                                if obj_1.position[0] == x and obj_1.position[1] == y and obj_1.Get_unit_type() == 4 and obj.Get_unit_type != 3:
                                    flag = 0
                            if flag ==1:
                                obj.position = [x,y]
                        else:
                            pass

        for things in self.move_instr_1:
            flag = 1
            for obj in id_collection:
                if obj.unit_id == things[0]:  # 如果unit_id 相符
                    if obj.Get_unit_type() == 0 or obj.Get_unit_type() == 4 or obj.flag == 0:
                        pass
                    else:
                        x = things[1]
                        y = things[2]
                        x1 = obj.position[0]
                        y1 = obj.position[1]
                        if x >= 100 or y >= 100 or x < 0 or y < 0:
                            pass
                        elif abs(x1 - x) + abs(y1 - y) <= obj.max_speed_now:
                            for obj_1 in id_collection:
                                if obj_1.position[0] == x and obj_1.position[1] == y and obj_1.Get_unit_type() == 4 and obj.Get_unit_type != 3:
                                    flag = 0
                            if flag ==1:
                                obj.position = [x,y]
                        else:
                            pass

        pass

    def produce_phase(self):
        #print(self.produce_instr_0)
        ai_id = 0
        tempcorrection=self.produce_instr_0.copy()
        for building_id in tempcorrection:
            del self.produce_instr_0[0]
            if self.units[building_id].flag !=0:
                continue
            if self.units[building_id].Get_type_name() == 9:#黑客学院
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['hacker']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['hacker']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['hacker']['tech_cost']:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'hacker', self.units[building_id].position, self.buff)
                self.resource[ai_id]['money'] -= unit.origin_attribute['hacker']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['hacker']['tech_cost']
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['hacker']['people_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 10:#生化研究院
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['superman']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['superman']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['superman']['tech_cost'] or \
                                self.amount_limit[ai_id]['superman'] == True:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'superman', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['superman']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['superman']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['superman']['tech_cost']
                self.amount_limit[ai_id]['superman'] = True
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 11:#特殊车辆系
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['battle_tank']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['battle_tank']['money_cost']*(1-self.buff[0][2]['produce_buff']) or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['battle_tank']['tech_cost']*(1-self.buff[0][2]['produce_buff']):
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'battle_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['battle_tank']['people_cost']
                self.resource[ai_id]['money'] -= int(unit.origin_attribute['battle_tank']['money_cost']*(1-self.buff[0][2]['produce_buff']))
                self.resource[ai_id]['tech'] -= int(unit.origin_attribute['battle_tank']['tech_cost']*(1-self.buff[0][2]['produce_buff']))
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 12:#电子对抗学院
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['bolt_tank']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['bolt_tank']['money_cost']*(1-self.buff[0][2]['produce_buff']) or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['bolt_tank']['tech_cost']*(1-self.buff[0][2]['produce_buff']):
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'bolt_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['bolt_tank']['people_cost']
                self.resource[ai_id]['money'] -= int(unit.origin_attribute['bolt_tank']['money_cost']*(1-self.buff[0][2]['produce_buff']))
                self.resource[ai_id]['tech'] -= int(unit.origin_attribute['bolt_tank']['tech_cost']*(1-self.buff[0][2]['produce_buff']))
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 13:#辐射系
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['nuke_tank']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['nuke_tank']['money_cost']*(1-self.buff[0][2]['produce_buff']) or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['nuke_tank']['tech_cost']*(1-self.buff[0][2]['produce_buff']) or \
                                self.amount_limit[ai_id]['nuke_tank'] == True:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'nuke_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['nuke_tank']['people_cost']
                self.resource[ai_id]['money'] -= int(unit.origin_attribute['nuke_tank']['money_cost']*(1-self.buff[0][2]['produce_buff']))
                self.resource[ai_id]['tech'] -= int(unit.origin_attribute['nuke_tank']['tech_cost']*(1-self.buff[0][2]['produce_buff']))
                self.amount_limit[ai_id]['nuke_tank'] = True
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 14:#无人机系
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['uav']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['uav']['money_cost']*(1-self.buff[0][3]['produce_buff']) or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['uav']['tech_cost']*(1-self.buff[0][3]['produce_buff']):
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'uav', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['uav']['people_cost']
                self.resource[ai_id]['money'] -= int(unit.origin_attribute['uav']['money_cost']*(1-self.buff[0][3]['produce_buff']))
                self.resource[ai_id]['tech'] -= int(unit.origin_attribute['uav']['tech_cost']*(1-self.buff[0][3]['produce_buff']))
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 15:#高等飞行器研究院
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['eagle']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['eagle']['money_cost']*(1-self.buff[0][3]['produce_buff']) or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['eagle']['tech_cost']*(1-self.buff[0][3]['produce_buff']) or \
                                self.amount_limit[ai_id]['eagle'] == True:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'eagle', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['eagle']['people_cost']
                self.resource[ai_id]['money'] -= int(unit.origin_attribute['eagle']['money_cost']*(1-self.buff[0][3]['produce_buff']))
                self.resource[ai_id]['tech'] -= int(unit.origin_attribute['eagle']['tech_cost']*(1-self.buff[0][3]['produce_buff']))
                self.amount_limit[ai_id]['eagle'] = True
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 0:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['meat']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['meat']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['meat']['tech_cost']:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'meat', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['meat']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['meat']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['meat']['tech_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
        ai_id = 1
        tempcorrection=self.produce_instr_1.copy()
        for building_id in tempcorrection:
            del self.produce_instr_1[0]
            if self.units[building_id].flag !=1:
                continue
            if self.units[building_id].Get_type_name() == 9:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['hacker']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['hacker']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['hacker']['tech_cost']:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'hacker', self.units[building_id].position, self.buff)
                self.resource[ai_id]['money'] -= unit.origin_attribute['hacker']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['hacker']['tech_cost']
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['hacker']['people_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 10:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['superman']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['superman']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['superman']['tech_cost'] or \
                                self.amount_limit[ai_id]['superman'] == True:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'superman', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['superman']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['superman']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['superman']['tech_cost']
                self.amount_limit[ai_id]['superman'] = True
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 11:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['battle_tank']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['battle_tank']['money_cost']*(1-self.buff[1][2]['produce_buff']) or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['battle_tank']['tech_cost']*(1-self.buff[1][2]['produce_buff']):
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'battle_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['battle_tank']['people_cost']
                self.resource[ai_id]['money'] -= int(unit.origin_attribute['battle_tank']['money_cost']*(1-self.buff[1][2]['produce_buff']))
                self.resource[ai_id]['tech'] -= int(unit.origin_attribute['battle_tank']['tech_cost']*(1-self.buff[1][2]['produce_buff']))
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 12:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['bolt_tank']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['bolt_tank']['money_cost']*(1-self.buff[1][2]['produce_buff']) or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['bolt_tank']['tech_cost']*(1-self.buff[1][2]['produce_buff']):
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'bolt_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['bolt_tank']['people_cost']
                self.resource[ai_id]['money'] -= int(unit.origin_attribute['bolt_tank']['money_cost']*(1-self.buff[1][2]['produce_buff']))
                self.resource[ai_id]['tech'] -= int(unit.origin_attribute['bolt_tank']['tech_cost']*(1-self.buff[1][2]['produce_buff']))
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 13:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['nuke_tank']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['nuke_tank']['money_cost']*(1-self.buff[1][2]['produce_buff']) or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['nuke_tank']['tech_cost']*(1-self.buff[1][2]['produce_buff']) or \
                                self.amount_limit[ai_id]['nuke_tank'] == True:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'nuke_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['nuke_tank']['people_cost']
                self.resource[ai_id]['money'] -= int(unit.origin_attribute['nuke_tank']['money_cost']*(1-self.buff[1][2]['produce_buff']))
                self.resource[ai_id]['tech'] -= int(unit.origin_attribute['nuke_tank']['tech_cost']*(1-self.buff[1][2]['produce_buff']))
                self.amount_limit[ai_id]['nuke_tank'] = True
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 14:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['uav']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['uav']['money_cost'] *(1-self.buff[1][3]['produce_buff'])or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['uav']['tech_cost']*(1-self.buff[1][3]['produce_buff']):
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'uav', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['uav']['people_cost']
                self.resource[ai_id]['money'] -= int(unit.origin_attribute['uav']['money_cost']*(1-self.buff[1][3]['produce_buff']))
                self.resource[ai_id]['tech'] -= int(unit.origin_attribute['uav']['tech_cost']*(1-self.buff[1][3]['produce_buff']))
                self.units[self.total_id] = weapon
                self.total_id += 1
                #print(unit.origin_attribute['uav']['money_cost']*(1-self.buff[1][3]['produce_buff']))
                continue
            if self.units[building_id].Get_type_name() == 15:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['eagle']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['eagle']['money_cost']*(1-self.buff[1][3]['produce_buff']) or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['eagle']['tech_cost']*(1-self.buff[1][3]['produce_buff']) or \
                                self.amount_limit[ai_id]['eagle'] == True:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'eagle', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['eagle']['people_cost']
                self.resource[ai_id]['money'] -= int(unit.origin_attribute['eagle']['money_cost']*(1-self.buff[1][3]['produce_buff']))
                self.resource[ai_id]['tech'] -= int(unit.origin_attribute['eagle']['tech_cost']*(1-self.buff[1][3]['produce_buff']))
                self.amount_limit[ai_id]['eagle'] = True
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 0:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['meat']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['meat']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['meat']['tech_cost']:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'meat', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['meat']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['meat']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['meat']['tech_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
        # 兵种获取指令结算
        pass

    def resource_phase(self):
        # 资源及单位状态结算阶段
        for unit_id in self.units.values():
            if unit_id.flag == -1:
                continue
            if unit_id.Get_type_name() == 21:
                if self.buff[unit_id.flag][0]['economy_buff'] > 0.1: #-1.0+1.0不一定为0，所以可以稍微大一点，因为最小有效值是1.0
                    self.resource[unit_id.flag]["money"] += 50
                elif self.buff[unit_id.flag][0]['economy_buff'] < -0.1:
                    self.resource[unit_id.flag]["money"] += 40
                else:
                    self.resource[unit_id.flag]["money"] += 45
            if unit_id.Get_type_name() == 20:
                if self.buff[unit_id.flag][0]['tech_buff'] > 0.1:
                    self.resource[unit_id.flag]["tech"] += 25
                elif self.buff[unit_id.flag][0]['tech_buff'] < -0.1:

                    self.resource[unit_id.flag]["tech"] += 15
                else:
                    self.resource[unit_id.flag]["tech"] += 20

        if self.ai0_shield_flag[0] == 1 and self.turn_num - self.ai0_shield_flag[2] > 10:
            for u in self.units.values():
                if u.unit_id == self.ai0_shield_flag[1]:
                    u.reset_attribute(self.buff, defense = unit.origin_attribute[name[u.Get_type_name()]]['origin_defense'])
                    self.ai0_shield_flag[0] = 0
        if self.ai1_shield_flag[0] == 1 and self.turn_num - self.ai1_shield_flag[2] > 10:
            for u in self.units.values():
                if u.unit_id == self.ai1_shield_flag[1]:
                    u.reset_attribute(self.buff, defense = unit.origin_attribute[name[u.Get_type_name()]]['origin_defense'])
                    self.ai1_shield_flag[0] = 0.

        for u in self.units.values():
            if  u.Get_unit_type() != 4:
                health_percentage = u.health_now/u.max_health_now
                my_type_name=u.Get_type_name()
                my_unit_type=u.Get_unit_type()
                u.reset_attribute(self.buff,max_health = origin_attribute[name[my_type_name]]['origin_max_health'] *(1 + self.buff[u.flag][my_unit_type]['health_buff']))
                u.reset_attribute(self.buff,health = u.max_health_now * health_percentage)
                u.reset_attribute(self.buff,attack = origin_attribute[name[my_type_name]]['origin_attack'] * (1 + self.buff[u.flag][my_unit_type]['attack_buff']))
                if u.flag==0 and u.unit_id==self.ai0_shield_flag[1]:
                    pass
                elif u.flag==1 and u.unit_id==self.ai1_shield_flag[1]:
                    pass
                else:
                    u.reset_attribute(self.buff,defense = origin_attribute[name[my_type_name]]['origin_defense'] * (1 + self.buff[u.flag][my_unit_type]['defense_buff']))
                u.reset_attribute(self.buff,shot_range = origin_attribute[name[my_type_name]]['origin_shot_range'] + self.buff[u.flag][my_unit_type]['shot_range_buff'])
                if(my_unit_type != 0 and my_type_name != 3):
                    u.reset_attribute(self.buff,speed = origin_attribute[name[my_type_name]]['origin_max_speed'] + self.buff[u.flag][my_unit_type]['speed_buff'])
                if (my_type_name == 3 and u.motor_type == 1 and self.buff[u.flag][my_unit_type]["speed_buff"] >0):
                    u.reset_attribute(self.buff, speed= 12 + self.buff[u.flag][my_unit_type]['speed_buff'])
                elif (my_type_name == 3 and u.motor_type == 0 and self.buff[u.flag][my_unit_type]["speed_buff"] >0):
                    u.reset_attribute(self.buff, speed= 4 + self.buff[u.flag][my_unit_type]['speed_buff'])
                if(u.health_now + u.healing_rate * u.max_health_now >= u.max_health_now):
                    new_health = u.max_health_now
                else:
                    new_health = u.health_now + u.healing_rate * u.max_health_now
                u.reset_attribute(self.buff, health = new_health)
                if(u.is_disable == True and self.turn_num-u.disable_since>=5):
                    u.reset_attribute(self.buff,is_disable=False)
                if u.Get_type_name() == 8 and u.flag == 0 and self.ai0_eagle_flag == 1 and self.turn_num - u.skill_last_release_time2 > 10:
                    self.ai0_eagle_flag = 0
                    u.reset_attribute(self.buff, speed=u.max_speed_now - 5)
                if u.Get_type_name() == 8 and u.flag == 1 and self.ai1_eagle_flag == 1 and self.turn_num - u.skill_last_release_time2 > 10:
                    self.ai1_eagle_flag = 1
                    u.reset_attribute(self.buff, speed=u.max_speed_now - 5)
                if u.Get_type_name() == 3 and u.motor_type == 1 and self.turn_num - u.skill_last_release_time2 > 20:
                    u.reset_attribute(self.buff, speed = 4.0, motor_type=0)


        pass

    def capture_phase(self):
        # 占领建筑阶段
        current_pointer = {}
        unit_obj = list(self.units.values())
        unit_building=list(self.buildings)
        for x in unit_building:
            current_pointer[x.unit_id]=0
        for orders in self.capture_instr_0:#AI0_capture
            for things in unit_obj:
                if orders[0] == things.unit_id and things.Get_type_name() == 1 and things.flag == 0:
                    for k in unit_building:
                        if k.unit_id == orders[1] and k.Get_unit_type() == 4 and abs(things.position[0] - k.position[0]) + abs(things.position[1] - k.position[1]) == 1:
                            current_pointer[k.unit_id] += 1
                    things.health_now=0

        for orders in self.capture_instr_1:#AI1_capture
            for things in unit_obj:
                if orders[0] == things.unit_id and things.Get_type_name() == 1 and things.flag == 1:
                    for k in unit_building:
                        if k.unit_id == orders[1] and k.Get_unit_type() == 4 and abs(things.position[0] - k.position[0]) + abs(things.position[1] - k.position[1]) == 1:
                            current_pointer[k.unit_id] -= 1
                    things.health_now=0

        for obj in unit_building:  # 结算建筑都是哪一方的
            if current_pointer[obj.unit_id] > 0:
                obj.flag = 0
            if current_pointer[obj.unit_id] < 0:
                obj.flag = 1
            if current_pointer[obj.unit_id] == 0:
                pass

        #先将Buff置0，然后不同建筑加和，避免丢失建筑后还遗留Buff
        for flag in [unit.FLAG_0, unit.FLAG_1]:
            for unit_type in [unit.BASE, unit.INFANTRY, unit.VEHICLE, unit.AIRCRAFT]:
                for key in self.buff[flag][unit_type]:
                    self.buff[flag][unit_type][key] = 0.0

        for units in unit_building:#根据建筑的flag结算被动效果
            if units.Get_type_name() == 9:
                if units.flag == 0:
                    self.buff[unit.FLAG_0][unit.BASE]['tech_buff'] += 1.0
                    self.buff[unit.FLAG_1][unit.BASE]['tech_buff'] += -1.0
                if units.flag == 1:
                    self.buff[unit.FLAG_1][unit.BASE]['tech_buff'] += 1.0
                    self.buff[unit.FLAG_0][unit.BASE]['tech_buff'] += -1.0
            if units.Get_type_name() == 10:#生化研究院
                if units.flag == 0:
                    self.buff[unit.FLAG_0][unit.INFANTRY]['health_buff'] = 0.5
                    self.buff[unit.FLAG_0][unit.INFANTRY]['attack_buff'] = 0.1
                if units.flag == 1:
                    self.buff[unit.FLAG_1][unit.INFANTRY]['health_buff'] = 0.5
                    self.buff[unit.FLAG_1][unit.INFANTRY]['attack_buff'] = 0.1
            if units.Get_type_name() == 11:#特种车辆系
                if units.flag == 0:
                    self.buff[unit.FLAG_0][unit.VEHICLE]['defense_buff'] = 0.15
                    self.buff[unit.FLAG_0][unit.VEHICLE]['speed_buff'] = 3.0
                if units.flag == 1:
                    self.buff[unit.FLAG_1][unit.VEHICLE]['defense_buff'] = 0.15
                    self.buff[unit.FLAG_1][unit.VEHICLE]['speed_buff'] = 3.0
            if units.Get_type_name() == 12:#电子对抗系
                if units.flag == 0:
                    self.buff[unit.FLAG_0][unit.VEHICLE]['shot_range_buff'] = 4.0
                if units.flag == 1:
                    self.buff[unit.FLAG_1][unit.VEHICLE]['shot_range_buff'] = 4.0
            if units.Get_type_name() == 13:#辐射系
                if units.flag == 0:
                    self.buff[unit.FLAG_0][unit.VEHICLE]['attack_buff'] = 0.2
                if units.flag == 1:
                    self.buff[unit.FLAG_1][unit.VEHICLE]['attack_buff'] = 0.2
            if units.Get_type_name() == 14:#无人机
                if units.flag == 0:
                    self.buff[unit.FLAG_0][unit.VEHICLE]['produce_buff'] = 0.1
                    self.buff[unit.FLAG_0][unit.AIRCRAFT]['produce_buff'] = 0.1
                if units.flag == 1:
                    self.buff[unit.FLAG_1][unit.VEHICLE]['produce_buff'] = 0.1
                    self.buff[unit.FLAG_1][unit.AIRCRAFT]['produce_buff'] = 0.1
            if units.Get_type_name() == 15:#高等飞行研究院
                if units.flag == 0:
                    self.buff[unit.FLAG_0][unit.AIRCRAFT]['speed_buff'] = 3.0
                    self.buff[unit.FLAG_0][unit.AIRCRAFT]['attack_buff'] = 0.15
                if units.flag == 1:
                    self.buff[unit.FLAG_1][unit.AIRCRAFT]['speed_buff'] = 3.0
                    self.buff[unit.FLAG_1][unit.AIRCRAFT]['attack_buff'] = 0.15
            if units.Get_type_name() == 16: #建筑土木学院
                if units.flag == 0:
                    self.buff[unit.FLAG_0][unit.BASE]['defense_buff'] = 2.0
                    self.buff[unit.FLAG_0][unit.BASE]['attack_buff'] = 0.5
                if units.flag == 1:
                    self.buff[unit.FLAG_1][unit.BASE]['defense_buff'] = 2.0
                    self.buff[unit.FLAG_1][unit.BASE]['attack_buff'] = 1.0
            if units.Get_type_name() == 17:  # 社会金融学院
                if units.flag == 0:
                    self.buff[unit.FLAG_0][unit.BASE]['economy_buff'] += 1.0
                    self.buff[unit.FLAG_1][unit.BASE]['economy_buff'] += -1.0
                if units.flag == 1:
                    self.buff[unit.FLAG_1][unit.BASE]['economy_buff'] += 1.0
                    self.buff[unit.FLAG_0][unit.BASE]['economy_buff'] += -1.0
            if units.Get_type_name() == 18:  # 特殊材料学院
                if units.flag == 0:
                    self.buff[unit.FLAG_0][unit.INFANTRY]['speed_buff'] = 5.0
                if units.flag == 1:
                    self.buff[unit.FLAG_1][unit.INFANTRY]['speed_buff'] = 5.0
            if units.Get_type_name() == 19:  # 纳米研究学院
                if units.flag == 0:
                    self.ai0_healing_flag = 1
                if units.flag == 1:
                    self.ai1_healing_flag = 1
            for u in self.units.values():
                if ((u.flag == 0 and self.ai0_healing_flag == 1) or (u.flag == 1 and self.ai1_healing_flag == 1)) and (u.Get_unit_type() == 2 or u.Get_unit_type() == 3):
                    u.reset_attribute(self.buff, healing_rate = 0.025)
                else:
                    u.reset_attribute(self.buff, healing_rate = 0)
        #print(self.buff)

    def fetch_instruction(self):
        # 获取指令存入两个指令list
        pass

    def check_legal(self):
        # 检查双方指令是否合法，去重
        temp_m_instr_0 = {}
        temp_m_instr_1 = {}
        for i in range(len(self.move_instr_0)):
            for things in self.units.values():
                if things.unit_id == self.move_instr_0[i][0] and things.flag == 0:  # 如果移动的是自己的单位
                    temp_m_instr_0[self.move_instr_0[i][0]] = self.move_instr_0[i]
                if things.unit_id == self.move_instr_0[i][0] and things.flag == 1:  # 如果移动的不是自己的单位
                    pass
        self.move_instr_0 = list(temp_m_instr_0.values())
        for i in range(len(self.move_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.move_instr_1[i][0] and things.flag == 1:  # 如果移动的是自己的单位
                    temp_m_instr_1[self.move_instr_1[i][0]] = self.move_instr_1[i]
                if things.unit_id == self.move_instr_1[i][0] and things.flag == 0:  # 如果移动的不是自己的单位
                    pass
        self.move_instr_1 = list(temp_m_instr_1.values())

        temp_c_instr_0 = {}
        temp_c_instr_1 = {}
        for i in range(len(self.capture_instr_0)):
            for things in self.units.values():
                if things.unit_id == self.capture_instr_0[i][0] and things.flag == 0:  # 如果移动的是自己的单位
                    temp_c_instr_0[self.capture_instr_0[i][0]] = self.capture_instr_0[i]
                if things.unit_id == self.capture_instr_0[i][0] and things.flag == 1:  # 如果移动的不是自己的单位
                    pass
        self.capture_instr_0 = list(temp_c_instr_0.values())
        #print(len(self.capture_instr_1))
        for i in range(len(self.capture_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.capture_instr_1[i][0] and things.flag == 1:  # 如果移动的是自己的单位
                    temp_c_instr_1[self.capture_instr_1[i][0]] = self.capture_instr_1[i]
                if things.unit_id == self.capture_instr_1[i][0] and things.flag == 0:  # 如果移动的不是自己的单位
                    pass
        self.capture_instr_1 = list(temp_c_instr_1.values())
        #print(len(self.capture_instr_1))
        #print("******************************")

        temp_p_instr_1 = {}
        temp_p_instr_0 = {}
        #print(len(self.produce_instr_0))
        for i in range(len(self.produce_instr_0)):
            for things in self.units.values():
                if things.unit_id == self.produce_instr_0[i] and things.flag == 0:  # 如果移动的是自己的单位
                    temp_p_instr_0[self.produce_instr_0[i]] = self.produce_instr_0[i]
                if things.unit_id == self.produce_instr_0[i] and things.flag == 1:  # 如果移动的不是自己的单位
                    pass
        self.produce_instr_0 = list(temp_p_instr_0.values())
        #print(len(self.produce_instr_0))
        #print("******************************")

        #print(len(self.produce_instr_1))
        for i in range(len(self.produce_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.produce_instr_1[i] and things.flag == 1:  # 如果移动的是自己的单位
                    temp_p_instr_1[self.produce_instr_1[i]] = self.produce_instr_1[i]
                if things.unit_id == self.produce_instr_1[i] and things.flag == 0:  # 如果移动的不是自己的单位
                    pass
        self.produce_instr_1 = list(temp_p_instr_1.values())
        #print(len(self.produce_instr_1))
        #print("******************************")

        temp_s_instr_0 = {}
        temp_s_instr_1 = {}
        #print(len(self.skill_instr_0))
        for i in range(len(self.skill_instr_0)):
            for things in self.units.values():
                if things.unit_id == self.skill_instr_0[i][1] and things.flag == 0:  # 如果移动的是自己的单位
                    temp_s_instr_0[self.skill_instr_0[i][1]] = self.skill_instr_0[i]
                if things.unit_id == self.skill_instr_0[i][1] and things.flag == 1:  # 如果移动的不是自己的单位
                    pass
        self.skill_instr_0 = list(temp_s_instr_0.values())
        #print(len(self.skill_instr_0))
       # print("******************************")

        #print(len(self.skill_instr_1))
        for i in range(len(self.skill_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.skill_instr_1[i][1] and things.flag == 1:  # 如果移动的是自己的单位
                    temp_s_instr_1[self.skill_instr_1[i][1]] = self.skill_instr_1[i]
                if things.unit_id == self.skill_instr_1[i][1] and things.flag == 0:  # 如果移动的不是自己的单位
                    pass
        self.skill_instr_1 = list(temp_s_instr_1.values())
        #print(len(self.skill_instr_1))
        #print("******************************")

    def next_tick(self):
        # 获取指令，指令检测合法与去重，回合演算
        #print(self.skill_instr_0)
        #print("before HP0:", self.hqs[0].health_now, "before HP1:", self.hqs[1].health_now)
        self.check_legal()
        self.skill_phase(self.skill_instr_0)
        self.skill_phase(self.skill_instr_1)
        #print("HP0:",self.hqs[0].health_now,"HP1:",self.hqs[1].health_now)
        self.cleanup_phase()
        self.check_winner=self.win_determine()
        #print("produce instr_0:", len(self.produce_instr_0), "move instr_0:", len(self.move_instr_0), "cap instr_0:",len(self.capture_instr_0), "skill instr_0:", len(self.skill_instr_0))
        #print("produce instr_1:", len(self.produce_instr_1), "move instr_1:", len(self.move_instr_1), "cap instr_1:",len(self.capture_instr_1), "skill instr_1:", len(self.skill_instr_1))
        if (self.check_winner == 3):
            self.move_phase()
            self.produce_phase()
            self.resource_phase()
            self.capture_phase()
            self.cleanup_phase()
        check_timeup =self.timeup_determine()
        #print("after HP0:", self.hqs[0].health_now, "after HP1:", self.hqs[1].health_now)
        ai0 = {}
        ai1 = {}
        for x in range(22):
            ai0[x]=0
            ai1[x]=0
        for u in self.units.values():
            if u.flag==0:
                ai0[u.Get_type_name()] += 1
            if u.flag==1:
                ai1[u.Get_type_name()] += 1
        #print(ai0)
        #print(ai1)
        self.skill_instr_0 = []  # ai0的当前回合指令
        self.skill_instr_1 = []  # ai1的当前回合制令
        self.produce_instr_0 = []  # 指令格式为[building_id,building_id,]
        self.produce_instr_1 = []
        self.move_instr_0 = []  # 指令格式[[unit_id,position_x,position_y],[unit_id,position_x,position_y]]
        self.move_instr_1 = []
        self.capture_instr_0 = []  # 指令格式[[unit_id,building_id][unit_id,building_id][]]
        self.capture_instr_1 = []
        self.turn_num+=1
        if(self.check_winner==3 and check_timeup==3):
            pass
        elif(self.check_winner!=3):
            print("winner is",self.check_winner,"!!")
            self.is_end = True
        else :
            print("winner is", check_timeup, "!!")
            self.is_end = True
            self.check_winner = check_timeup
    def to_string(self):
        # 将当前状态信息返回，用String,Json什么都行，你们自己起名字吧
        pass

