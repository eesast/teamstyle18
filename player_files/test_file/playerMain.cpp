//选手1写入ai
#include "teamstyle18-my-1.h"
#include <iostream>
void player_main(void)				//参数以及返回值待定       void需要被一个数组（队列）取代
{
	using namespace std;
	produce(0);
	//skill_1(007,110,Position(3,3),Position(4,4)) ;
	Unit * myunit=getUnit();
	int myUnitSize=getUnitSize();
	double * myBuff=getBuff();
	resourse myResourse_1=getResourse_1();
	resourse myResourse_2=getResourse_2();
	cout<<myUnitSize<<endl;
	for (int i=0;i<myUnitSize;i++)
	{
	//	cout<<myunit[i].attack_mode<<endl;
	//	cout<<myunit[i].flag<<endl;
	}
	//cout<<endl;
	cout<<myResourse_1.money<<'\t'<<myResourse_1.remain_people<<'\t'<<myResourse_1.tech<<endl;
	//cout<<myResourse_2.money<<'\t'<<myResourse_2.remain_people<<'\t'<<myResourse_2.tech<<endl;
}


/*
void skill_1(int unit_id,int target_id=-1,Position tpos1=none_position,Position tpos2=none_position) ;
void skill_2(int unit_id,int target_id=-1,Position tpos1=none_position,Position tpos2=none_position) ;
void produce(int building_id);
void Move(int unit_id, Position pos);
void capture(int unit_id, int building_id);



Unit * getUnit(void);
int getUnitSize(void);
double * getBuff(void);
resourse getResourse_1(void);
resourse getResourse_2(void);
*/
