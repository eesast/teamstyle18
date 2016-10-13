#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from src import unit
from src import gamemain

def receive_orders(order):
    for k in range(len(order)):
        if(order[k][0]=='bolt_tank_skill1'):
            bolt_tank_skill1(order[k][1],order[k][2])
        elif(order[k][0]=='hacker_skill1'):
            hacker_skill1(order[k][1],order[k][2])
        elif(order[k][0]=='uav'):
            uav(order[k][1],order[k][2])
        elif(order[k][0]=='battle_tank_skill1'):
            battle_tank_skill1(order[k][1],order[k][2])
        elif(order[k][0]=='nuke_tank_skill1'):
            nuke_tank_skill1(order[k][1],order[k][2])
        elif(order[k][0]=='nuke_tank_skill2'):
            nuke_tank_skill2(order[k][1],order[k][2])
        elif(order[k][0]=='eagle_skill1'):
            eagle_skill1(order[k][1],order[k][2])
        elif(order[k][0]=='eagle_skill2'):
            eagle_skill1(order[k][1],order[k][2])
        elif(order[k][0]=='superman_skill1'):
            superman_skill1(order[k][1],order[k][2])
        elif(order[k][0]=='superman_skill2'):
            superman_skill2(order[k][1])

def Get_id_information(id):
    for k in A.units:
        if (k == id):
            return A.units[k]

def Get_distance(my_position, enemy_position):
    x = my_position[0] - enemy_position[0]
    y = my_position[1] - enemy_position[1]
    return (x * x + y * y) ** 0.5

# 电子对抗坦克技能1
def bolt_tank_skill1(id, attack_id):
    my_information = Get_id_information(id)
    enemy_information = Get_id_information(attack_id)
    skill_cd = A.turn_num - my_information.skill_last_release_time1 
    distance = Get_distance(my_information.position, enemy_information.position)
    if (skill_cd >= origin_attribute['bolt_tank']['skill_cd_1'] and distance <= origin_attribute['blot_tank']['origin_shot_range']):
        if (my_information.flag != enemy_information.flag) and (enemy_information.Get_unit_type() == 3):
            enemy_information.reset_attribute(health=enemy_information.health_now - 200)
            my_information.reset_attribute(skill_last_release_time1=A.turn_num)
        elif (my_information.flag != enemy_information.flag) and (enemy_information.Get_unit_type() == 2):
            enemy_information.reset_attribute(is_disable=True)
            my_information.reset_attribute(skill_last_release_time1=A.turn_num)


# 黑客技能1
def hacker_skill1(id, attack_id):
    my_information = Get_id_information(id)
    enemy_information = Get_id_information(attack_id)
    skill_cd = A.turn_num - my_information.skill_last_release_time1 
    distance = Get_distance(my_information.position, enemy_information.position)
    if (skill_cd >= origin_attribute['hacker']['skill_cd_1'] and distance <= origin_attribute['hacker']['origin_shot_range']):
        if (my_information.flag != enemy_information.flag) and (
                enemy_information.Get_unit_type() == 3 or enemy_information.Get_unit_type() == 2):
            enemy_information.reset_attribute(hacked_point=enemy_information.hacked_point + 1)
            my_information.reset_attribute(skill_last_release_time1=A.turn_num)
        elif (my_information.flag == enemy_information.flag) and (
                enemy_information.Get_unit_type() == 3 or enemy_information.Get_unit_type() == 2):
            enemy_information.reset_attribute(hacked_point=enemy_information.hacked_point - 1)
            my_information.reset_attribute(skill_last_release_time1=A.turn_num)


# 无人战机技能1
def uav(id, attack_id):
    my_information = Get_id_information(id)
    enemy_information = Get_id_information(attack_id)
    skill_cd = A.turn_num - my_information.skill_last_release_time1 
    distance = Get_distance(my_information.position, enemy_information.position)
    if (skill_cd >= origin_attribute['uav']['skill_cd_1'] and distance <= origin_attribute['uav']['origin_shot_range'] and (my_information.flag != enemy_information.flag)):
        enemy_information.reset_attribute(health=enemy_information.health_now - 5)
        my_information.reset_attribute(skill_last_release_time1=A.turn_num)


# 主站坦克技能1
def battle_tank_skill1(id, attack_id):
    my_information = Get_id_information(id)
    enemy_information = Get_id_information(attack_id)
    skill_cd = A.turn_num - my_information.skill_last_release_time1
    distance = Get_distance(my_information.position, enemy_information.position)
    if (skill_cd >= origin_attribute['battle_tank']['skill_cd_1'] and distance <= origin_attribute['battle_tank']['origin_shot_range'] and (my_information.flag != enemy_information.flag)):
        enemy_information.reset_attribute(health=enemy_information.health_now - 100)
        my_information.reset_attribute(skill_last_release_time1=A.turn_num)


