#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unit
from unit import origin_attribute
import random
from random import choice
import time
MAXROUND = 1000


class GameMain:
    units = {}  # 单位dict key:unit_id value:unitobject
    hqs = []  # 主基地
    buildings = []  # 中立建筑
    # turn_flag = 0  # 谁的回合
    is_end = False
    check_winner = 3 #胜利者
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
    superman_motortype = [0,0]
    superman_skill_release_time = [0,0]
    buff = {
        unit.FLAG_0: {
            unit.INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                            'shot_range_buff': 0.0, 'produce_buff': 0.0},
            unit.VEHICLE: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                           'shot_range_buff': 0.0, 'produce_buff': 0.0},
            unit.AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                            'shot_range_buff': 0.0, 'produce_buff': 0.0}
        },
        unit.FLAG_1: {
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
    meat_count0 = 0
    meat_count1 = 0

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
        self.resource = {ai_id0: {"tech": 0, "money": 1000, "remain_people": 200},
                         ai_id1: {"tech": 0, "money": 1000, "remain_people": 200}}
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

        base0 = unit.UnitObject(self.total_id, ai_id0, 'base', (player0_x, player0_y), self.buff)
        self.units[self.total_id] = base0
        self.hqs.append(base0)
        self.total_id += 1
        base1 = unit.UnitObject(self.total_id, ai_id1, 'base', (player1_x, player1_y), self.buff)
        self.units[self.total_id] = base1
        self.hqs.append(base1)
        self.total_id += 1
        tech0 = unit.UnitObject(self.total_id, ai_id0, 'teach_building', (player0_x, player0_y + 2), self.buff)
        self.units[self.total_id] = tech0
        self.total_id += 1
        tech1 = unit.UnitObject(self.total_id, ai_id1, 'teach_building', (99 - player0_x, 97 - player0_y), self.buff)
        self.units[self.total_id] = tech1
        self.total_id += 1
        bank0 = unit.UnitObject(self.total_id, ai_id0, 'bank', (player0_x, player0_y - 2), self.buff)
        self.units[self.total_id] = bank0
        self.total_id += 1
        bank1 = unit.UnitObject(self.total_id, ai_id1, 'bank', (99 - player0_x, 101 - player0_y), self.buff)
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
                                        (tech_x, tech_y), self.buff)
                self.units[self.total_id] = tech0
                self.buildings.append(tech0)
                self.total_id += 1
                tech1 = unit.UnitObject(self.total_id, -1, 'teach_building',
                                        (tech_1_x, tech_1_y), self.buff)
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
                                        (bank_x, bank_y), self.buff)
                self.units[self.total_id] = bank0
                self.buildings.append(bank0)
                self.total_id += 1
                bank1 = unit.UnitObject(self.total_id, -1, 'bank',
                                        (bank_1_x, bank_1_y), self.buff)
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
                hack_lab0 = unit.UnitObject(self.total_id, -1, 'hack_lab', (building_x, building_y), self.buff)
                self.buildings.append(hack_lab0)
                self.units[self.total_id] = hack_lab0
                self.total_id += 1
                hack_lab1 = unit.UnitObject(self.total_id, -1, 'hack_lab', (99 - building_x, 99 - building_y),
                                            self.buff)
                self.units[self.total_id] = hack_lab1
                self.buildings.append(hack_lab1)
                self.total_id += 1
            if building_type == 2:
                bid_lab0 = unit.UnitObject(self.total_id, -1, 'bid_lab', (building_x, building_y), self.buff)
                self.buildings.append(bid_lab0)
                self.units[self.total_id] = bid_lab0
                self.total_id += 1
                bid_lab1 = unit.UnitObject(self.total_id, -1, 'bid_lab', (99 - building_x, 99 - building_y),
                                           self.buff)
                self.buildings.append(bid_lab1)
                self.units[self.total_id] = bid_lab1
                self.total_id += 1
            if building_type == 3:
                car_lab0 = unit.UnitObject(self.total_id, -1, 'car_lab', (building_x, building_y), self.buff)
                self.buildings.append(car_lab0)
                self.units[self.total_id] = car_lab0
                self.total_id += 1
                car_lab1 = unit.UnitObject(self.total_id, -1, 'car_lab', (99 - building_x, 99 - building_y),
                                           self.buff)
                self.units[self.total_id] = car_lab1
                self.buildings.append(car_lab1)
                self.total_id += 1
            if building_type == 4:
                elec_lab0 = unit.UnitObject(self.total_id, -1, 'elec_lab', (building_x, building_y), self.buff)
                self.buildings.append(elec_lab0)
                self.units[self.total_id] = elec_lab0
                self.total_id += 1
                elec_lab1 = unit.UnitObject(self.total_id, -1, 'elec_lab', (99 - building_x, 99 - building_y),
                                            self.buff)
                self.buildings.append(elec_lab1)
                self.units[self.total_id] = elec_lab1
                self.total_id += 1
            if building_type == 5:
                radiation_lab0 = unit.UnitObject(self.total_id, -1, 'radiation_lab', (building_x, building_y),
                                                 self.buff)
                self.buildings.append(radiation_lab0)
                self.units[self.total_id] = radiation_lab0
                self.total_id += 1
                radiation_lab1 = unit.UnitObject(self.total_id, -1, 'radiation_lab',
                                                 (99 - building_x, 99 - building_y), self.buff)
                self.buildings.append(radiation_lab1)
                self.units[self.total_id] = radiation_lab1
                self.total_id += 1
            if building_type == 6:
                uav_lab0 = unit.UnitObject(self.total_id, -1, 'uav_lab', (building_x, building_y), self.buff)
                self.buildings.append(uav_lab0)
                self.units[self.total_id] = uav_lab0
                self.total_id += 1
                uav_lab1 = unit.UnitObject(self.total_id, -1, 'uav_lab', (99 - building_x, 99 - building_y),
                                           self.buff)
                self.buildings.append(uav_lab1)
                self.units[self.total_id] = uav_lab1
                self.total_id += 1
            if building_type == 7:
                aircraft_lab0 = unit.UnitObject(self.total_id, -1, 'aircraft_lab', (building_x, building_y), self.buff)
                self.buildings.append(aircraft_lab0)
                self.units[self.total_id] = aircraft_lab0
                self.total_id += 1
                aircraft_lab1 = unit.UnitObject(self.total_id, -1, 'aircraft_lab', (99 - building_x, 99 - building_y),
                                                self.buff)
                self.units[self.total_id] = aircraft_lab1
                self.buildings.append(aircraft_lab1)
                self.total_id += 1
            if building_type == 8:
                build_lab0 = unit.UnitObject(self.total_id, -1, 'build_lab', (building_x, building_y), self.buff)
                self.buildings.append(build_lab0)
                self.units[self.total_id] = build_lab0
                self.total_id += 1
                build_lab1 = unit.UnitObject(self.total_id, -1, 'build_lab', (99 - building_x, 99 - building_y),
                                             self.buff)
                self.units[self.total_id] = build_lab1
                self.buildings.append(build_lab1)
                self.total_id += 1
            if building_type == 9:
                finance_lab0 = unit.UnitObject(self.total_id, -1, 'finance_lab', (building_x, building_y), self.buff)
                self.buildings.append(finance_lab0)
                self.units[self.total_id] = finance_lab0
                self.total_id += 1
                finance_lab1 = unit.UnitObject(self.total_id, -1, 'finance_lab', (99 - building_x, 99 - building_y),
                                               self.buff)
                self.units[self.total_id] = finance_lab1
                self.buildings.append(finance_lab1)
                self.total_id += 1
            if building_type == 10:
                material_lab0 = unit.UnitObject(self.total_id, -1, 'material_lab', (building_x, building_y), self.buff)
                self.buildings.append(material_lab0)
                self.units[self.total_id] = material_lab0
                self.total_id += 1
                material_lab1 = unit.UnitObject(self.total_id, -1, 'material_lab', (99 - building_x, 99 - building_y),
                                                self.buff)
                self.units[self.total_id] = material_lab1
                self.buildings.append(material_lab1)
                self.total_id += 1
            if building_type == 11:
                nano_lab0 = unit.UnitObject(self.total_id, -1, 'nano_lab', (building_x, building_y), self.buff)
                self.buildings.append(nano_lab0)
                self.units[self.total_id] = nano_lab0
                self.total_id += 1
                nano_lab1 = unit.UnitObject(self.total_id, -1, 'nano_lab', (99 - building_x, 99 - building_y),
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
        flag_0 = self.hqs[0].flag
        flag_1 = self.hqs[1].flag
        counter_01 = 0  # 0方的兵力
        counter_11 = 0  # 1方的兵力
        counter_02 = 0  # 0方的建筑数
        counter_12 = 0  # 1方的建筑数
        if self.hqs[0].health_now * self.hqs[1].health_now > 0 and self.hqs[0].health_now + self.hqs[
            1].health_now > 0:  # 如果双方主基地都正Hp
            return 3
        else:
            if self.hqs[0].health_now < self.hqs[1].health_now:
                return 1
            if self.hqs[0].health_now > self.hqs[1].health_now:
                return 0
            if self.hqs[0].health_now == self.hqs[1].health_now:
                for things in unit_obj:
                    if things.__unit_type == 1 or things.__unit_type == 2 or things.__unit_type == 3:
                        if things.flag == flag_0:
                            counter_01 += 1
                        if things.flag == flag_1:
                            counter_11 += 1
                    else:
                        if things.flag == flag_0:
                            counter_02 += 1
                        if things.flag == flag_1:
                            counter_12 += 1
                    if counter_01 > counter_11:
                        return 0
                    if counter_01 < counter_11:
                        return 1
                    if counter_01 == counter_11:
                        if counter_02 > counter_12:
                            return 0
                        if counter_02 < counter_12:
                            return 1
                        if counter_02 == counter_12:
                            return 2

    def timeup_determine(self):
        # 超时胜利判定
        if self.turn_num <= MAXROUND:
            return 3
        if self.turn_num > MAXROUND:  # 如果超过了最大回合数
            unit_obj = list(self.units.values())
            flag_0 = self.hqs[0].flag
            flag_1 = self.hqs[1].flag
            counter_01 = 0  # 0方的兵力
            counter_11 = 0  # 1方的兵力
            counter_02 = 0  # 0方的建筑数
            counter_12 = 0  # 1方的建筑数
            if self.hqs[0].health_now < self.hqs[1].health_now:
                return 1
            if self.hqs[0].health_now > self.hqs[1].health_now:
                return 0
            if self.hqs[0].health_now == self.hqs[1].health_now:
                for things in unit_obj:
                    if things.Get_unit_type() == 1 or things.Get_unit_type() == 2 or things.Get_unit_type() == 3:
                        if things.flag == flag_0:
                            counter_01 += 1
                        if things.flag == flag_1:
                            counter_11 += 1
                    else:
                        if things.flag == flag_0:
                            counter_02 += 1
                        if things.flag == flag_1:
                            counter_12 += 1
                    if counter_01 > counter_11:
                        return 0
                    if counter_01 < counter_11:
                        return 1
                    if counter_01 == counter_11:
                        if counter_02 > counter_12:
                            return 0
                        if counter_02 < counter_12:
                            return 1
                        if counter_02 == counter_12:
                            return 2

    def cleanup_phase(self):
        # 单位死亡判定
        # id_collection = [0,1]  # 寻找传入ai_id对应的value
        # for ai_id in id_collection:
        tempcache=self.units.copy()
        for unit_id in tempcache.keys():
            things = self.units[unit_id]
            if self.units[unit_id].health_now <= 0:
                del self.units[unit_id]  # 从字典的value列表中把死亡单位删除
                if things.Get_type_name() == 2:
                    self.resource[things.flag]['remain_people'] += origin_attribute['hacker']['people_cost']
                if things.Get_type_name() == 3:
                    self.resource[things.flag]['remain_people'] += origin_attribute['superman']['people_cost']
                    self.amount_limit[things.flag]['superman'] = False
                if things.Get_type_name() == 4:
                    self.resource[things.flag]['remain_people'] += origin_attribute['battle_tank']['people_cost']
                if things.Get_type_name() == 5:
                    self.resource[things.flag]['remain_people'] += origin_attribute['bolt_tank']['people_cost']
                if things.Get_type_name() == 6:
                    self.amount_limit[things.flag]['nuke_tank'] = False
                    self.resource[things.flag]['remain_people'] += origin_attribute['nuke_tank']['people_cost']
                if things.Get_type_name() == 7:
                    self.resource[things.flag]['remain_people'] += origin_attribute['uav']['people_cost']
                if things.Get_type_name() == 8:
                    self.resource[things.flag]['remain_people'] += origin_attribute['eagle']['people_cost']
                    self.amount_limit[things.flag]['eagle'] = False
                if things.Get_type_name() == 1:
                    self.resource[things.flag]['remain_people'] += origin_attribute['meat']['people_cost']
                    if things.flag == 0:
                        self.meat_count0 -= 1
                    if things.flag == 1:
                        self.meat_count1 -= 1
            if things.hacked_point >= things.max_health_now >= 0:
                del self.units[unit_id]  # 从字典里删除被黑了的单位
                if things.Get_type_name() == 4:
                    self.resource[things.flag]['remain_people'] += origin_attribute['battle_tank']['people_cost']
                if things.Get_type_name() == 5:
                    self.resource[things.flag]['remain_people'] += origin_attribute['bolt_tank']['people_cost']
                if things.Get_type_name() == 6:
                    self.resource[things.flag]['remain_people'] += origin_attribute['nuke_tank']['people_cost']
                    self.amount_limit[things.flag]['nuke_tank'] = False
                if things.Get_type_name() == 7:
                    self.resource[things.flag]['remain_people'] += origin_attribute['uav']['people_cost']
                if things.Get_type_name() == 8:
                    self.resource[things.flag]['remain_people'] += origin_attribute['eagle']['people_cost']
                    self.amount_limit[things.flag]['eagle'] = False
        pass

    def skill_phase(self, order):
        # 技能结算
        if(self.turn_num-self.superman_skill_release_time[0]>20):
            self.superman_motortype[0]=0
        if(self.turn_num-self.superman_skill_release_time[1]>20):
            self.superman_motortype[1]=0
        def Get_id_information(id):
            for k in self.units:
                if (k == id):
                    return self.units[k]
            if (self.hqs[0].unit_id == id):
                return self.hqs[0]

        def Get_distance(my_position, enemy_position):
            x = my_position[0] - enemy_position[0]
            y = my_position[1] - enemy_position[1]
            return (x * x + y * y) ** 0.5

        # 电子对抗坦克技能1 修改计算公式
        def bolt_tank_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, enemy_information.position)
            if (skill_cd >= origin_attribute['bolt_tank']['skill_cd_1'] and distance <= origin_attribute['bolt_tank'][
                'origin_shot_range']):
                if (my_information.flag != enemy_information.flag) and (enemy_information.Get_unit_type() == 3):
                    enemy_information.reset_attribute(self.buff,
                                                      health=enemy_information.health_now - my_information.attack_now * (
                                                      1 - enemy_information.defense_now / 1000))
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
                elif (my_information.flag != enemy_information.flag) and (enemy_information.Get_unit_type() == 2):
                    enemy_information.reset_attribute(self.buff, is_disable=True)
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 黑客技能1
        def hacker_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, enemy_information.position)
            if (skill_cd >= origin_attribute['hacker']['skill_cd_1'] and distance <= origin_attribute['hacker'][
                'origin_shot_range']):
                if (my_information.flag != enemy_information.flag) and (
                        enemy_information.Get_unit_type() == 3 or enemy_information.Get_unit_type() == 2):
                    enemy_information.reset_attribute(self.buff, hacked_point=enemy_information.hacked_point + 1)
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
                elif (my_information.flag == enemy_information.flag) and (
                        enemy_information.Get_unit_type() == 3 or enemy_information.Get_unit_type() == 2):
                    enemy_information.reset_attribute(self.buff, hacked_point=enemy_information.hacked_point - 1)
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 无人战机技能1
        def uav(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, enemy_information.position)
            if (skill_cd >= origin_attribute['uav']['skill_cd_1'] and distance <= origin_attribute['uav'][
                'origin_shot_range'] and (my_information.flag != enemy_information.flag)):
                if (
                                enemy_information.Get_unit_type() == 3 or enemy_information.Get_unit_type() == 2 or enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 0):
                    enemy_information.reset_attribute(self.buff,
                                                      health=enemy_information.health_now - my_information.attack_now * (
                                                      1 - enemy_information.defense_now / 1000))
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 主站坦克技能1
        def battle_tank_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, enemy_information.position)
            if (skill_cd >= origin_attribute['battle_tank']['skill_cd_1'] and distance <=
                origin_attribute['battle_tank']['origin_shot_range'] and (
                my_information.flag != enemy_information.flag)):
                if (
                                enemy_information.Get_unit_type() == 3 or enemy_information.Get_unit_type() == 2 or enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 0):
                    enemy_information.reset_attribute(self.buff,
                                                      health=enemy_information.health_now - my_information.attack_now * (
                                                      1 - enemy_information.defense_now / 1000))
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 核子坦克技能1
        def nuke_tank_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, enemy_information.position)
            if (skill_cd >= origin_attribute['nuke_tank']['skill_cd_1'] and distance <= origin_attribute['nuke_tank'][
                'origin_shot_range'] and (my_information.flag != enemy_information.flag)):
                if (
                            enemy_information.Get_unit_type() == 2 or enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 0):
                    enemy_information.reset_attribute(self.buff,
                                                      health=enemy_information.health_now - my_information.attack_now * (
                                                      1 - enemy_information.defense_now / 1000))
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 核子坦克技能2
        def nuke_tank_skill2(id, attack_range_x, attack_range_y):
            attack_range = [attack_range_x,attack_range_y]
            my_information = Get_id_information(id)
            skill_cd = self.turn_num - my_information.skill_last_release_time2
            distance = Get_distance(my_information.position, attack_range)
            if (skill_cd >= origin_attribute['nuke_tank']['skill_cd_2'] and distance <= origin_attribute['nuke_tank'][
                'origin_shot_range']):
                for k in self.units:
                    enemy_position = self.units[k].position
                    if (Get_distance(enemy_position, attack_range) < 2):
                        self.units[k].reset_attribute(self.buff, health=self.units[k].health_now - 800 * (
                      1 - self.units[k].defense_now / 1000))
                base_position = self.hqs[0].position
                if (Get_distance(base_position, attack_range) < 2):
                    self.hqs[0].reset_attribute(self.buff, health=self.hqs[0].health_now - 800 * (
                    1 - self.units[k].defense_now / 1000))
                base_position2 = self.hqs[1].position
                if (Get_distance(base_position2, attack_range) < 2):
                    self.hqs[1].reset_attribute(self.buff, health=self.hqs[1].health_now - 800 * (
                    1 - self.units[k].defense_now / 1000))
                my_information.reset_attribute(self.buff, skill_last_release_time2=self.turn_num)

        # 鹰式战斗机技能1
        def eagle_skill1(id, attack_range_x,attack_range_y):
            attack_range = [attack_range_x,attack_range_y]
            my_information = Get_id_information(id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, attack_range)
            if (skill_cd >= origin_attribute['eagle']['skill_cd_1'] and distance <= origin_attribute['eagle'][
                'origin_shot_range']):
                for k in self.units:
                    enemy_position = self.units[k].position
                    if (enemy_position == attack_range):
                        self.units[k].reset_attribute(self.buff,
                                                      health=self.units[k].health_now - my_information.attack_now * (
                                                      1 - self.units[k].defense_now / 1000))
                base_position = self.hqs[0].position
                if (base_position == attack_range):
                    self.hqs[0].reset_attribute(self.buff, health=self.hqs[0].health_now - my_information.attack_now * (
                    1 - self.units[k].defense_now / 1000))
                base_position2 = self.hqs[1].position
                if (base_position2 == attack_range):
                    self.hqs[1].reset_attribute(self.buff, health=self.hqs[1].health_now - my_information.attack_now * (
                        1 - self.units[k].defense_now / 1000))
                my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 鹰式战斗机技能2
        def eagle_skill2(id, attack_range_x1,attack_range_y1,attack_range_x2, attack_range_y2):
            attack_range1 = [attack_range_x1,attack_range_y1]
            attack_range2 = [attack_range_x2,attack_range_y2]
            my_information = Get_id_information(id)
            skill_cd = self.turn_num - my_information.skill_last_release_time2
            distance1 = Get_distance(my_information.position, attack_range1)
            distance2 = Get_distance(my_information.position, attack_range2)
            if (skill_cd >= origin_attribute['eagle']['skill_cd_2'] and distance1 <= origin_attribute['eagle'][
                'origin_shot_range'] and distance2 <= origin_attribute['eagle']['origin_shot_range']):
                for k in self.units:
                    enemy_position = self.units[k].position
                    if (enemy_position == attack_range1 or enemy_position == attack_range2):
                        self.units[k].reset_attribute(self.buff, health=self.units[k].health_now - 400 * (
                        1 - self.units[k].defense_now / 1000))
                base_position = self.hqs[0].position
                if (base_position == attack_range1 or base_position == attack_range2):
                    self.hqs[0].reset_attribute(self.buff, health=self.hqs[0].health_now - 400 * (
                    1 - self.units[k].defense_now / 1000))
                base_position2 = self.hqs[1].position
                if (base_position2 == attack_range1 or base_position2 == attack_range2):
                    self.hqs[1].reset_attribute(self.buff, health=self.hqs[1].health_now - 400 * (
                    1 - self.units[k].defense_now / 1000))
                print(my_information.max_speed_now)
                my_information.reset_attribute(self.buff, speed=my_information.max_speed_now + 5)
                my_information.reset_attribute(self.buff, skill_last_release_time2=self.turn_num)
                print(my_information.max_speed_now)

        # 改造人战士技能1
        def superman_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, enemy_information.position)
            if (skill_cd >= origin_attribute['superman']['skill_cd_1'] and distance <= origin_attribute['superman'][
                'origin_shot_range'] and (my_information.flag != enemy_information.flag)):
                if (self.superman_motortype[my_information.flag]== 0) and (
                            enemy_information.Get_unit_type() == 0 or enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 2):
                    enemy_information.reset_attribute(self.buff,
                                                      health=enemy_information.health_now - my_information.attack_now * (
                                                      1 - enemy_information.defense_now / 1000))
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
                elif (self.superman_motortype[my_information.flag] == 1) and (
                                enemy_information.Get_unit_type() == 0 or enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 2 or enemy_information.Get_unit_type() == 3):
                    enemy_information.reset_attribute(self.buff,
                                                      health=enemy_information.health_now - my_information.attack_now * (
                                                      1 - enemy_information.defense_now / 1000))
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 改造人战士技能2
        def superman_skill2(id):
            my_information = Get_id_information(id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            if (skill_cd >= origin_attribute['superman']['skill_cd_2']):
                my_information.reset_attribute(self.buff, speed=12,
                                               health=my_information.health.now * 1.02)
                my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
                self.superman_skill_release_time[my_information.flag]=self.turn_num

        for k in range(len(order)):
            #print(Get_id_information(order[k][1]).Get_type_name())
            if (Get_id_information(order[k][1]).Get_type_name() == 5):#'bolt_tank'
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
            elif (Get_id_information(order[k][1]).Get_type_name() == 6 and order[k][0]==2):#'nuke_tank'
                nuke_tank_skill2(order[k][1], order[k][2],order[k][3])
                #print('use skill6')
            elif (Get_id_information(order[k][1]).Get_type_name() == 8and order[k][0]==1):#'eagle'
                eagle_skill1(order[k][1], order[k][2],order[k][3])
                #print('use skill7')
            elif (Get_id_information(order[k][1]).Get_type_name() == 8and order[k][0]==2):#'eagle'
                eagle_skill2(order[k][1], order[k][2], order[k][3],order[k][4], order[k][5])
                #print('use skill8')
            elif (Get_id_information(order[k][1]).Get_type_name() == 3and order[k][0]==1):#'superman'
                superman_skill1(order[k][1], order[k][2])
                #print('use skill9')
            elif (Get_id_information(order[k][1]).Get_type_name() == 3and order[k][0]==2):#'superman'
                superman_skill2(order[k][1])
                #print('use skill0')
        pass

    def move_phase(self):
        # 移动指令结算
        id_collection = list(self.units.values())  # 寻找传入ai_id对应的value(unitobject)
        for things in self.move_instr_0:
            for obj in id_collection:
                if obj.unit_id == things[0]:  # 如果unit_id 相符
                    if obj.Get_unit_type() == 0 or obj.Get_unit_type() == 4 or obj.flag != 0:
                        pass
                    else:
                        x = things[1]
                        y = things[2]
                        x1 = obj.position[0]
                        y1 = obj.position[1]
                        if x > 100 or y > 100 or x < 0 or y < 0:
                            return
                        elif abs(x1 - x) + abs(y1 - y) <= obj.max_speed_now:
                            for obj_1 in id_collection:
                                if obj_1.position[0] == x and obj_1.position[1] == y:
                                    pass
                                else:
                                    obj.position=[x,y]

                        else:
                            pass
        for things in self.move_instr_1:
            for obj in id_collection:
                if obj.unit_id == things[0]:  # 如果unit_id 相符
                    if obj.Get_unit_type() == 0 or obj.Get_unit_type() == 4 or obj.flag == 0:
                        pass
                    else:
                        x = things[1]
                        y = things[2]
                        x1 = obj.position[0]
                        y1 = obj.position[1]
                        if x > 100 or y > 100 or x < 0 or y < 0:
                            return
                        elif abs(x1 - x) + abs(y1 - y) <= obj.max_speed_now:
                            for obj_1 in id_collection:
                                if obj_1.position[0] == x and obj_1.position[1] == y:
                                    pass
                                else:
                                    obj.position=(x,y)
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
                                self.resource[ai_id]['money'] < unit.origin_attribute['battle_tank']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['battle_tank']['tech_cost']:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'battle_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['battle_tank']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['battle_tank']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['battle_tank']['tech_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 12:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['bolt_tank']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['bolt_tank']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['bolt_tank']['tech_cost']:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'bolt_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['bolt_tank']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['bolt_tank']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['bolt_tank']['tech_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 13:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['nuke_tank']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['nuke_tank']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['nuke_tank']['tech_cost'] or \
                                self.amount_limit[ai_id]['nuke_tank'] == True:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'nuke_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['nuke_tank']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['nuke_tank']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['nuke_tank']['tech_cost']
                self.amount_limit[ai_id]['nuke_tank'] = True
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 14:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['uav']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['uav']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['uav']['tech_cost']:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'uav', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['uav']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['uav']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['uav']['tech_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 15:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['eagle']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['eagle']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['eagle']['tech_cost'] or \
                                self.amount_limit[ai_id]['eagle'] == True:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'eagle', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['eagle']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['eagle']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['eagle']['tech_cost']
                self.amount_limit[ai_id]['eagle'] = True
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 0:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['meat']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['meat']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['meat']['tech_cost'] or self.meat_count0 >= 10:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'meat', self.units[building_id].position, self.buff)
                self.meat_count0 += 1
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
                                self.resource[ai_id]['money'] < unit.origin_attribute['battle_tank']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['battle_tank']['tech_cost']:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'battle_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['battle_tank']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['battle_tank']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['battle_tank']['tech_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 12:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['bolt_tank']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['bolt_tank']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['bolt_tank']['tech_cost']:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'bolt_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['bolt_tank']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['bolt_tank']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['bolt_tank']['tech_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 13:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['nuke_tank']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['nuke_tank']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['nuke_tank']['tech_cost'] or \
                                self.amount_limit[ai_id]['nuke_tank'] == True:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'nuke_tank', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['nuke_tank']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['nuke_tank']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['nuke_tank']['tech_cost']
                self.amount_limit[ai_id]['nuke_tank'] = True
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 14:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['uav']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['uav']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['uav']['tech_cost']:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'uav', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['uav']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['uav']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['uav']['tech_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 15:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['eagle']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['eagle']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['eagle']['tech_cost'] or \
                                self.amount_limit[ai_id]['eagle'] == True:
                    continue
                weapon = unit.UnitObject(self.total_id, ai_id, 'eagle', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['eagle']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['eagle']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['eagle']['tech_cost']
                self.amount_limit[ai_id]['eagle'] = True
                self.units[self.total_id] = weapon
                self.total_id += 1
                continue
            if self.units[building_id].Get_type_name() == 0:
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['meat']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['meat']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['meat']['tech_cost'] or self.meat_count1 >= 10:
                    continue
                meat_count1 +=1
                weapon = unit.UnitObject(self.total_id, ai_id, 'meat', self.units[building_id].position, self.buff)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['meat']['people_cost']
                self.resource[ai_id]['money'] -= unit.origin_attribute['meat']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['meat']['tech_cost']
                self.units[self.total_id] = weapon
                self.total_id += 1
        # 兵种获取指令结算
        pass

    def resource_phase(self):
        # 资源结算阶段
        for unit_id in self.units.values():
            if unit_id.flag == -1:
                continue
            if unit_id.Get_type_name() == 21:
                self.resource[unit_id.flag]["money"] += 100
            if unit_id.Get_type_name() == 20:
                self.resource[unit_id.flag]["tech"] += 50
        pass

    def capture_phase(self):
        # 占领建筑阶段
        current_pointer = {}
        unit_obj = list(self.units.values())
        unit_building=list(self.buildings)
        for x in unit_building:
            current_pointer[x.unit_id]=0
        for orders in self.capture_instr_0:
            for things in unit_obj:
                #print("am")
                if orders[0] == things.unit_id and things.Get_type_name() == 1 and things.flag == 0:
                    for k in unit_building:
                        if k.unit_id == orders[1]:
                            if k.Get_unit_type() == 4 and abs(
                                        things.position[0] - k.position[0]) + abs(things.position[1] - k.position[1]) == 1:
                                current_pointer[k.unit_id] += 1
                    things.health_now=0

        for orders in self.capture_instr_1:
            for things in unit_obj:
                if orders[0] == things.unit_id and things.Get_type_name() == 1 and things.flag == 1:
                    for k in unit_building:
                        if k.unit_id == orders[1] :
                            if k.Get_unit_type() == 4 and abs(
                                        things.position[0] - k.position[0]) + abs(things.position[1] - k.position[1]) == 1:
                                current_pointer[k.unit_id] -= 1
                    things.health_now=0
        for obj in unit_building:  # 结算建筑都是哪一方的
            if current_pointer[obj.unit_id] > 0:
                obj.flag = 0
            if current_pointer[obj.unit_id] < 0:
                obj.flag = 1
            if current_pointer[obj.unit_id] == 0:
                pass
            for units in unit_building:
                if units.Get_type_name() == 9:
                    for things in unit_obj:
                        if things.flag == units.flag:
                            things.hacked_point *= 1.5
                if units.Get_type_name() == 10:
                    if units.flag == 0:
                        self.buff[unit.FLAG_0][unit.INFANTRY]['health_buff'] = 0.5
                    if units.flag == 1:
                        self.buff[unit.FLAG_1][unit.INFANTRY]['health_buff'] = 0.5
                if units.Get_type_name() == 11:
                    if units.flag == 0:
                        self.buff[unit.FLAG_0][unit.VEHICLE]['attack_buff'] = 0.05
                        self.buff[unit.FLAG_0][unit.VEHICLE]['defence_buff'] = 0.05
                    if units.flag == 1:
                        self.buff[unit.FLAG_1][unit.VEHICLE]['attack_buff'] = 0.05
                        self.buff[unit.FLAG_1][unit.VEHICLE]['defence_buff'] = 0.05
                if units.Get_type_name() == 12:
                    if units.flag == 0:
                        self.buff[unit.FLAG_0][unit.VEHICLE]['attack_buff'] = 0.1
                        self.buff[unit.FLAG_0][unit.AIRCRAFT]['attack_buff'] = 0.1
                    if units.flag == 1:
                        self.buff[unit.FLAG_1][unit.VEHICLE]['attack_buff']= 0.1
                        self.buff[unit.FLAG_1][unit.AIRCRAFT]['attack_buff'] = 0.1
                if units.Get_type_name() == 13:
                    if units.flag == 0:
                        self.buff[unit.FLAG_0][unit.VEHICLE]['attack_buff'] = 0.2
                    if units.flag == 1:
                        self.buff[unit.FLAG_1][unit.VEHICLE]['attack_buff'] = 0.2

                if units.Get_type_name() == 14:
                    if units.flag == 0:
                        self.buff[unit.FLAG_0][unit.VEHICLE]['produce_buff'] = 0.15
                        self.buff[unit.FLAG_0][unit.INFANTRY]['produce_buff'] = 0.15
                        self.buff[unit.FLAG_0][unit.AIRCRAFT]['produce_buff'] = 0.15

                    if units.flag == 1:
                        self.buff[unit.FLAG_1][unit.VEHICLE]['produce_buff'] = 0.15
                        self.buff[unit.FLAG_1][unit.INFANTRY]['produce_buff'] = 0.15
                        self.buff[unit.FLAG_1][unit.AIRCRAFT]['produce_buff'] = 0.15
                if units.Get_type_name() == 15:
                    if units.flag == 0:
                        self.buff[unit.FLAG_0][unit.AIRCRAFT]['produce_buff'] = 0.1
                        self.buff[unit.FLAG_0][unit.AIRCRAFT]['speed_buff'] = 3
                        self.buff[unit.FLAG_0][unit.AIRCRAFT]['attack_buff'] = 0.1
                    if units.flag == 1:
                        self.buff[unit.FLAG_1][unit.VEHICLE]['produce_buff'] = 0.1
                        self.buff[unit.FLAG_1][unit.VEHICLE]['speed_buff'] = 3
                        self.buff[unit.FLAG_1][unit.VEHICLE]['attack_buff'] = 0.1

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
        for i in range(len(self.capture_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.capture_instr_1[i][0] and things.flag == 1:  # 如果移动的是自己的单位
                    temp_c_instr_1[self.capture_instr_1[i][0]] = self.capture_instr_1[i]
                if things.unit_id == self.capture_instr_1[i][0] and things.flag == 0:  # 如果移动的不是自己的单位
                    pass
        self.capture_instr_1 = list(temp_c_instr_1.values())

        temp_p_instr_1 = {}
        temp_p_instr_0 = {}
        for i in range(len(self.produce_instr_0)):
            for things in self.units.values():
                if things.unit_id == self.produce_instr_0[i] and things.flag == 0:  # 如果移动的是自己的单位
                    temp_p_instr_0[self.produce_instr_0[i]] = self.produce_instr_0[i]
                if things.unit_id == self.produce_instr_0[i] and things.flag == 1:  # 如果移动的不是自己的单位
                    pass
        self.produce_instr_0 = list(temp_p_instr_0.values())
        for i in range(len(self.produce_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.produce_instr_1[i] and things.flag == 1:  # 如果移动的是自己的单位
                    temp_p_instr_1[self.produce_instr_1[i]] = self.produce_instr_1[i]
                if things.unit_id == self.produce_instr_1[i] and things.flag == 0:  # 如果移动的不是自己的单位
                    pass
        self.produce_instr_1 = list(temp_p_instr_1.values())

        temp_s_instr_0 = {}
        temp_s_instr_1 = {}
        for i in range(len(self.skill_instr_0)):
            for things in self.units.values():
                if things.unit_id == self.skill_instr_0[i][1] and things.flag == 0:  # 如果移动的是自己的单位
                    temp_s_instr_0[self.skill_instr_0[i][1]] = self.skill_instr_0[i]
                if things.unit_id == self.skill_instr_0[i][1] and things.flag == 1:  # 如果移动的不是自己的单位
                    pass
        self.skill_instr_0 = list(temp_s_instr_0.values())
        for i in range(len(self.skill_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.skill_instr_1[i][1] and things.flag == 1:  # 如果移动的是自己的单位
                    temp_s_instr_1[self.skill_instr_1[i][1]] = self.skill_instr_1[i]
                if things.unit_id == self.skill_instr_1[i][1] and things.flag == 0:  # 如果移动的不是自己的单位
                    pass
        self.skill_instr_1 = list(temp_s_instr_1.values())


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
        print("produce instr_0:", len(self.produce_instr_0), "move instr_0:", len(self.move_instr_0), "cap instr_0:",len(self.capture_instr_0), "skill instr_0:", len(self.skill_instr_0))
        print("produce instr_1:", len(self.produce_instr_1), "move instr_1:", len(self.move_instr_1), "cap instr_1:",len(self.capture_instr_1), "skill instr_1:", len(self.skill_instr_1))
        if (self.check_winner == 3):
            self.move_phase()
            self.produce_phase()
            self.resource_phase()
            self.capture_phase()
        check_timeup =self.timeup_determine()
        print("after HP0:", self.hqs[0].health_now, "after HP1:", self.hqs[1].health_now)
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
        print(ai0)
        print(ai1)
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

        # 测试技能用
