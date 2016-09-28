#暂定主基地branch属性为0, 1-8依次为小鲜肉，黑客，改造人战士，主战坦克，电子对抗坦克，核子坦克，无人机，鹰式战斗机,剩余9-19为建筑
#tuple内数据依次为【原始HP上限】，【原始最大速度】，【原始射程】，【原始防御】，【原始攻击】，【技能1CD】，【技能2CD】，【最大数量】，【人口占用】，【金钱消耗】，【科技消耗】
#建筑的最大数量，人口占用，金钱消耗，科技消耗均为0
origin_attribute = ((10000,0,10,0,10,None,1,0,0,0,0),#主基地数据
                   (100,3,1,10,0,None,None,None,1,100,0),(150,3,18,20,0,1,None,None,2,600,300),(500,4,10,150,15,1,50,1,10,2000,1500),#步兵
                   (900,7,14,200,100,10,None,None,4,1500,600),(500,6,12,100,200,10,None,None,3,1000,500),(700,5,20,150,300,10,150,1,10,4000,2000),#坦克
                   (300,12,10,50,5,1,None,None,2,400,100),(600,15,16,200,200,20,50,1),#飞机
                   (100000000,0,0,0,0,None,None,0,0,0,0),(100000000,0,0,0,0,None,None,0,0,0,0),(100000000,0,0,0,0,None,None,0,0,0,0),(100000000,0,0,0,0,None,None,0,0,0,0),#各种建筑，并没有什么区别
                   (100000000,0,0,0,0,None,None,0,0,0,0),(100000000,0,0,0,0,None,None,0,0,0,0),(100000000,0,0,0,0,None,None,0,0,0,0),
                   (100000000,0,0,0,0,None,None,0,0,0,0),(100000000,0,0,0,0,None,None,0,0,0,0),(100000000,0,0,0,0,None,None,0,0,0,0),(100000000,0,0,0,0,None,None,0,0,0,0))
#生产CD待定
origin_max_health = 0
origin_max_speed = 1
origin_shot_range = 2
origin_defense = 3
origin_attack = 4
skill_cd_1 = 5
skill_cd_2 = 6
max_account = 7
people_cost = 8
money_cost = 9
tech_cost =10
#------主基地
base = 0
#------单位
fresh_meat = 1
hack = 2
superman = 3
battle_tank = 4
electronic = 5
nuke_tank = 6
uav = 7
eagle_fighter = 8
#------生产建筑
hacker_academic = 9
biochemistry_lab = 10
vehicle_department = 11
electronic_battle_academic = 12
radiation_department = 13
uav_department = 14
advanced_aircraft_lab = 15
#------技能建筑
construction_department = 16
finance_lab = 17
material_lab = 18
nano_lab = 19
#物体名称
name_list =['主基地','小鲜肉','黑客','改造人战士','主战坦克','电子对抗坦克','核子坦克','无人战机','鹰式战斗机',
            '黑客学院','生化研究院','特种车辆系','电子对抗学院','辐射系','无人机系','高等飞行器研究院',
            '建造学院','社科金融研究院','特殊材料研究院','纳米科技研究院']

