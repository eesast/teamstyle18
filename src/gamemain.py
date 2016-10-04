#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from src import unit
import random
from random import choice

class GameMain:
    units = {}  # 单位dict
    hqs = []  # 主基地
    buildings = []  # 中立建筑
    turn_flag = 0  # 谁的回合
    turn_num = 0  # 回合数
    phase_num = 0  # 回合阶段指示
    buff = {
        unit.FLAG_0: {
            unit.INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                       'shot_range_buff': 0.0},
            unit.VEHICLE: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                      'shot_range_buff': 0.0},
            unit.AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                       'shot_range_buff': 0.0}
        },
        unit.FLAG_1: {
            unit.INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                       'shot_range_buff': 0.0},
            unit.VEHICLE: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                      'shot_range_buff': 0.0},
            unit.AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                       'shot_range_buff': 0.0}
        }
    }
    resource = {}  # 选手0的资源值 一级key为ai_id 二级key为tech和money和remain_people
    total_id = 0  # 作为units中记录每个单位的id 从0开始依次记录

    def __init__(self):
        pass

    def map_phase(self, ai_id0, ai_id1):
        # 地图生成模块
        self.resource = {ai_id0: {"tech": 1000, "money": 1000, "remain_people": 1000000},
                         ai_id1: {"tech": 1000, "money": 1000, "remain_people": 1000000}}
        # 在一定范围内random出一个基地并中心对称 并伴随生成bank 和teaching building 各一个
        # player0_x = random.randint(12, 28)
        # player0_y = random.randint(12, 88)
        #
        #
        box_base0_x = random.randint(1, 10)
        box_base0_y = random.randint(1, 5)
        box_base1_x = 10 - box_base0_x
        box_base1_y = 5 - box_base0_y
        player0_x = (box_base0_x - 1) * 10 + random.randint(1, 9)
        player0_y = (box_base0_y - 1) * 10 + random.randint(1, 5)
        player1_x = 100 - player0_x
        player1_y = 100 - player0_y
        self.hqs = [(player0_x, player0_y), (player1_x, player1_y)]
        base0 = unit.UnitObject(self.total_id, ai_id0, 'base', (player0_x, player0_y))
        self.units[ai_id0] = self.total_id
        self.total_id += 1
        base1 = unit.UnitObject(self.total_id, ai_id1, 'base', (player1_x, player1_y))
        self.units[ai_id1] = self.total_id
        self.total_id += 1
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
                tech0 = unit.UnitObject(None, None, 'teach_building', (tech_x, tech_y))
                tech1 = unit.UnitObject(None, None, 'teach_building', (tech_1_x, tech_1_y))
            if type_rand == 1:
                bank_x = (box_x - 1) * 10 + random.randint(1, 9)
                bank_y = (box_y - 1) * 10 + random.randint(1, 5)
                bank_1_x = 100 - bank_x
                bank_1_y = 100 - bank_y
                bank0 = unit.UnitObject(None, None, 'teach_building', (bank_x, bank_y))
                bank1 = unit.UnitObject(None, None, 'teach_building', (bank_1_x, bank_1_y))
            bank_and_teach -= 1
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
                building0 = unit.UnitObject(None, None, 'hack_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'hack_lab', (100 - building_x, 100 - building_y))
            if building_type == 2:
                building0 = unit.UnitObject(None, None, 'bid_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'bid_lab', (100 - building_x, 100 - building_y))
            if building_type == 3:
                building0 = unit.UnitObject(None, None, 'car_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'car_lab', (100 - building_x, 100 - building_y))
            if building_type == 4:
                building0 = unit.UnitObject(None, None, 'elec_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'elec_lab', (100 - building_x, 100 - building_y))
            if building_type == 5:
                building0 = unit.UnitObject(None, None, 'radiation_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'radiation_lab', (100 - building_x, 100 - building_y))
            if building_type == 6:
                building0 = unit.UnitObject(None, None, 'uav_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'uav_lab', (100 - building_x, 100 - building_y))
            if building_type == 7:
                building0 = unit.UnitObject(None, None, 'aircraft_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'aircraft_lab', (100 - building_x, 100 - building_y))
            if building_type == 8:
                building0 = unit.UnitObject(None, None, 'build_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'build_lab', (100 - building_x, 100 - building_y))
            if building_type == 9:
                building0 = unit.UnitObject(None, None, 'finance_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'finance_lab', (100 - building_x, 100 - building_y))
            if building_type == 10:
                building0 = unit.UnitObject(None, None, 'material_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'material_lab', (100 - building_x, 100 - building_y))
            if building_type == 11:
                building0 = unit.UnitObject(None, None, 'nano_lab', (building_x, building_y))
                building1 = unit.UnitObject(None, None, 'nano_lab', (100 - building_x, 100 - building_y))
            building_list.remove(building_type)
            total_building -= 1

    def windetermine_phase(self):
        # 胜利判定
        pass

    def cleanup_phase(self, ai_id):
        # 单位死亡判定
        # 单位死亡判定
        unit_obj = list(self.units.get(ai_id))  # 寻找传入ai_id对应的value
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
        """

        :type ai_id: int
        """
        pass

    def skill_phase(selfself, ai_id):
        # 技能结算
        """

        :type ai_id: int
        """
        pass

    def move_phase(self, ai_id):
        # 移动指令结算
        """

        :type ai_id: int
        """
        pass

    def produce_phase(self, ai_id, building_id):  # 需要多传入一个参数 建筑物的id以确定生产的兵种种类
        unit_obj = list(self.units.get(ai_id))  # 寻找传入ai_id对应的value
        meat_count = 0
        people_type = 0

        if building_id in unit_obj:
            if building_id.__type_name == 'hack_lab':
                people_type = 2
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['hack_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['hack_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['hack_lab']['tech_cost']:
                    return
                person = building0 = unit.UnitObject(self.total_id, ai_id, 'hacker', building_id.position)
                self.resource[ai_id]['money'] -= unit.origin_attribute['hack_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['hack_lab']['tech_cost']
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['hack_lab']['remain_people']
            if building_id.__type_name == 'bid_lab':
                people_type = 3
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['bid_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['bid_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['bid_lab']['tech_cost']:
                    return
                person = building0 = unit.UnitObject(self.total_id, ai_id, 'superman', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['bid_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['bid_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['bid_lab']['tech_cost']
            if building_id.__type_name == 'car_lab':
                people_type = 4
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['car_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['car_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['car_lab']['tech_cost']:
                    return
                person = building0 = unit.UnitObject(self.total_id, ai_id, 'battle_tank', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['car_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['car_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['car_lab']['tech_cost']
            if building_id.__type_name == 'elec_lab':
                people_type = 5
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['elec_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['elec_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['elec_lab']['tech_cost']:
                    return
                person = building0 = unit.UnitObject(self.total_id, ai_id, 'bolt_tank', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['elec_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['elec_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['elec_lab']['tech_cost']
            if building_id.__type_name == 'radiation_lab':
                people_type = 6
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['radiation_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['radiation_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['radiation_lab']['tech_cost']:
                    return
                person = building0 = unit.UnitObject(self.total_id, ai_id, 'nuke_tank', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['radiation_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['radiation_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['radiation_lab']['tech_cost']
            if building_id.__type_name == 'uav_lab':
                people_type = 7
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['uav_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['uav_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['uav_lab']['tech_cost']:
                    return
                person = building0 = unit.UnitObject(self.total_id, ai_id, 'uav', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['uav_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['uav_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['uav_lab']['tech_cost']
            if building_id.__type_name == 'aircraft_lab':
                people_type = 8
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['aircraft_lab']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['aircraft_lab']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['aircraft_lab']['tech_cost']:
                    return
                person = building0 = unit.UnitObject(self.total_id, ai_id, 'eagle', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['aircraft_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['aircraft_lab']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['aircraft_lab']['tech_cost']
            if building_id.__type_name == 'base':
                people_type = 1
                if self.resource[ai_id]['remain_people'] < unit.origin_attribute['base']['people_cost'] or \
                                self.resource[ai_id]['money'] < unit.origin_attribute['base']['money_cost'] or \
                                self.resource[ai_id]['tech'] < unit.origin_attribute['base']['tech_cost']:
                    return
                person = building0 = unit.UnitObject(self.total_id, ai_id, 'hacker', building_id.position)
                self.resource[ai_id]['remain_people'] -= unit.origin_attribute['base_lab']['remain_people']
                self.resource[ai_id]['money'] -= unit.origin_attribute['base']['money_cost']
                self.resource[ai_id]['tech'] -= unit.origin_attribute['base']['tech_cost']

        self.total_id += 1
        # 兵种获取指令结算
        """

        :type ai_id: int
        """
        pass

    def resource_phase(self, ai_id):
        # 资源结算
        bank = 0
        teaching_building = 0
        unit_obj = list(self.units.get(ai_id))  # 寻找传入ai_id对应的value
        for things in unit_obj:
            if things.__type_name == 'teach_building':
                teaching_building = teaching_building + 1
            if things.__type_name == 'bank':
                bank = bank + 1
        ################################################################################################################
        self.resource[ai_id]["money"] += bank * 500
        self.resource[ai_id]["tech"] += teaching_building * 50
        # """

        #:param ai_id: int
        # """
        # pass

    def capture_phase(self, ai_id):
        # 占领建筑阶段
        """

        :type ai_id: int
        """
        pass

    def next_tick(self):
        # 进入下一回合前通信等任务
        pass

    def to_string(self):
        # 将当前状态信息返回，用String,Json什么都行，你们自己起名字吧
        pass
