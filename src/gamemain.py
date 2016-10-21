#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from src import unit
from src.unit import origin_attribute
import random
from random import choice

class GameMain:
    units = {}  # 单位dict key:unit_id value:unitobject
    hqs = []  # 主基地
    buildings = []  # 中立建筑
    # turn_flag = 0  # 谁的回合
    turn_num = 0  # 回合数
    phase_num = 0  # 回合阶段指示
    skill_instr_0 = []  # ai0的当前回合指令
    skill_instr_1 = []  # ai1的当前回合制令
    produce_instr_0 = []
    produce_instr_1 = []
    move_instr_0 = []  # 指令格式[[unit_id,position_x,position_y],[unit_id,position_x,position_y]]
    move_instr_1 = []
    capture_instr_0 = []  # 指令格式[[unit_id,building_id][unit_id,building_id][]]
    capture_instr_1 = []
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
    total_id = 0 #总共的项目的id编号
    resource = {} #双方金钱、科技、剩余人口容量记录

    def __init__(self):
        #地图生成模块
        id_collection = [0,1]  # 寻找传入ai_id对应的value
        ai_id0 = id_collection[0]
        ai_id1 = id_collection[1]
        #初始化self.resource
        self.resource = {ai_id0: {"tech": 1000, "money": 1000, "remain_people": 1000000},
                         ai_id1: {"tech": 1000, "money": 1000, "remain_people": 1000000}}
        # 在一定范围内random出一个基地并中心对称 并伴随生成bank 和teaching building 各一个
        box_base0_x = random.randint(1, 10)
        box_base0_y = random.randint(1, 5)
        box_base1_x = 10 - box_base0_x
        box_base1_y = 5 - box_base0_y
        player0_x = (box_base0_x - 1) * 10 + random.randint(1, 9)
        player0_y = (box_base0_y - 1) * 10 + random.randint(1, 5)
        player1_x = 100 - player0_x
        player1_y = 100 - player0_y
        base0 = unit.UnitObject(self.total_id, ai_id0, 'base', (player0_x, player0_y))
        self.units[ai_id0] = self.total_id
        self.hqs.append(self.total_id)
        self.total_id += 1
        base1 = unit.UnitObject(self.total_id, ai_id1, 'base', (player1_x, player1_y))
        self.units[ai_id1] = self.total_id
        self.hqs.append(self.total_id)
        self.total_id += 1
        self.hqs = [(player0_x, player0_y), (player1_x, player1_y)]
        tech0 = unit.UnitObject(self.total_id, ai_id0, 'teach_building', (player0_x, player0_y + 2))
        self.units[ai_id0] = self.total_id
        self.total_id += 1
        tech1 = unit.UnitObject(self.total_id, ai_id0, 'teach_building', (100 - player0_x, 98 - player0_y))
        self.units[ai_id0] = self.total_id
        self.total_id += 1
        bank0 = unit.UnitObject(self.total_id, ai_id1, 'bank', (player0_x, player0_y - 2))
        self.units[ai_id1] = self.total_id
        self.total_id += 1
        bank1 = unit.UnitObject(self.total_id, ai_id1, 'bank', (100 - player0_x, 102 - player0_y))
        self.units[ai_id1] = self.total_id
        self.total_id += 1
        # random银行和教学楼并中心对称
        # 除去出生地附近 教学楼和银行总数为8或7（一半地图） 各自数目不定
        bank_and_teach = 12
        position_now = 0
        box_x = 0
        box_y = 0
        while (bank_and_teach > 0):
            position_now += random.randint(1, int((50 - position_now) / bank_and_teach))
            box_x = position_now % 10
            box_y = int(position_now / 10) + 1
            if box_base0_x == box_x and box_base0_y == box_y:
                bank_and_teach -= 1
                continue
            type_rand = random.randint(0, 1)  # 0产生教学楼，1产生银行
            if type_rand == 0:
                tech_x = (box_x - 1) * 10 + random.randint(1, 9)
                tech_y = (box_y - 1) * 10 + random.randint(1, 5)
                tech_1_x = 100 - tech_x
                tech_1_y = 100 - tech_y
                tech0 = unit.UnitObject(self.total_id, None, 'teach_building', (tech_x, tech_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                tech1 = unit.UnitObject(self.total_id, None, 'teach_building', (tech_1_x, tech_1_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if type_rand == 1:
                bank_x = (box_x - 1) * 10 + random.randint(1, 9)
                bank_y = (box_y - 1) * 10 + random.randint(1, 5)
                bank_1_x = 100 - bank_x
                bank_1_y = 100 - bank_y
                bank0 = unit.UnitObject(self.total_id, None, 'teach_building', (bank_x, bank_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                bank1 = unit.UnitObject(self.total_id, None, 'teach_building', (bank_1_x, bank_1_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            bank_and_teach -= 1
        #生成11个具有特定技能的建筑 不进行building_id编号和占有方编号
        building_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        position_now = 0
        total_building = 11
        while (total_building > 0):
            position_now += random.randint(1, int((50 - position_now) / total_building))
            box_x = position_now % 10
            box_y = int(position_now / 10) + 1
            building_x = (box_x - 1) * 10 + random.randint(1, 9)
            building_y = (box_y - 1) * 10 + random.randint(7, 9)
            building_type = choice(building_list)
            if building_type == 1:
                building0 = unit.UnitObject(self.total_id, None, 'hack_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'hack_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if building_type == 2:
                building0 = unit.UnitObject(self.total_id, None, 'bid_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'bid_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if building_type == 3:
                building0 = unit.UnitObject(self.total_id, None, 'car_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'car_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if building_type == 4:
                building0 = unit.UnitObject(self.total_id, None, 'elec_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'elec_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if building_type == 5:
                building0 = unit.UnitObject(self.total_id, None, 'radiation_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'radiation_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if building_type == 6:
                building0 = unit.UnitObject(self.total_id, None, 'uav_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'uav_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if building_type == 7:
                building0 = unit.UnitObject(self.total_id, None, 'aircraft_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'aircraft_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if building_type == 8:
                building0 = unit.UnitObject(self.total_id, None, 'build_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'build_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if building_type == 9:
                building0 = unit.UnitObject(self.total_id, None, 'finance_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'finance_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if building_type == 10:
                building0 = unit.UnitObject(self.total_id, None, 'material_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'material_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
            if building_type == 11:
                building0 = unit.UnitObject(self.total_id, None, 'nano_lab', (building_x, building_y))
                self.buildings.append(self.total_id)
                self.total_id += 1
                building1 = unit.UnitObject(self.total_id, None, 'nano_lab', (100 - building_x, 100 - building_y))
                self.buildings.append(self.total_id)
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
        #超时胜利判定
        if self.turn_num>MAX_ROUND:#如果超过了最大回合数
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


    def cleanup_phase(self):
        # 单位死亡判定
        id_collection = [0,1]  # 寻找传入ai_id对应的value
        for ai_id in id_collection:
            unit_obj=list(self.units.get(ai_id))
            for things in unit_obj:
                if things.health_now <= 0:
                    self.units[ai_id].remove(things)  # 从字典的value列表中把死亡单位删除
                    if things.__type_name == 'hacker':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['hack_lab']['remain_people']
                    if things.__type_name == 'superman':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['bid_lab']['remain_people']
                    if things.__type_name == 'battle_tank':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['car_lab']['remain_people']
                    if things.__type_name == 'bolt_tank':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['elec_lab']['remain_people']
                    if things.__type_name == 'nuke_tank':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['radiation_lab']['remain_people']
                    if things.__type_name == 'uav':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['uav_lab']['remain_people']
                    if things.__type_name == 'eagle':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['aircraft_lab']['remain_people']
                    if things.__type_name == 'meat':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['base']['remain_people']
                if things.hacked_point >= things.max_health_now >= 0:
                    self.units[ai_id].remove(things)  # 从字典里删除被黑了的单位
                    if things.__type_name == 'battle_tank':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['car_lab']['remain_people']
                    if things.__type_name == 'bolt_tank':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['elec_lab']['remain_people']
                    if things.__type_name == 'nuke_tank':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['radiation_lab']['remain_people']
                    if things.__type_name == 'uav':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['uav_lab']['remain_people']
                    if things.__type_name == 'eagle':
                        self.resource[ai_id]['remain_people'] += unit.origin_attribute['aircraft_lab']['remain_people']
        pass

    def skill_phase(self,order):
        # 技能结算


        def Get_id_information(id):
            for k in self.units:
                if (k == id):
                    return self.units[k]

        def Get_distance(my_position, enemy_position):
            x = my_position[0] - enemy_position[0]
            y = my_position[1] - enemy_position[1]
            return (x * x + y * y) ** 0.5

        # 电子对抗坦克技能1
        def bolt_tank_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, enemy_information.position)
            if (skill_cd >= origin_attribute['bolt_tank']['skill_cd_1'] and distance <= origin_attribute['blot_tank'][
                'origin_shot_range']):
                if (my_information.flag != enemy_information.flag) and (enemy_information.Get_unit_type() == 3):
                    enemy_information.reset_attribute(self.buff,health=enemy_information.health_now - 200)
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
                enemy_information.reset_attribute(self.buff, health=enemy_information.health_now - 5)
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
                enemy_information.reset_attribute(self.buff, health=enemy_information.health_now - 100)
                my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 核子坦克技能1
        def nuke_tank_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, enemy_information.position)
            if (skill_cd >= origin_attribute['nuke_tank']['skill_cd_1'] and distance <= origin_attribute['nuke_tank'][
                'origin_shot_range'] and (my_information.flag != enemy_information.flag)):
                if (enemy_information.Get_unit_type() == 3 or enemy_information.Get_unit_type() == 2):
                    enemy_information.reset_attribute(self.buff, health=enemy_information.health_now - 300)
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 核子坦克技能2
        def nuke_tank_skill2(id, attack_range):
            my_information = Get_id_information(id)
            skill_cd = self.turn_num - my_information.skill_last_release_time2
            distance = Get_distance(my_information.position, attack_range)
            if (skill_cd >= origin_attribute['nuke_tank']['skill_cd_2'] and distance <= origin_attribute['nuke_tank'][
                'origin_shot_range']):
                print(self.units)
                for k in self.units:
                    enemy_position = self.units[k].position
                    if (Get_distance(enemy_position, attack_range) < 2):
                        self.units[k].reset_attribute(self.buff, health=self.units[k].health_now - 800)
                my_information.reset_attribute(self.buff, skill_last_release_time2=self.turn_num)

        # 鹰式战斗机技能1
        def eagle_skill1(id, attack_range):
            my_information = Get_id_information(id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, attack_range)
            if (skill_cd >= origin_attribute['eagle']['skill_cd_1'] and distance <= origin_attribute['eagle'][
                'origin_shot_range']):
                for k in self.units:
                    enemy_position = self.units[k].position
                    if (enemy_position == attack_range):
                        self.units[k].reset_attribute(health=self.units[k].health_now - 200)
                my_information.reset_attribute(skill_last_release_time1=self.turn_num)

        # 鹰式战斗机技能2
        def eagle_skill2(id, attack_range1, attack_range2):
            my_information = Get_id_information(id)
            skill_cd = self.turn_num - my_information.skill_last_release_time2
            distance1 = Get_distance(my_information.position, attack_range1)
            distance2 = Get_distance(my_information.position, attack_range2)
            if (skill_cd >= origin_attribute['eagle']['skill_cd_2'] and distance1 <= origin_attribute['eagle'][
                'origin_shot_range'] and distance2 <= origin_attribute['eagle']['origin_shot_range']):
                for k in self.units:
                    enemy_position = self.units[k].position
                    if (enemy_position == attack_range1 or enemy_position == attack_range2):
                        self.units[k].reset_attribute(self.buff, health=self.units[k].health_now - 400)
                my_information.reset_attribute(self.buff, speed=my_information.max_speed_now + 5)
                my_information.reset_attribute(self.buff, skill_last_release_time2=self.turn_num)

        # 改造人战士技能1
        def superman_skill1(id, attack_id):
            my_information = Get_id_information(id)
            enemy_information = Get_id_information(attack_id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            distance = Get_distance(my_information.position, enemy_information.position)
            if (skill_cd >= origin_attribute['superman']['skill_cd_1'] and distance <= origin_attribute['superman'][
                'origin_shot_range'] and (my_information.flag != enemy_information.flag)):
                if (my_information.motor_type == 0) and (
                                enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 2):
                    enemy_information.reset_attribute(self.buff, health=enemy_information.health_now - 15)
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)
                elif (my_information.motor_type == 1):
                    enemy_information.reset_attribute(self.buff, health=enemy_information.health_now - 15)
                    my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        # 改造人战士技能2
        def superman_skill2(id):
            my_information = Get_id_information(id)
            skill_cd = self.turn_num - my_information.skill_last_release_time1
            if (skill_cd >= origin_attribute['superman']['skill_cd_2']):
                my_information.reset_attribute(self.buff, motor_type=1, speed=12, health=my_information.health.now * 1.02)
                my_information.reset_attribute(self.buff, skill_last_release_time1=self.turn_num)

        for k in range(len(order)):
            if (order[k][0] == 'bolt_tank_skill1'):
                bolt_tank_skill1(order[k][1], order[k][2])
            elif (order[k][0] == 'hacker_skill1'):
                hacker_skill1(order[k][1], order[k][2])
            elif (order[k][0] == 'uav'):
                uav(order[k][1], order[k][2])
            elif (order[k][0] == 'battle_tank_skill1'):
                battle_tank_skill1(order[k][1], order[k][2])
            elif (order[k][0] == 'nuke_tank_skill1'):
                nuke_tank_skill1(order[k][1], order[k][2])
            elif (order[k][0] == 'nuke_tank_skill2'):
                nuke_tank_skill2(order[k][1], order[k][2])
            elif (order[k][0] == 'eagle_skill1'):
                eagle_skill1(order[k][1], order[k][2])
            elif (order[k][0] == 'eagle_skill2'):
                eagle_skill1(order[k][1], order[k][2])
            elif (order[k][0] == 'superman_skill1'):
                superman_skill1(order[k][1], order[k][2])
            elif (order[k][0] == 'superman_skill2'):
                superman_skill2(order[k][1])
        pass

    def move_phase(self):
        # 移动指令结算
        id_collection = list(self.units.values())  # 寻找传入ai_id对应的value(unitobject)
        for things in self.move_instr_0:
            for obj in id_collection:
                if obj.unit_id == things[0]:  # 如果unit_id 相符
                    if obj.__unit_type == 0 or obj.__unit_type == 4 or obj.flag != 0:
                        pass
                    else:
                        x = things[1]
                        y = things[2]
                        x1 = obj.position_x
                        y1 = obj.position_y
                        if x > 100 or y > 100 or x < 0 or y < 0:
                            return
                        elif abs(x1 - x) + abs(y1 - y) <= obj.max_speed_now:
                            for obj_1 in id_collection:
                                if obj_1.position_x == x and obj_1.position_y == y:
                                    pass
                                else:
                                    obj.position_x = x
                                    obj.position_y = y
                        else:
                            pass
        for things in self.move_instr_1:
            for obj in id_collection:
                if obj.unit_id == things[0]:  # 如果unit_id 相符
                    if obj.__unit_type == 0 or obj.__unit_type == 4 or obj.flag == 0:
                        pass
                    else:
                        x = things[1]
                        y = things[2]
                        x1 = obj.position_x
                        y1 = obj.position_y
                        if x > 100 or y > 100 or x < 0 or y < 0:
                            return
                        elif abs(x1 - x) + abs(y1 - y) <= obj.max_speed_now:
                            for obj_1 in id_collection:
                                if obj_1.position_x == x and obj_1.position_y == y:
                                    pass
                                else:
                                    obj.position_x = x
                                    obj.position_y = y
                        else:
                            pass

        pass

    def produce_phase(self):
        id_collection = [0,1]  # 寻找传入ai_id对应的value
        ai_id = id_collection[0]
        for building_id in self.produce_instr_0:
            if building_id.__type_name == 'hack_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['hack_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['hack_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['hack_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'hacker', building_id.position)
                self.resource[ai_id]['money'] -= unit.origin_attribute['hack_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['hack_lab']['tech_cost']
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['hack_lab']['remain_people']
            if building_id.__type_name == 'bid_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['bid_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['bid_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['bid_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'superman', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['bid_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['bid_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['bid_lab']['tech_cost']
            if building_id.__type_name == 'car_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['car_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['car_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['car_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'battle_tank', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['car_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['car_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['car_lab']['tech_cost']
            if building_id.__type_name == 'elec_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['elec_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['elec_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['elec_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'bolt_tank', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['elec_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['elec_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['elec_lab']['tech_cost']
            if building_id.__type_name == 'radiation_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['radiation_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['radiation_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['radiation_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'nuke_tank', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['radiation_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['radiation_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['radiation_lab']['tech_cost']
            if building_id.__type_name == 'uav_lab':
                people_type = 7
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['uav_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['uav_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['uav_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'uav', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['uav_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['uav_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['uav_lab']['tech_cost']
            if building_id.__type_name == 'aircraft_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['aircraft_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['aircraft_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['aircraft_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'eagle', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['aircraft_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['aircraft_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['aircraft_lab']['tech_cost']
            if building_id.__type_name == 'base':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['base']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['base']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['base']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'hacker', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['base_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['base']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['base']['tech_cost']
        self.units[ai_id].append(self.total_id)
        self.total_id += 1
        ai_id = id_collection[1]
        for building_id in self.produce_instr_1:
            if building_id.__type_name == 'hack_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['hack_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['hack_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['hack_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'hacker', building_id.position)
                self.resource[ai_id]['money'] -= unit.origin_attribute['hack_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['hack_lab']['tech_cost']
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['hack_lab']['remain_people']
            if building_id.__type_name == 'bid_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['bid_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['bid_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['bid_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'superman', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['bid_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['bid_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['bid_lab']['tech_cost']
            if building_id.__type_name == 'car_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['car_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['car_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['car_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'battle_tank', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['car_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['car_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['car_lab']['tech_cost']
            if building_id.__type_name == 'elec_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['elec_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['elec_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['elec_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'bolt_tank', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['elec_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['elec_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['elec_lab']['tech_cost']
            if building_id.__type_name == 'radiation_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['radiation_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['radiation_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['radiation_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'nuke_tank', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['radiation_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['radiation_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['radiation_lab']['tech_cost']
            if building_id.__type_name == 'uav_lab':
                people_type = 7
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['uav_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['uav_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['uav_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'uav', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['uav_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['uav_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['uav_lab']['tech_cost']
            if building_id.__type_name == 'aircraft_lab':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['aircraft_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['aircraft_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['aircraft_lab']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'eagle', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['aircraft_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['aircraft_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['aircraft_lab']['tech_cost']
            if building_id.__type_name == 'base':
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['base']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['base']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['base']['tech_cost']:
                    return
                person = unit.UnitObject(self.total_id, ai_id, 'hacker', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['base_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['base']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['base']['tech_cost']
        self.units[ai_id].append(self.total_id)
        self.total_id += 1
        # 兵种获取指令结算
        pass

    def resource_phase(self):
        #资源结算阶段
        bank_count = 0
        teaching_building_count = 0
        id_collection = [0,1]  # 寻找传入ai_id对应的value
        for ai_id in id_collection:
            unit_obj = list(self.units.get(ai_id))
            for things in unit_obj:
                if things.__type_name == "bank":
                    bank_count += 1
                if things.__type_name == "teach_building":
                    teaching_building_count += 1
            self.resource[ai_id]["money"] += 500 * bank_count
            self.resource[ai_id]["tech"] += 50 * teaching_building_count
        pass

    def capture_phase(self):
        # 占领建筑阶段
        unit_obj = list(self.units.values())
        for orders in self.capture_instr_0:
            for things in unit_obj:
                if orders[0] == things.unit_id and things.__type_name == "meat" and things.flag == 0:
                    for k in unit_obj:
                        if k.unit_id == orders[1] and k.__unit_type == 4 and abs(
                                        things.position_x - k.position_x) + abs(things.position_y - k.position_y) == 1:
                            things.current_pointer += 1
        for orders in self.capture_instr_1:
            for things in unit_obj:
                if orders[0] == things.unit_id and things.__type_name == "meat" and things.flag == 1:
                    for k in unit_obj:
                        if k.unit_id == orders[1] and k.__unit_type == 4 and abs(
                                        things.position_x - k.position_x) + abs(things.position_y - k.position_y) == 1:
                            things.current_pointer -= 1
        for obj in unit_obj:  # 结算建筑都是哪一方的
            if obj.current_pointer > 0:
                obj.flag = 0
            if obj.current_pointer < 0:
                obj.flag = 1
            if obj.current_pointer == 0 and obj.__type_name == 4:
                obj.flag = 2
            for unit in unit_obj:
                if unit.__type_name == 'hack_lab':
                    for things in unit_obj:
                        if things.flag == unit.flag:
                            things.hacked_point *= 1.5
                if unit.__type_name == 'bid_lab':
                    if unit.flag == 0:
                        self.buff[unit.FLAG_0[unit.INFANTRY['health_buff']]] = 0.5
                    if unit.flag == 1:
                        self.buff[unit.FLAG_1[unit.INFANTRY['health_buff']]] = 0.5
                if unit.__type_name == 'car_lab':
                    if unit.flag == 0:
                        self.buff[unit.FLAG_0[unit.VEHICLE['attack_buff']]] = 0.05
                        self.buff[unit.FLAG_0[unit.VEHICLE['defence_buff']]] = 0.05
                    if unit.flag == 1:
                        self.buff[unit.FLAG_1[unit.VEHICLE['attack_buff']]] = 0.05
                        self.buff[unit.FLAG_1[unit.VEHICLE['defence_buff']]] = 0.05
                if unit.__type_name == 'elec_lab':
                    if unit.flag == 0:
                        self.buff[unit.FLAG_0[unit.VEHICLE['attack_buff']]] = 0.1
                        self.buff[unit.FLAG_0[unit.AIRCRAFT['attack_buff']]] = 0.1
                    if unit.flag == 1:
                        self.buff[unit.FLAG_1[unit.VEHICLE['attack_buff']]] = 0.1
                        self.buff[unit.FLAG_1[unit.AIRCRAFT['attack_buff']]] = 0.1
                if unit.__type_name == 'radiation_lab':
                    if unit.flag == 0:
                        self.buff[unit.FLAG_0[unit.VEHICLE['attack_buff']]] = 0.2

                    if unit.flag == 1:
                        self.buff[unit.FLAG_1[unit.VEHICLE['attack_buff']]] = 0.2

                if unit.__type_name == 'uav_lab':
                    if unit.flag == 0:
                        self.buff[unit.FLAG_0[unit.VEHICLE['produce_buff']]] = 0.15
                        self.buff[unit.FLAG_0[unit.INFANTRY['produce_buff']]] = 0.15
                        self.buff[unit.FLAG_0[unit.AIRCRAFT['produce_buff']]] = 0.15

                    if unit.flag == 1:
                        self.buff[unit.FLAG_1[unit.VEHICLE['produce_buff']]] = 0.15
                        self.buff[unit.FLAG_1[unit.INFANTRY['produce_buff']]] = 0.15
                        self.buff[unit.FLAG_1[unit.AIRCRAFT['produce_buff']]] = 0.15
                if unit.__type_name == 'aircraft_lab':
                    if unit.flag == 0:
                        self.buff[unit.FLAG_0[unit.AIRCRAFT['produce_buff']]] = 0.1
                        self.buff[unit.FLAG_0[unit.AIRCRAFT['speed_buff']]] = 3
                        self.buff[unit.FLAG_0[unit.AIRCRAFT['attack_buff']]] = 0.1
                    if unit.flag == 1:
                        self.buff[unit.FLAG_1[unit.VEHICLE['produce_buff']]] = 0.1
                        self.buff[unit.FLAG_1[unit.VEHICLE['speed_buff']]] = 3
                        self.buff[unit.FLAG_1[unit.VEHICLE['attack_buff']]] = 0.1
        pass

    def fetch_instruction(self):
        #获取指令存入两个指令list
        pass

    def check_legal(self):
        #检查双方指令是否合法，去重
        # 将指令list反向
        self.move_instr_0.reverse()
        self.move_instr_1.reverse()
        self.capture_instr_0.reverse()
        self.capture_instr_1.reverse()
        self.skill_instr_0.reverse()
        self.skill_instr_1.reverse()
        self.produce_instr_0.reverse()
        self.produce_instr_1.reverse()
        for i in range(len(self.move_instr_0)):
            for things in self.units.values():
                if things.unit_id == self.move_instr_0[i][0] and things.flag == 0:  # 如果移动的是自己的单位
                    for j in range[i:len(self.move_instr_0):1]:
                        if self.move_instr_0[i][0] == self.move_instr_0[j][0]:  # 如果unit_id相同
                            del self.move_instr_0[j]  # 删除较靠前的项
                if things.unit_id == self.move_instr_0[i][0] and things.flag == 1:  # 如果移动的不是自己的单位
                    del self.move_instr_0[i]
        for i in range(len(self.move_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.move_instr_1[i][0] and things.flag == 1:  # 如果移动的是自己的单位
                    for j in range[i:len(self.move_instr_1):1]:
                        if self.move_instr_1[i][0] == self.move_instr_1[j][0]:  # 如果unit_id相同
                            del self.move_instr_1[j]  # 删除较靠前的项
                if things.unit_id == self.move_instr_1[i][0] and things.flag == 0:  # 如果移动的不是自己的单位
                    del self.move_instr_1[i]
        self.move_instr_0.reverse()
        self.move_instr_1.reverse()
        for i in range(len(self.capture_instr_0)):
            for things in self.units.values():
                if things.unit_id == self.capture_instr_0[i][0] and things.flag == 0:  # 如果移动的是自己的单位
                    for j in range[i:len(self.capture_instr_0):1]:
                        if self.capture_instr_0[i][0] == self.capture_instr_0[j][0]:  # 如果unit_id相同
                            del self.capture_instr_0[j]  # 删除较靠前的项
                if things.unit_id == self.capture_instr_0[i][0] and things.flag == 1:  # 如果移动的不是自己的单位
                    del self.capture_instr_0[i]  # 删除该指令
        for i in range(len(self.capture_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.capture_instr_1[i][0] and things.flag == 1:  # 如果移动的是自己的单位
                    for j in range[i:len(self.capture_instr_1):1]:
                        if self.capture_instr_1[i][0] == self.capture_instr_1[j][0]:  # 如果unit_id相同
                            del self.capture_instr_1[j]  # 删除较靠前的项
                if things.unit_id == self.capture_instr_1[i][0] and things.flag == 0:  # 如果移动的不是自己的单位
                    del self.capture_instr_1[i]  # 删除该指令
        self.capture_instr_0.reverse()
        self.capture_instr_1.reverse()
        for i in range(len(self.produce_instr_0)):
            for things in self.units.values():
                if things.unit_id == self.produce_instr_0[i][0] and things.flag == 0:  # 如果移动的是自己的单位
                    for j in range[i:len(self.produce_instr_0):1]:
                        if self.produce_instr_0[i][0] == self.produce_instr_0[j][0]:  # 如果unit_id相同
                            del self.capture_instr_0[j]  # 删除较靠前的项
                if things.unit_id == self.produce_instr_0[i][0] and things.flag == 1:  # 如果移动的不是自己的单位
                    del self.produce_instr_0[i]  # 删除该指令
        for i in range(len(self.produce_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.produce_instr_1[i][0] and things.flag == 1:  # 如果移动的是自己的单位
                    for j in range[i:len(self.produce_instr_1):1]:
                        if self.produce_instr_1[i][0] == self.produce_instr_1[j][0]:  # 如果unit_id相同
                            del self.produce_instr_1[j]  # 删除较靠前的项
                if things.unit_id == self.produce_instr_1[i][0] and things.flag == 0:  # 如果移动的不是自己的单位
                    del self.produce_instr_1[i]  # 删除该指令
        self.produce_instr_0.reverse()
        self.produce_instr_1.reverse()
        for i in range(len(self.skill_instr_0)):
            for things in self.units.values():
                if things.unit_id == self.skill_instr_0[i][0] and things.flag == 0:  # 如果移动的是自己的单位
                    for j in range[i:len(self.skill_instr_0):1]:
                        if self.skill_instr_0[i][0] == self.skill_instr_0[j][0]:  # 如果unit_id相同
                            del self.capture_instr_0[j]  # 删除较靠前的项
                if things.unit_id == self.skill_instr_0[i][0] and things.flag == 1:  # 如果移动的不是自己的单位
                    del self.skill_instr_0[i]  # 删除该指令
        for i in range(len(self.skill_instr_1)):
            for things in self.units.values():
                if things.unit_id == self.skill_instr_1[i][0] and things.flag == 1:  # 如果移动的是自己的单位
                    for j in range[i:len(self.skill_instr_1):1]:
                        if self.skill_instr_1[i][0] == self.skill_instr_1[j][0]:  # 如果unit_id相同
                            del self.skill_instr_1[j]  # 删除较靠前的项
                if things.unit_id == self.skill_instr_1[i][0] and things.flag == 0:  # 如果移动的不是自己的单位
                    del self.skill_instr_1[i]  # 删除该指令
        self.skill_instr_0.reverse()
        self.skill_instr_1.reverse()
        pass

    def next_tick(self):
        # 获取指令，指令检测合法与去重，回合演算
        self.check_legal()
        self.skill_phase()
        self.cleanup_phase()
        self.win_determine()
        self.move_phase()
        self.produce_phase()
        self.capture_phase()
        self.timeup_determine()
        pass

    def to_string(self):
        # 将当前状态信息返回，用String,Json什么都行，你们自己起名字吧
        pass

    #测试技能用

#测试

A = GameMain()
tank = unit.UnitObject(1, 1, 'nuke_tank', (22, 33), A.buff)
fuck = unit.UnitObject(2, 0, 'battle_tank', (22, 32), A.buff)
A.units[1] = tank
A.units[2] = fuck
A.units[1].print_info()
A.units[2].print_info()
order = [['nuke_tank_skill2', 1, (22, 31)]]

A.skill_phase(order)
A.units[1].print_info()
A.units[2].print_info()