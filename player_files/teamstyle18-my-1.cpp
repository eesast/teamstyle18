
#include "teamstyle18-my-1.h"

#include <queue>
using namespace std;
extern queue <Instr>  q_instruction;
extern resourse allResourse;
extern float buff[48] = { 0.0 }; //buff全局变量 阵营1[单位类型][buff类型]
extern Unit all_unit[500];			  //所有的unit
extern int all_unit_size;				//记录所有unit的个数
extern int team_id;
//构造函数
Unit::Unit(){};
Unit::Unit(int _unit_id, int _flag, TypeName _type_name, Position pos)
{

	unit_id = _unit_id;
	flag = _flag;
	position = pos;
	type_name = _type_name;
	unit_type = UnitType(origin_attribute[type_name][UNIT_TYPE]);
	health_now = origin_attribute[type_name][ORIGIN_MAX_HEALTH] * (1 + buff[24*flag+6*unit_type+HEALTH]);	//从“double”转换到“int”，可能丢失数据	  //单位生成时默认为最大血量，以下同理
	max_health_now = origin_attribute[type_name][ORIGIN_MAX_HEALTH] * (1 + buff[24*flag+6*unit_type+HEALTH]);
	max_speed_now = origin_attribute[type_name][ORIGIN_MAX_SPEED] * (1 + buff[24*flag+6*unit_type+SPEED]);
	shot_range_now = origin_attribute[type_name][ORIGIN_SHOT_RANGE] * (1 + buff[24*flag+6*unit_type+SHOT_RANGE]);
	defense_now = origin_attribute[type_name][ORIGIN_DEFENSE] * (1 + buff[24*flag+6*unit_type+DEFENSE]);
	attack_now = origin_attribute[type_name][ORIGIN_ATTACK] * (1 + buff[24*flag+6*unit_type+ATTACK]);

}
void Unit::Print()
{

}
Instr::Instr(int instru_type,int u_id,int tar_build_id,Position tpos1,Position tpos2):instruction_type(instru_type),the_unit_id(u_id),target_id_building_id(tar_build_id),pos1(tpos1),pos2(tpos2){};


//1表示skkil1,2表示skkil2,3表示produce,4表示Move,5表示capture
void skill_1(int unit_id,int target_id,Position tpos1,Position tpos2) 
{
	Instr Isttemp(1,unit_id,target_id,tpos1,tpos2);
	q_instruction.push(Isttemp);
}
void skill_2(int unit_id,int target_id,Position tpos1,Position tpos2) 
{
	Instr Isttemp(2,unit_id,target_id,tpos1,tpos2);
	q_instruction.push(Isttemp);
}
void produce(int building_id)
{
	Instr Isttemp(3,-1,building_id);
	q_instruction.push(Isttemp);
}
void Move(int unit_id, Position pos)
{
	Instr Isttemp(4,unit_id,-1,pos);
	q_instruction.push(Isttemp);
}
void capture(int unit_id, int building_id)
{
	Instr Isttemp(5,unit_id,building_id);
	q_instruction.push(Isttemp);
}
Unit * getUnit(void)
{
	return all_unit;
}
int getUnitSize(void)
{
	return all_unit_size;
}
float * getBuff(void)
{
	return buff;
}
resourse getResourse(void)
{
	return allResourse;
}
bool getTeamId(void)
{
	return team_id;
}
void NewData(void)
{
	;
}
