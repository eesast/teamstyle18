//选手1写入ai

#include "teamstyle18-my-1.h"
#include<vector>
#include<queue>
#include<cmath>
#include<algorithm>
#include<ctime>
const int mapsize = 100;
using namespace std;

Unit mybase;
Unit enemybase;
int stage = 0;
vector<Position>obstacle;
int Distance(Position a, Position b)
{
	return abs(a.x - b.x) + abs(a.y - b.y);
}
struct cap_pair {
	Unit src;
	Unit target;
};
vector<Unit>cap_target;
bool init1 = true;
bool find_obstacle(Position src)
{
	for (int i = 0; i < obstacle.size(); i++)
	{
		if (obstacle[i].x == src.x&&obstacle[i].y == src.y)
		{
			return true;
		}
	}
	return false;
}
Position nextPace(Position src, Position target, int speed)
{
	if (Distance(src, target) <= speed)
	{
		return target;
	}
	else {
		int xxx = target.x - src.x >= 0 ? 1 : -1;
		int yyy = target.y - src.y >= 0 ? 1 : -1;
		for (int i = min(abs(target.x - src.x), speed); i>=0; i--)
		{
			for (int j = min((abs(target.y - src.y)), speed - i); j >= 0; j--)
			{
				Position temp(src.x + xxx*i, src.y + yyy*j);
				if (!find_obstacle(temp))
				{
					return temp;
				}
				else{}
			}
		}
		return Position(src.x + xxx*speed/2, src.y + yyy*speed / 2);
	}
	
	
}


