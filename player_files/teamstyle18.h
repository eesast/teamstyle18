#pragma once
#include<string>
#include<iostream>
#include<vector>
using std::string;
using std::vector;
extern int team_id = -1; //队伍id

//type_name
enum UnitType
{
	BASE,	     //主基地
	INFANTRY,		 //步兵
	VEHICLE,		 //坦克
	AIRCRAFT,		 //飞机
	BUILDING   	 //建筑
};
enum BuffType
{
	HEALTH,	            //最大生命值buff
	ATTACK,		            //攻击buff
	SPEED,		            //速度buff
	DEFENSE,		        //防御buff
	SHOT_RANGE 		//射程buff
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


struct Position
{
	int x;
	int y;
};

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


class Unit
{
public:
	int unit_id = 0;				// 单位id
	string name = "";				// 单位名字，给选手赛艇一番
	Position position;				// 单位位置，目测是一个point之类的东西
	int flag = -1;					// 所属阵营	
	int motor_type;					// 移动方式，分地面和空中，精英步兵的技能会用到

	UnitType unit_type;
	TypeName type_name;

	int max_health_now;				// 当前HP上限
	int health_now;					// 当前生命值
	int max_speed_now;				// 当前最大速度
	int shot_range_now;				// 当前射程(现阶段貌似没有提升射程的技能，不过先保留)
	int defense_now;				// 当前防御
	int attack_now;					// 当前攻击
	double healing_rate = 0;		// 治疗 / 维修速率
	int hacked_point;				// 被黑的点数
	bool is_disable = false;		// 是否被瘫痪
	int disable_since;				// 被瘫痪的时间点，用于判断瘫痪时间
	int skill_last_release_time1;	// 上次技能1释放时间
	int skill_last_release_time2;	// 上次技能2释放时间
	int attack_mode;				// 攻击模式，例如可对空，可对坦克，可对步兵之类的

	Unit(int unit_id, int flag, TypeName type_name, Position pos);
};


std::ostream& operator <<(std::ostream &os, const Unit&u)//这也是用来测试的
{

	os << "id:" << u.unit_id << "阵营:" << u.flag << "位置:" << " (" << u.position.x << "," << u.position.y << ") " << "类型:" << u.unit_type << "兵种:" << u.type_name << "自定名称:" << u.name <<
		"HP:" << u.health_now << "MAXHP:" << u.max_health_now << "速度:" << u.max_speed_now << "射程:" << u.shot_range_now << "防御:" << u.defense_now << "攻击:" << u.attack_now <<
		"最大数量:" << origin_attribute[u.type_name][MAX_ACCOUNT] <<
		"人口:" << origin_attribute[u.type_name][PEOPLE_COST] <<
		"金钱消耗:" << origin_attribute[u.type_name][MONEY_COST] <<
		"科技消耗:" << origin_attribute[u.type_name][TECH_COST] <<
		std::endl;
	return os;
}