# 核子坦克技能1
def nuke_tank_skill1(id, attack_id):
    my_information = Get_id_information(id)
    enemy_information = Get_id_information(attack_id)
    skill_cd = A.turn_num - my_information.skill_last_release_time1 
    distance = Get_distance(my_information.position, enemy_information.position)
    if (skill_cd >= origin_attribute['nuke_tank']['skill_cd_1'] and distance <= origin_attribute['nuke_tank']['origin_shot_range'] and (my_information.flag != enemy_information.flag)):
        if (enemy_information.Get_unit_type() == 3 or enemy_information.Get_unit_type() == 2):
            enemy_information.reset_attribute(health=enemy_information.health_now - 300)
            my_information.reset_attribute(skill_last_release_time1=A.turn_num)


# 核子坦克技能2
def nuke_tank_skill2(id,attack_range):
    my_information = Get_id_information(id)
    skill_cd = A.turn_num - my_information.skill_last_release_time2 
    distance = Get_distance(my_information.position, attack_range)
    if (skill_cd >= origin_attribute['nuke_tank']['skill_cd_2'] and distance <= origin_attribute['nuke_tank']['origin_shot_range']):
        for k in A.units:
            enemy_position = A.units[k].position
            if (Get_distance(enemy_position,attack_range) < 2):
                A.units[k].reset_attribute(health=A.units[k].health_now - 800)
        my_information.reset_attribute(skill_last_release_time2=A.turn_num)


# 鹰式战斗机技能1
def eagle_skill1(id,attack_range):
    my_information = Get_id_information(id)
    skill_cd = A.turn_num - my_information.skill_last_release_time1 
    distance = Get_distance(my_information.position, attack_range)
    if (skill_cd >= origin_attribute['eagle']['skill_cd_1'] and distance <= origin_attribute['eagle']['origin_shot_range']):
        for k in A.units:
            enemy_position = A.units[k].position
            if (enemy_position==attack_range):
                A.units[k].reset_attribute(health=A.units[k].health_now - 200)
        my_information.reset_attribute(skill_last_release_time1=A.turn_num)

# 鹰式战斗机技能2
def eagle_skill2(id,attack_range1,attack_range2):
    my_information = Get_id_information(id)
    skill_cd = A.turn_num - my_information.skill_last_release_time2 
    distance1 = Get_distance(my_information.position, attack_range1)
    distance2 = Get_distance(my_information.position, attack_range2)
    if (skill_cd >= origin_attribute['eagle']['skill_cd_2'] and distance1 <= origin_attribute['eagle']['origin_shot_range'] and distance2 <= origin_attribute['eagle']['origin_shot_range']):
        for k in A.units:
            enemy_position = A.units[k].position
            if (enemy_position==attack_range1 or enemy_position==attack_range2):
                A.units[k].reset_attribute(health=A.units[k].health_now - 400)
        my_information.reset_attribute(speed=my_information.max_speed_now+5)
        my_information.reset_attribute(skill_last_release_time2=A.turn_num)

#改造人战士技能1
def superman_skill1(id, attack_id):
    my_information = Get_id_information(id)
    enemy_information = Get_id_information(attack_id)
    skill_cd = A.turn_num - my_information.skill_last_release_time1 
    distance = Get_distance(my_information.position, enemy_information.position)
    if (skill_cd >= origin_attribute['superman']['skill_cd_1'] and distance <= origin_attribute['superman']['origin_shot_range'] and (my_information.flag != enemy_information.flag)):
        if(my_information.motor_type == 0) and (enemy_information.Get_unit_type() == 1 or enemy_information.Get_unit_type() == 2):
            enemy_information.reset_attribute(health=enemy_information.health_now - 15)
            my_information.reset_attribute(skill_last_release_time1=A.turn_num)
        elif(my_information.motor_type == 1):
            enemy_information.reset_attribute(health=enemy_information.health_now - 15)
            my_information.reset_attribute(skill_last_release_time1=A.turn_num)

#改造人战士技能2
def superman_skill2(id):
    my_information = Get_id_information(id)
    skill_cd = A.turn_num - my_information.skill_last_release_time1 
    if (skill_cd >= origin_attribute['superman']['skill_cd_2']):
        my_information.reset_attribute(motor_type=1,speed=12,health=my_information.health.now*1.02)
        my_information.reset_attribute(skill_last_release_time1=A.turn_num)

tank = UnitObject(1, 1, 'nuke_tank', (22, 33))
fuck = UnitObject(2, 0, 'battle_tank', (22, 32))
A=GameMain()
A.units[1]=tank
A.units[2]=fuck
A.units[1].print_info()
A.units[2].print_info()
order=[['nuke_tank_skill2',1,(22,31)]]

receive_orders(order)
A.units[1].print_info()
A.units[2].print_info()