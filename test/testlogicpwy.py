import unittest
from src import unit
from src import gamemain
from src.unit import origin_attribute

test_buff = unit.test_buff

class testclean(unittest.TestCase):
    def setUp(self):
        self.test_obj = gamemain.GameMain()  # __init__()写好后加入参数
        self.test_obj.units[0] = unit.UnitObject(0, 0, 'meat', (1, 1), test_buff)  # 加入一个编号为0的单位
        self.test_obj.units[1] = unit.UnitObject(0, 0, 'eagle', (1, 1), test_buff)

    def test_clean(self):
        self.test_obj.units[0].health_now = 0  # 生命值置零情况
        people = self.test_obj.resource[0]['remain_people']
        self.test_obj.cleanup_phase()
        id_collection = list(self.test_obj.units)
        self.assertTrue(0 in id_collection)  # 删除之后检查是否还在units中
        self.assertTrue(people == self.test_obj.resource[0]['remain_people'] + origin_attribute['meat'][
            'people_cost'])  # 检查人口是否变化正确
        self.test_obj.units[1].hacked_point = self.test_obj.units[1].max_health_now  # 被黑的情况
        people = self.test_obj.resource[0]['remain_people']
        self.test_obj.cleanup_phase()
        id_collection = list(self.test_obj.units)
        self.assertTrue(1 in id_collection)
        self.assertTrue(
            people == self.test_obj.resource[0]['remain_people'] + origin_attribute['eagle']['people_cost'])

class testmove_phase(unittest.TestCase):
    def setUp(self):
        self.test_obj = gamemain.GameMain()  # __init__()写好后加入参数
        self.test_obj.units[0] = unit.UnitObject(0, 0, 'meat', (1, 1), test_buff)  # 加入一个编号为0的单位

    def test_speed(self):  # 速度测试
        for building in self.test_obj.buildings:
            building.position = (50, 50)
        for building in self.test_obj.units.values():
            if building.Get_unit_type() == 4 or building.Get_unit_type() == 0:
                building.position = (50, 50)
        i = self.test_obj.units[0].max_speed_now
        self.test_obj.units[0].position = (1, 1)  # 初始位置为（1,1）
        self.test_obj.move_instr_0 = [[1, 1, 1 + i]]
        self.test_obj.move_phase()
        self.assertTrue(self.test_obj.units[0].position[1] == 1 + i)  # 测试合法移动是否有效

    def test_wrong_speed(self):  # 非法速度测试
        for building in self.test_obj.buildings:
            building.position = (50, 50)
        for building in self.test_obj.units.values():
            if building.Get_unit_type() == 4 or building.Get_unit_type() == 0:
                building.position = (50, 50)
        i = self.test_obj.units[0].max_speed_now + 1
        self.test_obj.units[0].position = (1, 1)  # 初始位置为（1,1）
        self.test_obj.move_instr_0 = [[1, 1, 1 + i]]
        self.test_obj.move_phase()
        self.assertTrue(self.test_obj.units[0].position[1] != 1 + i)  # 测试非法移动是否无效

    def test_move_to_building(self):  # 非法移动测试
        for building in self.test_obj.buildings:
            building.position = (50, 50)
        for building in self.test_obj.units.values():
            if building.Get_unit_type() == 4:
                building.position = (49, 50)
            if building.Get_unit_type() == 0:
                building.position = (48, 50)
        self.test_obj.units[100] = unit.UnitObject(100, 0, 'meat', (49, 49), test_buff)
        self.test_obj.units[101] = unit.UnitObject(101, 0, 'meat', (49, 49), test_buff)
        self.test_obj.units[102] = unit.UnitObject(102, 0, 'meat', (49, 49), test_buff)
        self.test_obj.move_instr_0.append([100, 50, 50])
        self.test_obj.move_instr_0.append([100, 49, 50])
        self.test_obj.move_instr_0.append([100, 48, 50])
        self.assertTrue(self.test_obj.units[100].position != (50, 50))
        self.assertTrue(self.test_obj.units[101].position != (49, 50))
        self.assertTrue(self.test_obj.units[102].position != (48, 50))