class UnitObject(object):
    #单位固有属性
    __unit_type = None #单位类型，建筑飞机坦克步兵
    __name = None #单位名字，要不要估计也无所谓
    __branch = None #具体类型
    #__origin_max_health = 500 #原始HP上限
    #__origin_max_speed = 6 #原始最大速度
    #__origin_shot_range = 15 #原始射程
    #__origin_defense = 150 #原始防御
    #__origin_attack = 200  #原始攻击



    #单位动态属性
    flag = None #所属阵营
    position = None #单位位置，目测是一个point之类的东西
    motor_type = None  # 移动方式，分地面和空中，精英步兵的技能会用到
    max_health_now = None #当前HP上限
    health_now = None  # 当前生命值
    max_speed_now = None #当前最大速度
    shot_range_now = None #当前射程(现阶段貌似没有提升射程的技能，不过先保留)
    defense_now = None #当前防御
    attack_now = None  #当前攻击

    def __init__(self, unit_id, flag, branch, position):
        self.unit_id = unit_id
        self.flag = flag
        self.position = position
        self.__branch = branch
        self.health_now = origin_attribute[self.__branch][origin_max_health]#单位生成时默认为最大血量，以下同理
        self.max_health_now = origin_attribute[self.__branch][origin_max_health]
        self.max_speed_now = origin_attribute[self.__branch][origin_max_speed]
        self.shot_range_now = origin_attribute[self.__branch][origin_shot_range]
        self.defense_now = origin_attribute[self.__branch][origin_defense]
        self.attack_now = origin_attribute[self.__branch][origin_attack]

        self.__max_num = origin_attribute[self.__branch][max_account]  # 最大生产数量
        self.__people_cost = origin_attribute[self.__branch][people_cost]  # 人口
        self.__money_cost = origin_attribute[self.__branch][money_cost]  # 金钱
        self.__tech_cost = origin_attribute[self.__branch][tech_cost]  # 科技

        self.__skill_1_cd = origin_attribute[self.__branch][skill_cd_1]
        self.__skill_2_cd = origin_attribute[self.__branch][skill_cd_2]

        self.__name = name_list[self.__branch]
        #输出基本信息，已实现，测试用

    def print_info(self):
        print('id:',self.unit_id,'阵营:',self.flag, '位置:',self.position, '兵种:',self.__branch,'名称:',self.__name,
              'HP:',self.health_now, 'MAXHP:',self.max_health_now, '速度:',self.max_speed_now, '射程:',self.shot_range_now, '防御:',self.defense_now, '攻击:',self.attack_now,
              '最大数量:',self.__max_num, '人口:',self.__people_cost, '金钱消耗:',self.__money_cost, '科技消耗:',self.__tech_cost, 'CD1:',self.__skill_1_cd, 'CD2:',self.__skill_2_cd)

    def set_unit_attribute(self, health_buff=1, attack_buff=1, defense_buff=1, speed_buff=1, shot_range_buff=1):
        pass #这里一并更新属性，如果担心性能的话可以分开写

    def get_cd(self):
        pass  #获取两类CD


class Building(UnitObject):
    __unit_type = 0
    flag = -1

    def captured(self, capture_flag):
        pass

class ConstructBuilding(Building):
    produce_time1 = None #上一次生产的时间，用于判断CD
    produce_object = None #生产单位类型，这里的实现我不太确定，如果直接实例化对应的类就不需要了，或者可以考虑直接按照类名实例化

    def produce(self, infantry_cost_buff=1, vehicle_cost_buff=1, aircraft_cost_buff=1):
        pass  #参数用于判断关于三种类型的生产消耗的被动技能

    def passive_skill(self):
        pass


class SkillBuilding(Building):

    def passive_skill_1(self):
        pass

    def passive_skill_2(self):
        pass

class MainBase(ConstructBuilding):#主基地
    __branch = 0
    def attack(self, target_id):
        pass

class FightingUnits(UnitObject):
    __producing_building = None  # 生产建筑
    attack_mode = None #攻击模式，例如可对空，可对坦克，可对步兵之类的
    attack_time = None  # 上次攻击时间

    def normal_attack(self, target_id):
        pass

    def move(self, destination):
        pass

class Infantry(FightingUnits):
    cure_rate =None #治疗比率

    def cure(self):
        pass


class Vehicle(UnitObject):
    repair_rate = None #维修比率，下同
    is_disable = False #是否被瘫痪
    disable_since = None #被瘫痪的时间点，用于判断瘫痪时间
    def repair(self):
        pass

class Aircraft(UnitObject):
    repair_rate = None

    def repair(self):
        pass

class FreshMeat(Infantry):#小鲜肉

    __branch = 1
    __producing_building = base  # 生产建筑

    def normal_attack(self, target_id):
        pass #机制不同

class Hacker(Infantry):#黑客

    __branch = 2
    __producing_building = hacker_academic  # 生产建筑

    def normal_attack(self, target_id):
        pass #机制不同

