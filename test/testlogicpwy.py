import unittest
from src import unit
from src import gamemain.py
from src.unit import origin_attribute

class testclean(unittest.testcase):
    def setUp(self):
        test_obj = gamemain.Gamemain()                                      #__init__()写好后加入参数
        test_obj.units[0] = unit.UnitObject(0,0,'meat',(1,1),test_buff)      #加入一个编号为0的单位
        test_obj.units[1] = unit.UnitObject(0,0,'eagle',(1,1),test_buff)

    def test_clean(self):
        test_obj.units[0].health_now = 0                                    #生命值置零情况
        people = test_obj.resource[0]['remain_people']
        test_obj.cleanup_phase()
        id_collection = list(test_obj.units)    
        self.assertTrue(0 in id_collection)                                 #删除之后检查是否还在units中
        self.assertTrue(people == test_obj.resource[0]['remain_people'] - origin_attribute['meat']['people_cost'])  #检查人口是否变化正确
       
        test_obj.units[1].hacked_point = test_obj.units[1].max_health_now   #被黑的情况
        people = test_obj.resource[0]['remain_people']
        test_obj.cleanup_phase()
        id_collection = list(test_obj.units)
        self.assertTrue(1 in id_collection)
        self.assertTrue(people == test_obj.resource[0]['remain_people'] - origin_attribute['eagle']['people_cost'])

class testmove_phase(unittest.testcase):
    def setUp(self):
        test_obj = gamemain.Gamemain()                                      #__init__()写好后加入参数
        test_obj.units[0] = unit.UnitObject(0,0,'meat',(1,1),test_buff)     #加入一个编号为0的单位
    
    def test_move(self):
        for i in range(test_obj.units[1].max_speed_now + 1):
            test_obj.units[1].position = (1,1)                              #初始位置为（1,1）
            test_obj.move_instr_0 = [[1,1,1+i]]                             #移动距离从0到最大速度
            test_obj.move_phase()
            self.assertTrue(test_obj.units[1].position[1] == 1+i )          #测试合法移动是否有效
        test_obj.units[1].position = (1,1)
        test_obj.move_instr_0 = [[1,1,2+test_obj.units[1].maxspeed_now]]    #测试移动距离是最大速度加1
        test_obj.move_phase()                                          
        self.assertTrue(test_obj.units[1].position[1] == 1)                 #指令非法无效

class testcapture_phase(unittest.testcase):                                 #每个对象只测试一次
    def setUp(self):
        test_obj = gamemain.Gamemain()                                      #__init__()写好后加入参数
        test_obj.units[0] = unit.UnitObject(0,0,'meat',(1,2),test_buff)      #加入一个编号为0的单位
        test_obj.units[1] = unit.UnitObject(1,1,'meat',(1,2),test_buff)
        test_obj.units[2] = unit.UnitObject(2,1,'meat',(1,2),test_buff)
        test_obj.units[3] = unit.UnitObject(3,0,'superman',(1,2),testbuff)
        test_obj.building[0] = unit.UnitObject(99,2,'hack_lab',(1,1),test_buff)

    def test1(self):                                                        #测试一个小鲜肉占领的情况(实在想不出命名orz)
        test_obj.capture_instr_0 = [[test_obj.units[0].unit_id,test_obj.building[0].unit_id]]
        test_obj.capture_phase()
        self.assertTrue(test_obj.building[0].flag == 0)
        id_collection = list(test_obj.units)
        self.assertTrue((not (0 in id_collection)) or (test_obj.units[0].health_now <= 0))    #小鲜肉被删或者生命置0
    
    def test2(self):                                                        #测试两个小鲜肉和一个争夺占领的情况
        test_obj.capture_instr_0 = [[test_obj.units[0].unit_id,test_obj.building[0].unit_id]]
        test_obj.capture_instr_1 = [[test_obj.units[1].unit_id,test_obj.building[0].unit_id],[test_obj.units[2].unit_id,test_obj.building[0].unit_id]]
        test_obj.capture_phase()
        self.assertTrue(test_obj.building[0].flag == 1)
        id_collection = list(test_obj.units)
        self.assertTrue(((not 0 in id_collection) and (not 1 in id_collection) and (not 2 in id_collection)) or \
        ((test_obj.units[0].health_now<= 0) and (test_obj.units[1].health_now <= 0) and (test_obj.units[2].health_now <= 0))) #三个小鲜肉全部死亡
        
    def test3(self):                                                        #一方先占领，然后另一方重新占领
        test_obj.capture_instr_0 = [[test_obj.units[0].unit_id,test_obj.building[0].unit_id]]
        test_obj.capture_phase()
        test_obj.capture_instr_1 = [[test_obj.units[1].unit_id,test_obj.building[0].unit_id]]
        test_obj.capture_phase()
        self.assertTrue(test_obj.building[0].flag == 1)

    def test4(self):                                                        #测试一些错误情况，非小鲜肉发动占领
        test_obj.capture_instr_0 = [[test_obj.units[3].unit_id,test_obj.building[0].unit_id]]
        test_obj.capture_phase()
        self.assertTrue(test_obj.building[0].flag != 0)

    def test5(self):                                                        #位置错误占领
        test_obj.units[0].position = (2,2)
        test_obj.capture_instr_0 = [[test_obj.units[0].unit_id,test_obj.building[0].unit_id]]
        self.assertTrue(test_obj.building[0].flag != 0)
