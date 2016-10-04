#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from src import unit

class GameMain:
    units = {}  # 单位dict
    hqs = []  # 主基地
    buildings = []  # 中立建筑
    #turn_flag = 0  # 谁的回合
    turn_num = 0  # 回合数
    phase_num = 0  # 回合阶段指示
    skill_instr_0=[]#ai0的当前回合指令
    skill_instr_1=[]#ai1的当前回合制令
    produce_instr_0=[]
    produce_instr_1=[]
    move_instr_0=[]
    move_instr_1=[]
    capture_instr_0=[]
    capture_instr_1=[]
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

    def __init__(self):
        pass

    def windetermine_phase(self):
        # 胜利判定
        pass

    def cleanup_phase(self):
        # 单位死亡判定

        pass

    def skill_phase(selfself):
        # 技能结算

        pass

    def move_phase(self):
        # 移动指令结算

        pass

    def produce_phase(self):
        # 兵种获取指令结算

        pass

    def capture_phase(self):
        # 占领建筑阶段
        pass

    def fetch_instruction(self):
        #获取指令存入两个指令list
        pass

    def check_legal(self):
        #检查双方指令是否合法，去重
        pass

    def next_tick(self):
        # 获取指令，指令检测合法与去重，回合演算
        self.check_legal()
        self.skill_phase()
        self.cleanup_phase()
        self.windetermine_phase()
        self.move_phase()
        self.produce_phase()
        self.capture_phase()
        pass

    def to_string(self):
        # 将当前状态信息返回，用String,Json什么都行，你们自己起名字吧
        pass