class XFighter(Infantry):#改造人战士

    __branch = 3
    __producing_building = biochemistry_lab  # 生产建筑
    skill_release_time = None  # 上次技能释放时间

    def skill_2(self):
        pass


class HeavyTank(Vehicle):  #主战坦克

    __branch = 4
    __producing_building = vehicle_department  # 生产建筑


class EMPTank(Vehicle):  #电子对抗坦克

    __branch = 5
    __producing_building = electronic_battle_academic # 生产建筑


class NuclearTank(Infantry):  # 核子坦克

    __branch = 6
    __producing_building = radiation_department  # 生产建筑
    __max_num = 1  # 最大生产数量
    __people_cost = 10  # 人口
    __money_cost = 4000  # 金钱
    __tech_cost = 2000 # 科技
    skill_release_time = None  # 上次技能释放时间

    def skill_2(self, target_pos, target_id=-1):#既可以对目标，也可以对地点，地点优先
        pass


class UAV(Aircraft):  #无人战机

    __branch = 7
    __producing_building = uav_department  # 生产建筑


class Eagle(Aircraft):  #鹰式战斗机

    __branch = 8
    __producing_building = advanced_aircraft_lab  # 生产建筑
    skill_release_time = None  # 上次技能释放时间

    def normal_attack(self, target_pos, target_id=-1):
        pass  # 机制略有不同,可aoe,
    def skill_2(self, target_pos, target_pos2, target_id=-1 ,target_id2=-1):  # 既可以对目标，也可以对地点，地点优先,同时打两个地方
        pass


class HackerAcademic(ConstructBuilding):#黑客学院
    __branch = 9
    def passive_skill(self):
        pass

    def produce(self, infantry_cost_buff=1, vehicle_cost_buff=1, aircraft_cost_buff=1):
        pass



class BiochemistryLab(ConstructBuilding):#生化研究院
    __branch = 10
    def passive_skill(self):
        pass

    def produce(self, infantry_cost_buff=1, vehicle_cost_buff=1, aircraft_cost_buff=1):
        pass


class VehicleDepartment(ConstructBuilding):#特种车辆系
    __branch = 11

    def passive_skill(self):
        pass

    def produce(self, infantry_cost_buff=1, vehicle_cost_buff=1, aircraft_cost_buff=1):
        pass


class ElectronicBattleAcademic(ConstructBuilding):#电子对抗学院
    __branch = 12

    def passive_skill(self):
        pass

    def produce(self, infantry_cost_buff=1, vehicle_cost_buff=1, aircraft_cost_buff=1):
        pass


class RadiationDepartment(ConstructBuilding):#辐射系
    __branch = 13

    def passive_skill(self):
        pass

    def produce(self, infantry_cost_buff=1, vehicle_cost_buff=1, aircraft_cost_buff=1):
        pass


class UAVDepartment(ConstructBuilding):#无人机系
    __branch = 14

    def passive_skill(self):
        pass

    def produce(self, infantry_cost_buff=1, vehicle_cost_buff=1, aircraft_cost_buff=1):
        pass


class AdvancedAircraftLab(ConstructBuilding):#高等飞行器研究院
    __branch = 15

    def passive_skill(self):
        pass

    def produce(self, infantry_cost_buff=1, vehicle_cost_buff=1, aircraft_cost_buff=1):
        pass


class ConstructionDepartment(SkillBuilding):#建造学院
    __branch = 16

    def passive_skill_1(self):
        pass

    def passive_skill_2(self):
        pass


class FinanceLab(SkillBuilding):#社科金融学院
    __branch = 17

    def passive_skill_1(self):
        pass

    def passive_skill_2(self):
        pass


class MaterialLab(SkillBuilding):#特殊材料学院
    __branch = 18

    def passive_skill_1(self):
        pass

    def passive_skill_2(self):
        pass


class NanoLab(SkillBuilding):#纳米研究院
    __branch = 19

    def passive_skill_1(self):
        pass

    def passive_skill_2(self):
        pass

#-------------测试一发，并没有卵用-------------
tank = NuclearTank(1, 1, nuke_tank, 8823)
tank.health_now -= 50
tank.print_info()
