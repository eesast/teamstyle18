
#include "teamstyle18-my-1.h"

#include <queue>
using namespace std;
extern queue <Instr>  q_instruction;
extern resourse allResourse;
extern double buff[40]; //buffȫ�ֱ��� ��Ӫ1[��λ����][buff����]
extern Unit all_unit[300];			  //���е�unit
extern int all_unit_size;				//��¼����unit�ĸ���
extern int team_id;
template <typename Data> 
void safeQueue<Data>::safePush(Data value)
{
	mtx.lock();
	squeue.push();
	mtx.unlock();
}
template <typename Data> 
void safeQueue<Data>::safePop(void)
{
	;
}
template <typename Data> 
Data safeQueue<Data>::safeFront(void)
{
	;
}

//���캯��
Unit::Unit(){};
Unit::Unit(int _unit_id, int _flag, TypeName _type_name, Position pos)
{

	unit_id = _unit_id;
	flag = _flag;
	position = pos;
	type_name = _type_name;
	unit_type = UnitType(origin_attribute[type_name][UNIT_TYPE]);
	health_now = origin_attribute[type_name][ORIGIN_MAX_HEALTH] * (1 + buff[20*flag+5*unit_type+HEALTH]);	//�ӡ�double��ת������int�������ܶ�ʧ����	  //��λ����ʱĬ��Ϊ���Ѫ��������ͬ��
	max_health_now = origin_attribute[type_name][ORIGIN_MAX_HEALTH] * (1 + buff[20*flag+5*unit_type+HEALTH]);
	max_speed_now = origin_attribute[type_name][ORIGIN_MAX_SPEED] * (1 + buff[20*flag+5*unit_type+SPEED]);
	shot_range_now = origin_attribute[type_name][ORIGIN_SHOT_RANGE] * (1 + buff[20*flag+5*unit_type+SHOT_RANGE]);
	defense_now = origin_attribute[type_name][ORIGIN_DEFENSE] * (1 + buff[20*flag+5*unit_type+DEFENSE]);
	attack_now = origin_attribute[type_name][ORIGIN_ATTACK] * (1 + buff[20*flag+5*unit_type+ATTACK]);

}
void Unit::Print()
{

}
Instr::Instr(int instru_type,int u_id,int tar_build_id,Position tpos1,Position tpos2):instruction_type(instru_type),the_unit_id(u_id),target_id_building_id(tar_build_id),pos1(tpos1),pos2(tpos2){};


//1��ʾskkil1,2��ʾskkil2,3��ʾproduce,4��ʾMove,5��ʾcapture
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
double * getBuff(void)
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