class testcapture_phase(unittest.TestCase):  # 每个对象只测试一次
    def setUp(self):
        self.test_obj = gamemain.GameMain()  # __init__()写好后加入参数
        self.test_obj.units[0] = unit.UnitObject(0, 0, 'meat', (1, 2), test_buff)  # 加入一个编号为0的单位
        self.test_obj.units[1] = unit.UnitObject(1, 1, 'meat', (1, 2), test_buff)
        self.test_obj.units[2] = unit.UnitObject(2, 1, 'meat', (1, 2), test_buff)
        self.test_obj.units[3] = unit.UnitObject(3, 0, 'superman', (1, 2), test_buff)
        self.test_obj.buildings[0] = unit.UnitObject(99, 2, 'hack_lab', (1, 1), test_buff)

    def test1(self):  # 测试一个小鲜肉占领的情况(实在想不出命名orz)
        self.test_obj.capture_instr_0 = [[self.test_obj.units[0].unit_id, self.test_obj.buildings[0].unit_id]]
        self.test_obj.capture_phase()
        self.assertTrue(self.test_obj.buildings[0].flag == 0)
        id_collection = list(self.test_obj.units)
        self.assertTrue((not (0 in id_collection)) or (self.test_obj.units[0].health_now <= 0))  # 小鲜肉被删或者生命置0

    def test2(self):  # 测试两个小鲜肉和一个争夺占领的情况
        self.test_obj.capture_instr_0 = [[self.test_obj.units[0].unit_id, self.test_obj.buildings[0].unit_id]]
        self.test_obj.capture_instr_1 = [[self.test_obj.units[1].unit_id, self.test_obj.buildings[0].unit_id],
                                         [self.test_obj.units[2].unit_id, self.test_obj.buildings[0].unit_id]]
        self.test_obj.capture_phase()
        self.assertTrue(self.test_obj.buildings[0].flag == 1)
        id_collection = list(self.test_obj.units)
        self.assertTrue(((not 0 in id_collection) and (not 1 in id_collection) and (not 2 in id_collection)) or \
                        ((self.test_obj.units[0].health_now <= 0) and (self.test_obj.units[1].health_now <= 0) and (
                        self.test_obj.units[2].health_now <= 0)))  # 三个小鲜肉全部死亡

    def test3(self):  # 一方先占领，然后另一方重新占领
        self.test_obj.capture_instr_0 = [[self.test_obj.units[0].unit_id, self.test_obj.buildings[0].unit_id]]
        self.test_obj.capture_phase()
        self.test_obj.capture_instr_1 = [[self.test_obj.units[1].unit_id, self.test_obj.buildings[0].unit_id]]
        self.test_obj.capture_phase()
        self.assertTrue(self.test_obj.buildings[0].flag == 1)

    def test4(self):  # 测试一些错误情况，非小鲜肉发动占领
        self.test_obj.capture_instr_0 = [[self.test_obj.units[3].unit_id, self.test_obj.buildings[0].unit_id]]
        self.test_obj.capture_phase()
        self.assertTrue(self.test_obj.buildings[0].flag != 0)

    def test5(self):  # 位置错误占领
        self.test_obj.units[0].position = (2, 2)
        self.test_obj.capture_instr_0 = [[self.test_obj.units[0].unit_id, self.test_obj.buildings[0].unit_id]]
        self.assertTrue(self.test_obj.buildings[0].flag != 0)

class testproduce_phase(unittest.TestCase):
    def setUp(self):
        self.test_obj = gamemain.GameMain()

    def testmeat(self):  # 测试是否能够生产小鲜肉，生产的位置，阵营，id，类型是否正确
        self.test_obj.produce_instr_0 = [self.test_obj.hqs[0].unit_id]
        self.test_obj.produce_phase()
        self.assertTrue(self.test_obj.total_id - 1 == self.test_obj.units[self.test_obj.total_id - 1].unit_id)
        self.assertTrue(self.test_obj.units[self.test_obj.total_id - 1].flag == self.test_obj.hqs[0].flag)
        self.assertTrue(self.test_obj.units[self.test_obj.total_id - 1].position == self.test_obj.hqs[0].position)
        self.assertTrue(self.test_obj.units[self.test_obj.total_id - 1].Get_type_name() == 'meat')

    def testhacker(self):  # 测试是否能够生产黑客（仅测试单位数量是否增加）
        for building in self.test_obj.buildings:
            if building.Get_type_name() == 'hack_lab':
                self.test_obj.produce_instr_0.append(building.unit_id)
                building.flag = 0;
        self.tem_unit = len(self.test_obj.units)
        self.test_obj.produce_phase()
        self.assertTrue(len(self.test_obj.units) != self.tem_unit)

    def test_no_remain_people(self):  # 生产101个小鲜肉，是否仅生产出100个(人口测试)
        for i in range(101):
            self.test_obj.produce_instr_0.append(self.test_obj.hqs[0].unit_id)
        self.tem_unit = len(self.test_obj.units)
        self.test_obj.produce_phase()
        self.assertTrue(len(self.test_obj.units) == self.tem_unit + 100)

    def test_max_amount(self):  # 生产多个核子坦克，鹰式战斗机，改造人，是否仅生产三个（数量限制测试）
        for building in self.test_obj.buildings:
            if building.Get_type_name() == 'bid_lab':
                self.test_obj.produce_instr_0.append(building.unit_id)
                self.test_obj.produce_instr_0.append(building.unit_id)
                building.flag = 0;
                building.print_info()
            if building.Get_type_name() == 'radiation_lab':
                self.test_obj.produce_instr_0.append(building.unit_id)
                self.test_obj.produce_instr_0.append(building.unit_id)
                building.flag = 0;
            if building.Get_type_name() == 'aircraft_lab':
                self.test_obj.produce_instr_0.append(building.unit_id)
                self.test_obj.produce_instr_0.append(building.unit_id)
                building.flag = 0;
        self.tem_unit = len(self.test_obj.units)
        self.test_obj.produce_phase()
        self.assertTrue(len(self.test_obj.units) == self.tem_unit + 3)
