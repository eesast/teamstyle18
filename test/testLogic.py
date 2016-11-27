#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from src import gamemain, unit
def calculateInjure(attackvalue, defendvalue):
    return attackvalue * ( 1- defendvalue / 1000)
class Skill_phaseTest(unittest.TestCase):
    def setUp(self):
        self.orders = [["bolt_tank_skill1", 1, 12],     #0
                       ["bolt_tank_skill1", 1, 8],      #1
                       ["bolt_tank_skill1", 1, 10],     #2
                       ["hacker_skill1", 2, 12],        #3
                       ["uav", 5, 10],                  #4
                       ["battle_tank_skill1", 3, 10],   #5
                       ["nuke_tank_skill1", 16, 8],      #6
                       ["nuke_tank_skill2", 16, 2],      #7
                       ["eagle_skill1", 4, 1],          #8
                       ["eagle_skill2", 0, 1],          #9
                       ["superman_skill1", 1, 0],          #10
                       ["superman_skill2", 1, 0],        #11    #先存好所有需要测试的指令
                       ["uav", 5, 8],          #12
                       ["battle_tank_skill1", 3, 15]  ]  #13
        self.testOrders = list()  #将测试的指令
        self.game = gamemain.GameMain()         #初始化游戏
        testBuff = self.game.buff  # 设置属性加成
        self.units =  [ unit.UnitObject(1, 0, "bolt_tank", (3, 4),  testBuff),   #0
                        unit.UnitObject(2, 0, "hacker", (6, 8), testBuff),       #1
                        unit.UnitObject(3, 0, "battle_tank", (10, 10), testBuff),#2
                        unit.UnitObject(4, 0, "eagle", (20, 20), testBuff),     #3
                        unit.UnitObject(5, 0, "uav", (3, 3),testBuff),          #4
                        unit.UnitObject(6, 0, "superman", (35, 35), testBuff),  #5
                        unit.UnitObject(7, 0, "eagle", (50, 50), testBuff),     #6
                        unit.UnitObject(8, 1, "bolt_tank", (3, 5), testBuff),   #7
                        unit.UnitObject(9, 1, "hacker", (6, 8), testBuff),      #8
                        unit.UnitObject(10, 1, "battle_tank", (13, 13), testBuff),#9
                        unit.UnitObject(11, 1, "eagle", (20, 20), testBuff),     #10
                        unit.UnitObject(12, 1, "uav", (3, 3), testBuff),         #11
                        unit.UnitObject(13, 1, "superman", (35, 35), testBuff),  #12
                        unit.UnitObject(14, 1, "eagle", (50, 50), testBuff),    #13
                        unit.UnitObject(15, 1, "meat", (8, 8), testBuff),# 14
                        unit.UnitObject(16, 0, "nuke_tank", (10, 11), testBuff) ]   # 15  #生成测试需要的单位
        for i in range(len(self.units)):
            self.game.units[i+1] = self.units[i]

    def testBoltTankSkill(self):
        self.testOrders.append(self.orders[0])
        self.assertEqual(self.game.units[1].health_now, 500)
        self.assertEqual(self.game.units[12].health_now, 300)
        self.game.skill_phase(self.testOrders)
        expectHealth_now = 300 - calculateInjure(200, 50)    #used to record the HP of attacked object now
        self.assertEqual(self.game.units[12].health_now, expectHealth_now)  #测试电子对抗坦克进攻射程内的飞机
        self.game.units[12].position = (16, 4)
        self.testOrders.clear()
        self.testOrders.append(self.orders[0])
        self.game.skill_phase(self.testOrders)
        self.assertEqual(self.game.units[12].health_now, expectHealth_now)  #测试电子对抗坦克攻击射程外的飞机
        self.testOrders.clear()
        self.testOrders.append(self.orders[1])  # bolt_tank attack bolt_tank
        self.game.skill_phase(self.testOrders)
        expectHealth_now = 500 - calculateInjure(200, 100)
        self.assertEqual(self.game.units[8].health_now, expectHealth_now)
        self.game.units[8].hwalth_now = 500
        self.game.units[12].health_now = 300

    def testHackerSkill(self):
        self.testOrders.clear()
        self.testOrders.append(self.orders[1])

    def testUAV(self):
        self.testOrders.clear()
        self.testOrders.append(self.orders[4])
        self.game.skill_phase(self.testOrders)
        expecthealth_now = 900 - calculateInjure(5, 200)
        self.assertEqual(self.game.units[10].health_now, expecthealth_now)  # uav attack battle tank inside the range
        self.testOrders.clear()
        self.testOrders.append(self.orders[4])
        self.game.units[8].position = (12, 12)
        self.game.skill_phase(self.testOrders)
        self.assertEqual(self.game.units[8].health_now, expecthealth_now) #uav attack bolt tank outside the range
        self.testOrders.clear()
        self.testOrders.append(self.orders[12])
        self.game.skill_phase(self.testOrders)
        expecthealth_now = 500 - calculateInjure(5, 100)
        self.assertEqual(self.game.units[8].health_now, expecthealth_now)  # uav attack bolt tank inside the range

        self.game.units[10].health_now = 900   # reset the health
        self.game.units[8].health_now = 500

    def testBattleTankSkill1(self):
        self.testOrders.clear()
        self.testOrders.append(self.orders[5])
        self.game.skill_phase(self.testOrders)
        expecthealth_now = 900 - calculateInjure(100, 200)
        self.assertEqual(self.game.units[10].health_now, expecthealth_now) # battle tank attack battle tank inside the range

        self.testOrders.clear()
        self.testOrders.append(self.orders[5])
        self.game.skill_phase(self.testOrders)
        self.game.units[10].position = (20, 20)
        self.assertEqual(self.game.units[10].health_now, expecthealth_now) # battle tank attack battle tank outside the range

        self.testOrders.clear()
        self.testOrders.append(self.orders[13])
        self.game.skill_phase(self.testOrders)
        expecthealth_now = 100 - calculateInjure(100, 10)
        self.assertEqual(self.game.units[15].health_now, expecthealth_now)   # battle tank attack meat

        self.game.units[10].health_now = 900  #reset the health
        self.game.units[15].health_now = 100

    def testNukeTankSkills(self):
        self.testOrders.clear()
        self.testOrders.append(self.orders[6])
        self.game.skill_phase(self.testOrders)
        expecthealth_now = 500 - calculateInjure(300, 100)
        self.assertEqual(self.game.units[8].health_now, expecthealth_now) #nuke tank attack bolt tank inside tha range
        self.game.units[1].position = (50, 50)
        self.game.skill_phase(self.testOrders)
        self.assertEqual(self.game.units[8].health_now, expecthealth_now) #nuke tank attack bolt tank outside the range

        self.game.units[8].health_now = 500  #reset the health

        self.testOrders.clear()
        self.game.units[16].position = (40, 40)
        self.game.units[10].position = (40, 39)
        self.game.units[8].position = (40, 38)
        self.testOrders.append(self.orders[7])
        self.game.skill_phase(self.testOrders)      # nuke tank release skill2
        expecthealth_now1 = 900 - calculateInjure(800, 200)
        #expecthealth_now2 = 500 - calculateInjure(800, 100)
        expecthealth_now2 = 0
        self.assertEqual(self.game.units[10], expecthealth_now1)
        self.assertEqual(self.game.units[8], expecthealth_now2)

        self.game.units[10].health_now = 900  #reset the health
        self.game.units[8].health_now = 500

    def testEagleSkill1(self):
        self.game.units[4].position = (55, 55)
        self.game.units[6].position = (55, 54.5)
        self.game.units[12].posotion = (55, 55.5)
        self.game.units[13].position = (54.5, 55)
        self.testOrders.clear()
        self.testOrders.append(self.orders[8])  # eagle release skill1
        self.game.skill_phase(self.testOrders)
        expecthealth_now1 = 500
        expecthealth_now2 = 300 - calculateInjure(200, 50)
        expecthealth_now3 = 500 - calculateInjure(200, 150)
        self.assertEqual(self.game.units[6].health_now, expecthealth_now1)
        self.assertEqual(self.game.units[12].health_now, expecthealth_now2)
        self.assertEqual(self.game.units[13].health_now, expecthealth_now3)

        self.game.units[6].health_now = 500  # reset the health
        self.game.units[12].health_now = 300
        self.game.units[13].health_now = 500

    def testEagleSkill2(self):
        self.game.units[20] = unit.UnitObject(20, 0, "eagle", (100, 100), self.game.buff)
        #self.game.units[21] = unit.UnitObject(  not completed!
        pass

    def testSupermanSkill1(self):
        self.game.units[25] = unit.UnitObject(25, 0, "superman", (100, 100), self.game.buff)
        self.game.units[26] = unit.UnitObject(26, 1, "bolt_tank", (101, 100), self.game.buff)
        order = ["superman_skill1", 25, 26]
        self.testOrders.clear()
        self.testOrders.append(order)
        ehn = 500 - calculateInjure(15, 100)
        self.assertEqual(self.game.units[26].health_now, ehn) #superman attack bolt tank through skill1

    def testSupermanSkills(self):
        pazh
