#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#type_name
BASE = 0
INFANTRY = 1
VEHICLE = 2
AIRCRAFT = 3
BUILDING = 4
#buff全局变量

FLAG_0 = 0
FLAG_1 = 1


#暂定主基地为0, 1-8依次为小鲜肉，黑客，改造人战士，主战坦克，电子对抗坦克，核子坦克，无人机，鹰式战斗机,剩余9-21为建筑

#物体名称

#name_list ={'base':0,'meat':1,'hacker':2,'superman':3,'battle_tank':4,'bolt_tank':5,'nuke_tank':6,'uav':7,'eagle':8,
#            'hack_lab':9,'bid_lab':10,'car_lab':11,'elec_lab':12,'radiation_lab':13,'uav_lab':14,'aircraft_lab':15,
#           'build_lab':16,'finance_lab':17,'material_lab':18,'nano_lab':19}

#dic内数据依次为【单位大类】【原始HP上限】，【原始最大速度】，【原始射程】，【原始防御】，【原始攻击】，【技能1CD】，【技能2CD】，【最大数量】，【人口占用】，【金钱消耗】，【科技消耗】
#建筑的最大数量，人口占用，金钱消耗，科技消耗均为0

origin_attribute = {
    'base':          {'unit_type':BASE,    'origin_max_health':10000,    'origin_max_speed':0, 'origin_shot_range':10,'origin_defense':0,  'origin_attack':10, 'skill_cd_1':None,'skill_cd_2':1,    'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'meat':          {'unit_type':INFANTRY,'origin_max_health':100,      'origin_max_speed':3, 'origin_shot_range':1, 'origin_defense':10, 'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':None,'people_cost':1, 'money_cost':100, 'tech_cost':0   },
    'hacker':        {'unit_type':INFANTRY,'origin_max_health':150,      'origin_max_speed':3, 'origin_shot_range':18,'origin_defense':20, 'origin_attack':0,  'skill_cd_1':1,   'skill_cd_2':None, 'max_account':None,'people_cost':2, 'money_cost':600, 'tech_cost':300 },
    'superman':      {'unit_type':INFANTRY,'origin_max_health':500,      'origin_max_speed':4, 'origin_shot_range':10,'origin_defense':150,'origin_attack':15, 'skill_cd_1':1,   'skill_cd_2':50,   'max_account':1,   'people_cost':10,'money_cost':2000,'tech_cost':1500},
    'battle_tank':   {'unit_type':VEHICLE, 'origin_max_health':900,      'origin_max_speed':7, 'origin_shot_range':14,'origin_defense':200,'origin_attack':100,'skill_cd_1':10,  'skill_cd_2':None, 'max_account':None,'people_cost':4, 'money_cost':1500,'tech_cost':600 },
    'bolt_tank':     {'unit_type':VEHICLE, 'origin_max_health':500,      'origin_max_speed':6, 'origin_shot_range':12,'origin_defense':100,'origin_attack':200,'skill_cd_1':10,  'skill_cd_2':None, 'max_account':None,'people_cost':3, 'money_cost':1000,'tech_cost':500 },
    'nuke_tank':     {'unit_type':VEHICLE, 'origin_max_health':700,      'origin_max_speed':5, 'origin_shot_range':20,'origin_defense':150,'origin_attack':300,'skill_cd_1':10,  'skill_cd_2':150,  'max_account':1,   'people_cost':10,'money_cost':4000,'tech_cost':2000},
    'uav':           {'unit_type':AIRCRAFT,'origin_max_health':300,      'origin_max_speed':12,'origin_shot_range':10,'origin_defense':50, 'origin_attack':5,  'skill_cd_1':1,   'skill_cd_2':None, 'max_account':None,'people_cost':2, 'money_cost':400, 'tech_cost':100 },
    'eagle':         {'unit_type':AIRCRAFT,'origin_max_health':600,      'origin_max_speed':15,'origin_shot_range':16,'origin_defense':200,'origin_attack':200,'skill_cd_1':20,  'skill_cd_2':50,   'max_account':1,   'people_cost':1, 'money_cost':3000,'tech_cost':1500},
    'hack_lab':      {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'bid_lab':       {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'car_lab':       {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'elec_lab':      {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'radiation_lab': {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'uav_lab':       {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'aircraft_lab':  {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'build_lab':     {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'finance_lab':   {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'material_lab':  {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'nano_lab':      {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'teach_building':{'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   },
    'bank':          {'unit_type':BUILDING,'origin_max_health':100000000,'origin_max_speed':0, 'origin_shot_range':0, 'origin_defense':0,  'origin_attack':0,  'skill_cd_1':None,'skill_cd_2':None, 'max_account':0,   'people_cost':0, 'money_cost':0,   'tech_cost':0   }
}


#-----------------------------------
#生产CD待定
#-----------------------------------

class UnitObject(object):
    #单位固有属性
    __unit_type = None #单位大类，建筑4飞机3坦克2步兵1基地0
    __type_name = None #具体类型
    __producing_building = None #生产建筑


    #单位动态属性
    unit_id = 0
    name = None  # 单位名字，给选手闹着玩的
    flag = None #所属阵营
    position = None #单位位置，目测是一个point之类的东西
    motor_type = None  # 移动方式，分地面和空中，精英步兵的技能会用到
    max_health_now = None #当前HP上限
    health_now = None  # 当前生命值
    max_speed_now = None #当前最大速度
    shot_range_now = None #当前射程(现阶段貌似没有提升射程的技能，不过先保留)
    defense_now = None #当前防御
    attack_now = None  #当前攻击
    healing_rate = None  # 治疗/维修速率
    hacked_point = None #被黑的点数
    is_disable = False  # 是否被瘫痪
    disable_since = None  # 被瘫痪的时间点，用于判断瘫痪时间
    skill_last_release_time1 = None #上次技能1释放时间
    skill_last_release_time2 = None #上次技能2释放时间
    attack_mode = None #攻击模式，例如可对空，可对坦克，可对步兵之类的

    def __init__(self, unit_id, flag, type_name, position,buff=None):
        self.unit_id = unit_id
        self.flag = flag
        self.position = position
        self.__type_name = type_name
        self.__unit_type = origin_attribute[type_name]['unit_type']

        self.skill_last_release_time1 = -1000
        self.skill_last_release_time2 = -1000
        if (self.__unit_type!=BASE and self.__unit_type!=BUILDING):
            self.health_now = origin_attribute[type_name]['origin_max_health'] * (1+buff[flag][self.__unit_type]['health_buff'])   #单位生成时默认为最大血量，以下同理
            self.max_health_now = origin_attribute[type_name]['origin_max_health'] * (1+buff[flag][self.__unit_type]['health_buff'])
            self.max_speed_now = origin_attribute[type_name]['origin_max_speed'] * (1+buff[flag][self.__unit_type]['speed_buff'])
            self.shot_range_now = origin_attribute[type_name]['origin_shot_range'] * (1+buff[flag][self.__unit_type]['shot_range_buff'])
            self.defense_now = origin_attribute[type_name]['origin_defense'] * (1+buff[flag][self.__unit_type]['defense_buff'])
            self.attack_now = origin_attribute[type_name]['origin_attack'] * (1+buff[flag][self.__unit_type]['attack_buff'])
        else:
            self.health_now = origin_attribute[type_name]['origin_max_health']    #单位生成时默认为最大血量，以下同理
            self.max_health_now = origin_attribute[type_name]['origin_max_health']
            self.max_speed_now = origin_attribute[type_name]['origin_max_speed']
            self.shot_range_now = origin_attribute[type_name]['origin_shot_range']
            self.defense_now = origin_attribute[type_name]['origin_defense']
            self.attack_now = origin_attribute[type_name]['origin_attack']

        self.__skill_1_cd = origin_attribute[type_name]['skill_cd_1']
        self.__skill_2_cd = origin_attribute[type_name]['skill_cd_2']

        #输出基本信息，已实现，测试用

    def print_info(self):
        print('id:',self.unit_id,'阵营:',self.flag, '位置:',self.position, '类型:',self.__unit_type,'兵种:',self.__type_name,'自定名称:',self.name,
              'HP:',self.health_now, 'MAXHP:',self.max_health_now, '速度:',self.max_speed_now, '射程:',self.shot_range_now, '防御:',self.defense_now, '攻击:',self.attack_now,
              '最大数量:',origin_attribute[self.__type_name]['max_account'],
              '人口:',origin_attribute[self.__type_name]['people_cost'],
              '金钱消耗:',origin_attribute[self.__type_name]['money_cost'],
              '科技消耗:',origin_attribute[self.__type_name]['tech_cost'],
              'CD1:',self.__skill_1_cd, 'CD2:',self.__skill_2_cd)

    def Get_unit_type(self):
        return self.__unit_type

    def Get_type_name(self):
        return self.__type_name

    #写了一个接口虽然不觉得有什么卵用
    def reset_attribute(self, buff=None, **kwargs):
        if 'health' in kwargs:
            self.health_now = kwargs['health']
        if 'max_health' in kwargs:
            self.max_health_now = kwargs['max_health']
        if 'speed' in kwargs:
            self.max_speed_now = kwargs['speed']
        if 'shot_range' in kwargs:
            self.shot_range_now = kwargs['shot_range']
        if 'defense' in kwargs:
            self.defense_now = kwargs['defense']
        if 'attack' in kwargs:
            self.attack_now = kwargs['attack']
        if 'is_disable' in kwargs:
            self.is_disable = kwargs['is_disable']
        if 'hacked_point' in kwargs:
            self.hacked_point = kwargs['hacked_point']
        if 'motor_type' in kwargs:
            self.motor_type = kwargs['motor_type']
        if 'skill_last_release_time1' in kwargs:
            self.skill_last_release_time2 = kwargs['skill_last_release_time1']
        if 'skill_last_release_time2' in kwargs:
            self.skill_last_release_time2 = kwargs['skill_last_release_time2']

        if (self.__unit_type!=BASE and self.__unit_type!=BUILDING):
            self.max_health_now = origin_attribute[self.__type_name]['origin_max_health'] * (1 + buff[self.flag][self.__unit_type]['health_buff'])
            self.max_speed_now = origin_attribute[self.__type_name]['origin_max_speed'] * (1 + buff[self.flag][self.__unit_type]['speed_buff'])
            self.shot_range_now = origin_attribute[self.__type_name]['origin_shot_range'] * (1 + buff[self.flag][self.__unit_type]['shot_range_buff'])
            self.defense_now = origin_attribute[self.__type_name]['origin_defense'] * (1 + buff[self.flag][self.__unit_type]['defense_buff'])
            self.attack_now = origin_attribute[self.__type_name]['origin_attack'] * (1 + buff[self.flag][self.__unit_type]['attack_buff'])

        #虽然我这里留下了接口，但讲道理以下这几个东西最好直接访问来改变......如果需要其他的话在以下自行添加
        if 'position' in kwargs:
            self.attack_now = kwargs['position']
        if 'attack_mode' in kwargs:
            self.attack_now = kwargs['attack_mode']
        if 'motor_type' in kwargs:
            self.attack_now = kwargs['motor_type']

#以下这个buff是方便测试的，无实际作用
test_buff = {
    FLAG_0: {
        INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                   'shot_range_buff': 0.0},
        VEHICLE: {'health_buff': 0.5, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                  'shot_range_buff': 0.0},
        AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                        'shot_range_buff': 0.0}
    },
    FLAG_1: {
        INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                   'shot_range_buff': 0.0},
        VEHICLE: {'health_buff': 0.6, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                  'shot_range_buff': 0.0},
        AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                        'shot_range_buff': 0.0}
    }
}


#-------------实例化-------------
'''
tank = UnitObject(1, 1, 'nuke_tank', (22, 33), test_buff)
tank.print_info()
tank.reset_attribute(test_buff, speed=15, health=6666)
tank.print_info()
'''