extern int turn ;
void player_main(void)
{
	
	Unit * myunit = getUnit();
	int myUnitSize = getUnitSize();
	srand(int(time(0)));
	int meat_num = 0;
	//printf("回合数：%d",turn);
	double * myBuff = getBuff();
	resourse myResourse = getResourse();
	int myflag = getTeamId();
	int enemyflag = !myflag;
	//printf("unit num:%d\n", myUnitSize);
	//cout << "unit num:" << myUnitSize<<endl ;
	vector<Unit>my_units[22];
	vector<Unit>enemy_units[22];
	vector<Unit>netural_units[22];
	vector<Unit>meats;	

		//cout << "money1:" << myResourse.money_1 << "tech1:" << myResourse.tech_1 << "people1:" << myResourse.remain_people_1<<endl;
		
		for (int i = 0; i < myUnitSize; i++)
		{
			if (myunit[i].type_name== __BASE|| (myunit[i].type_name>=9&& myunit[i].type_name<=21))
			{
				obstacle.push_back(myunit[i].position);
			}
			if (myunit[i].type_name == MEAT)
			{
				//cout << "meat: id:" << myunit[i].unit_id << " my flag:" << myunit[i].flag << "position:(" << myunit[i].position.x << " " << myunit[i].position.y << ")" << endl;

			}
			if (myunit[i].flag == myflag)
			{
				//cout << i<<"th unit  id is mine: "<< myunit[i] .unit_id<<"type:" << myunit[i].type_name << " my flag:" << myunit[i].flag<<"position:(" << myunit[i].position.x<<" "<< myunit[i].position.y<<")"<<endl;
				my_units[int(myunit[i].type_name)].push_back(myunit[i]);
			}
			else
			{
				if (myunit[i].flag == enemyflag)
				{
					//cout << i << "th unit id is enemy: " << myunit[i].unit_id << "type:" << myunit[i].type_name << " enemy:" << myunit[i].flag << "position:(" << myunit[i].position.x << " " << myunit[i].position.y << ")" << endl;
					enemy_units[myunit[i].type_name].push_back(myunit[i]);
				}
				else
				{
					//cout << i << "th unit   id: " << myunit[i].unit_id << "type:" << myunit[i].type_name << " netural flag:" << myunit[i].flag << "position:(" << myunit[i].position.x << " " << myunit[i].position.y << ")" << endl;
					netural_units[myunit[i].type_name].push_back(myunit[i]);
				}
			}
		}



		mybase = my_units[__BASE][0];
		enemybase = enemy_units[__BASE][0];
		meat_num = my_units[MEAT].size();
		//cout << "enemybase HP:" << enemybase.health_now <<"("<< enemybase.position.x<<","<< enemybase.position.y<<")"<< endl;
		//cout << "meat_num:"<< my_units[MEAT].size() << endl;
		for (int i = 0; i < Type_num; i++)
		{
			//cout << "&" << i << ":" << my_units[i].size() << " ";
		}
		for (int i = 0; i < my_units[MEAT].size(); i++)
		{
			meats.push_back(my_units[MEAT][i]);
		}		
		if (stage == 0 && meat_num<=3)
		{
			produce(mybase.unit_id);
		}	

		if (init1)
		{
			cap_target.push_back(netural_units[BANK][0]);
			cap_target.push_back(netural_units[BANK][1]);
			cap_target.push_back(netural_units[TEACH_BUILDING][0]);
			int target1 = rand() % 7 + 9;
			int target2 = rand() % 7 + 9;
			cap_target.push_back(netural_units[target1][0]);
			cap_target.push_back(netural_units[target2][0]);
			init1 = false;
		}
		
		//cout << "目标：";
		//for (int i = 0; i < cap_target.size(); i++)
		//{
		//	cout << "(" << cap_target[i].position.x << "," << cap_target[i].position.y << ")";
		//}
		for (int i = 0; i < min(meats.size(), cap_target.size()); i++)
		{
			if (Distance(meats[i].position, cap_target[i].position) >= 2)
			{
				//cout << "break!!!" << endl;
				//Move(meats[i].unit_id, { meats[i].position.x + 1,meats[i].position.y + 1 });
				//cout << "*";
				Move(meats[i].unit_id, nextPace(meats[i].position,
				Position(cap_target[i].position.x - 1,  cap_target[i].position.y), meats[i].max_speed_now));
			}
			if (Distance(meats[i].position, cap_target[i].position) == 1)
			{
				capture(meats[i].unit_id, cap_target[i].unit_id);

				std::vector<Unit>::iterator it = cap_target.begin() + i;
				cap_target.erase(it);
			}
		}




		for (int i = HACK_LAB; i <= AIRCRAFT_LAB; i++)
		{
			if (my_units[i].size() != 0)
			{
				for (int j = 0; j < my_units[i].size(); j++)
				{
					if (myResourse.remain_people_1 >= origin_attribute[i - 7][PEOPLE_COST])
					{
						produce(my_units[i][j].unit_id);
					}
				}

			}
		}
		for (int i = HACKER; i <= EAGLE; i++)
		{
			if (my_units[i].size() != 0)
			{
				for (int j = 0; j < my_units[i].size(); j++)
				{
					if (Distance(my_units[i][j].position, enemybase.position) > origin_attribute[i][ORIGIN_SHOT_RANGE])
					{
						//cout << "move!";
						Move(my_units[i][j].unit_id, nextPace(my_units[i][j].position, Position(enemybase.position.x - 1,  enemybase.position.y), my_units[i][j].max_speed_now));
					}
					else
					{
						//cout << "attack!";
						if (my_units[i][j].type_name == EAGLE)
						{
							skill_1(my_units[i][j].unit_id, -1, enemybase.position);
						}
						else
						{
							skill_1(my_units[i][j].unit_id, enemybase.unit_id, enemybase.position, enemybase.position);
						}
					}
				}
			}

		}

		if (cap_target.size() < meat_num)
		{
			vector <int>notempty;
			for (int k = HACK_LAB; k < Type_num; k++)
			{
				if (!netural_units[k].empty())
				{
					notempty.push_back(k);
				}
			}
			int z = rand() % (notempty.size());
			for (int m = 0; m < netural_units[z].size(); m++)
			{
				bool find = false;
				for (int j = 0; j < cap_target.size(); j++)
				{
					if (netural_units[z][m].unit_id == cap_target[j].unit_id)
					{
						find = true;
						break;
					}
				}
				if (!find)
				{
					cap_target.push_back(netural_units[z][m]);
				}
			}
	}
		//cout << endl;
		//<<"*************************" << endl;
		
}


