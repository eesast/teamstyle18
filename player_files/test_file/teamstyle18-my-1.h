
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

//若干枚举型变量
//type_name
enum UnitType
{
	AIRCRAFT,	 //飞机
	BASE,	     //主基地
	BUILDING,   	 //建筑
	INFANTRY,	 //步兵
	VEHICLE	 //坦克
};

enum BuffType
{
	ATTACK,		 //攻击buff
	DEFENSE,	 //防御buff
	HEALTH,	     //最大生命值buff
	SHOT_RANGE, 	 //射程buff
	SPEED		 //速度buff
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
//用来给unit初始化
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

//定义的若干结构体
//resourse
struct resourse
{
	//int round;
	int tech_1;
	int money_1;
	int remain_people_1;
	int tech_2;
	int money_2;
	int remain_people_2;
};
struct Position
{
	int x;
	int y;
	Position(int xx = -1, int yy = -1) :x(xx),y(yy){};
};
const Position none_position = Position(-1,-1);



//按我的顺序改一下
//按字母顺序排序

struct Unit
{
	TypeName type_name;
	UnitType unit_type;
	int attack_mode;			// 攻击模式，例如可对空，可对坦克，可对步兵之类的
	float attack_now;					// 当前攻击
	float defense_now;				// 当前防御
	int disable_since ;			// 被瘫痪的时间点，用于判断瘫痪时间
	int flag ;					// 所属阵营
	int hacked_point;				// 被黑的点数
	int healing_rate ;		// 治疗 / 维修速率	
	float health_now;					// 当前生命值		
	int is_disable;		// 是否被瘫痪
	float max_health_now;				// 当前HP上限
	float max_speed_now;				// 当前最大速度
	Position position;				// 单位位置，目测是一个point之类的东西
	float shot_range_now;				// 当前射程(现阶段貌似没有提升射程的技能，不过先保留)
	int skill_last_release_time1;// 上次技能1释放时间
	int skill_last_release_time2;// 上次技能2释放时间
	int unit_id;				// 单位id
	Unit();						//new 时需要空的构造函数
	Unit(int unit_id, int flag, TypeName type_name, Position pos);    //(这是用来干什么的，有些完全不需要的信息怎么处理，没辙了？得用一个for循环，把接到的数据在再进去，不能直接用它？)
	void Print();
};


//默认参数这怎么回事？
class Instr							//把几种指令的数据都放到这个里面
{
public:
	int instruction_type;				//1表示skil1,2表示skil2,3表示produce,4表示Move,5表示capture
	int the_unit_id;
	int target_id_building_id;
	Position pos1;					//为什么要加struct?
	Position pos2;
	Instr(int instru_type=-1,int u_id=-1,int tar_build_id=-1,Position tpos1=none_position,Position tpos2=none_position);
};





//选手调用函数的声明
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
