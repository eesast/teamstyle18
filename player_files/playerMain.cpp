//选手1写入ai

#include "teamstyle18-my-1.h"
#include<vector>
#include<queue>
#include<cmath>
#include<algorithm>
#include<ctime>
const int mapsize = 100;
using namespace std;


int stage = 0;
vector<Position>obstacle;
vector<int>used_meats;
int Distance(Position a, Position b)
{
	return abs(a.x - b.x) + abs(a.y - b.y);
}
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
	/*cout<<src.x<<" "<<src.y<<endl;
	cout<<target.x<<" "<<target.y<<endl;
	cout<<speed<<endl;*/
	if (Distance(src, target) <= speed)
	{
		return target;
	}
	else 
	{
		int xxx = target.x - src.x;
		int yyy = target.y - src.y;
		int flag1=1,flag2=1;
		if(xxx<0)
			flag1=-1;
		if(yyy<0)
			flag2=-1;
		if(xxx!=0)
		{
			if(abs(xxx)<speed)
				return Position(src.x+xxx,src.y+(speed-abs(xxx))*flag2);
			else
				return Position(src.x+flag1*speed,src.y);
		}
		else if(yyy!=0)
		{
			if(abs(yyy)<speed)
				return Position(src.x,src.y+yyy);
			else
				return Position(src.x,src.y+flag2*speed);
		}
	}
}

bool find_meats(int meats_id)
{
	bool flag=1;
	for(int i=0;i<used_meats.size();i++)
	{
		if(meats_id==used_meats[i])
		{
			flag=0;break;
		}
	}
	return flag;
}

extern int turn ;
void player_main(void)
{
	Position next_position;
	vector<Unit>bank;//中立的银行
	vector<Unit>teach;//中立的教学楼
	vector<Unit>my_units[22];//非建筑单位
	vector<Unit>enemy_units[22];//敌人单位
	vector<Unit>netural_units[22];//中立建筑
	vector<Unit>meats;	//我的小鲜肉
	Unit mybase;
	Unit enemybase;
	Unit * all_unit = getUnit();
	resourse myResourse = getResourse();
	int all_UnitSize = getUnitSize();
	int meat_num = 0;
	//double * myBuff = getBuff();
	int myflag = getTeamId();
	int enemyflag = !myflag;

	for (int i = 0; i < all_UnitSize; i++)
	{
		if (all_unit[i].type_name== __BASE|| (all_unit[i].type_name>=9&& all_unit[i].type_name<=21))
		{
			obstacle.push_back(all_unit[i].position);
		}
			if (all_unit[i].type_name == MEAT)
			{
				meats.push_back(all_unit[i]);
				meat_num++;
			}
			if (all_unit[i].flag == myflag&&all_unit[i].type_name==__BASE)
			{
				mybase=all_unit[i];
			}
			if (all_unit[i].flag == enemyflag&&all_unit[i].type_name==__BASE)
			{
				enemybase=all_unit[i];
			}
			if (all_unit[i].flag == -1 && all_unit[i].type_name==BANK)
			{
				bank.push_back(all_unit[i]);
			}
			if (all_unit[i].flag == -1 && all_unit[i].type_name==TEACH_BUILDING)
			{
				teach.push_back(all_unit[i]);
			}
			if (all_unit[i].flag==myflag)
			{
				my_units[all_unit[i].type_name].push_back(all_unit[i]);
			}
			else
			{
				if (all_unit[i].flag == enemyflag)
				{

					enemy_units[all_unit[i].type_name].push_back(all_unit[i]);
				}
				else
				{
					netural_units[all_unit[i].type_name].push_back(all_unit[i]);
				}
			}
		}

	for(int i=0;i<enemy_units[UAV].size();i++)
	{
		if(Distance(enemy_units[UAV][i].position,mybase.position)<=12)
		{
			skill_1(mybase.unit_id,-1,enemy_units[UAV][i].position);
			cout<<"attack"<<endl;
			cout<<enemy_units[UAV][i].health_now<<endl;
		}
	}
}


