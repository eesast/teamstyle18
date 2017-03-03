
#pragma once
#include<string>
#include<iostream>
#include<vector>
#include <mutex>
#include <queue>
#include "communicate.h"
using namespace std;
using std::string;
using std::vector;
using std::mutex;

template <typename Data> 
class safeQueue
{
private:
	std::queue<Data> squeue ;  
	mutex mtx;
public:
	void safePush(Data value);
	void safePop(void);
	Data safeFront(void);
};

//����ö���ͱ���
//type_name
enum UnitType
{
	BASE,	     //������
	INFANTRY,	 //����
	VEHICLE,	 //̹��
	AIRCRAFT,	 //�ɻ�
	BUILDING   	 //����
};

enum BuffType
{
	ATTACK,		 //����buff
	DEFENSE,	 //����buff
	HEALTH,	     //�������ֵbuff
	SHOT_RANGE, 	 //���buff
	SPEED		 //�ٶ�buff
};

enum TypeName
{
	__BASE, 
	
	MEAT, HACKER, SUPERMAN,
	
	BATTLE_TANK, BOLT_TANK, NUKE_TANK, 
	
	UAV, EAGLE, 
	
	HACK_LAB, BID_LAB, CAR_LAB, ELEC_LAB, RADIATION_LAB, 
	UAV_LAB, AIRCRAFT_LAB, BUILD_LAB, FINANCE_LAB, MATERIAL_LAB,
	NANO_LAB, TEACH_BUILDING, BANK,
	Type_num
};


enum attribute
{
	UNIT_TYPE,
	ORIGIN_MAX_HEALTH,
	ORIGIN_MAX_SPEED,
	ORIGIN_SHOT_RANGE,
	ORIGIN_DEFENSE,
	ORIGIN_ATTACK,
	SKILL_CD_1,
	SKILL_CD_2,
	MAX_ACCOUNT,
	PEOPLE_COST,
	MONEY_COST,
	TECH_COST,
	attribute_num
};
//������unit��ʼ��
const int origin_attribute[Type_num][attribute_num] =
{

{BASE,      10000  ,  0,   10,  0,    10,  -1,   1,   0,     0,   0,     0      },
{INFANTRY,	100    ,  3,   1,   10,   0,   -1,  -1,   -1,    1,   100,   0	    },
{INFANTRY,	150    ,  3,   18,  20,   0,   1,   -1,   -1,    2,   600,   300	},
{INFANTRY,	500    ,  4,   10,  150,  15,  1,   50,   1,     10,  2000,  1500	},
{VEHICLE,	900    ,  7,   14,  200,  100, 10,  -1,   -1,    4,   1500,  600	},
{VEHICLE,	500    ,  6,   12,  100,  200, 10,  -1,   -1,    3,   1000,  500	},
{VEHICLE,	700    ,  5,   20,  150,  300, 10,  150,  1,     10,  4000,  2000	},
{AIRCRAFT,	300    ,  12,  10,  50,   5,   1,   -1,   -1,    2,   400,   100	},
{AIRCRAFT,	600    ,  15,  16,  200,  200, 20,  50,   1,     1,   3000,  1500	},
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    },
{BUILDING,	INT_MAX,  0,   0,   0,    0,   -1,  -1,   0,     0,   0,     0	    }

};

//��������ɽṹ��
//resourse
struct resourse
{
	int money_1;
	int remain_people_1;
	int tech_1;
	
	int money_2;
	int remain_people_2;
	int tech_2;
};
struct Position
{
	int x;
	int y;
	Position(int xx = -1, int yy = -1) :x(xx),y(yy){};
};
const Position none_position = Position(-1,-1);
struct BuildingHandle
{
	int id;
	int flag;
	TypeName type;
	Position pos;
	BuildingHandle(int xx = -1, int yy = -1,TypeName t= Type_num,int x=0,int y=0) :id(xx), flag(yy), type(t),pos(x,y){};
};



struct Unit
{
	TypeName type_name;
	UnitType unit_type;
	int attack_mode;			// ����ģʽ������ɶԿգ��ɶ�̹�ˣ��ɶԲ���֮���
	float attack_now;					// ��ǰ����
	float defense_now;				// ��ǰ����
	int disable_since ;			// ��̱����ʱ��㣬�����ж�̱��ʱ��
	int flag ;					// ������Ӫ
	int hacked_point;				// ���ڵĵ���
	int healing_rate ;		// ���� / ά������	
	float health_now;					// ��ǰ����ֵ		
	int is_disable;		// �Ƿ�̱��
	float max_health_now;				// ��ǰHP����
	float max_speed_now;				// ��ǰ����ٶ�
	Position position;				// ��λλ��
	float shot_range_now;				// ��ǰ���
	int skill_last_release_time1;// �ϴμ���1�ͷ�ʱ��
	int skill_last_release_time2;// �ϴμ���2�ͷ�ʱ��
	int unit_id;				// ��λid
	Unit();	
	Unit(int unit_id, int flag, TypeName type_name, Position pos);  
	void Print();
};

class Instr	
{
public:
	int instruction_type;				//1��ʾskil1,2��ʾskil2,3��ʾproduce,4��ʾMove,5��ʾcapture
	int the_unit_id;
	int target_id_building_id;
	Position pos1;					
	Position pos2;
	Instr(int instru_type=-1,int u_id=-1,int tar_build_id=-1,Position tpos1=none_position,Position tpos2=none_position);
};





//ѡ�ֵ��ú���������
void skill_1(int unit_id,int target_id=-1,Position tpos1=none_position,Position tpos2=none_position) ;
void skill_2(int unit_id,int target_id=-1,Position tpos1=none_position,Position tpos2=none_position) ;
void produce(int building_id);
void Move(int unit_id, Position pos);
void capture(int unit_id, int building_id);



Unit * getUnit(void);
int getUnitSize(void);
double * getBuff(void);
resourse getResourse(void);
bool getTeamId(void);
void NewData(void);
