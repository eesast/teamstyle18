#pragma once
#include "teamstyle18.h"

vector<Unit>units;      // 单位List
int turn_num = 0;   //回合数
extern double buff[2][4][5] = { 0.0 }; //buff全局变量 [阵营][单位类型][buff类型]


Unit::Unit(int _unit_id, int _flag, TypeName _type_name, Position pos)
{

	unit_id = _unit_id;
    flag = _flag;
	position = pos;
	type_name = _type_name;
	unit_type = UnitType(origin_attribute[type_name][UNIT_TYPE]);
	health_now = origin_attribute[type_name][ORIGIN_MAX_HEALTH] * (1 + buff[flag][unit_type][HEALTH]);		  //单位生成时默认为最大血量，以下同理
	max_health_now = origin_attribute[type_name][ORIGIN_MAX_HEALTH] * (1 + buff[flag][unit_type][HEALTH]);
	max_speed_now = origin_attribute[type_name][ORIGIN_MAX_SPEED] * (1 + buff[flag][unit_type][SPEED]);
	shot_range_now = origin_attribute[type_name][ORIGIN_SHOT_RANGE] * (1 + buff[flag][unit_type][SHOT_RANGE]);
	defense_now = origin_attribute[type_name][ORIGIN_DEFENSE] * (1 + buff[flag][unit_type][DEFENSE]);
	attack_now = origin_attribute[type_name][ORIGIN_ATTACK] * (1 + buff[flag][unit_type][ATTACK]);

}

void Move(int unit_id, Position pos);
void skill_1(int unit_id, ...);//参数并没有想好怎么写
void skill_2(int unit_id, ...);

int main()//这是用来测试的
{
	Unit tank(1, 1, NUKE_TANK, { 22,33 });
	std::cout<<tank;
	units.push_back(tank);
}