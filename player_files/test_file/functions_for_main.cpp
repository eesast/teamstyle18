#include "communicate.h"
#include "head_for_main.h"
//#define WIN32_LEAN_AND_MEAN   // Exclude rarely-used stuff from Windows headers
 
// #include <windows.h>
 
extern bool flag_of_round;	
extern bool flag_of_gameOver;
extern recv_send_socket  * p_sock_receive_send;
extern int all_received;
extern bool receiveable = true;
extern bool runAI = false;
extern int turn=0;
void player_main(void);				//选手的线程要调用     写在playerMain.cpp中


void init_global_vars()					//内容待定，等到接到信息时再转为true
{
	flag_of_round=false;	
	flag_of_gameOver=false;				//游戏结束时再置为true
}

void send_client_hello()				//告诉逻辑端， 选手这边准备好了
{
	p_sock_receive_send->InitialSocketClient();					//初始化socket，并向 逻辑端发出初始化的请求
	
}

bool game_not_end()						//得从逻辑端获取游戏是否结束的信息
{
	if (flag_of_gameOver==true)
		return false;
	else
#ifdef DEBUG
		return true;
#else 
		return true;
#endif
}

unsigned int __stdcall start_player(void* arg)					//启动选手1的线程
{
	while (!flag_of_gameOver)
	{
		if (runAI)
		{
		cout<<"turns："<<turn<<endl;
		player_main();
		turn++;
		runAI = false;
		p_sock_receive_send->send_data();
		}	

	}
	return 0;
}


void wait_till_next_round()					//之后加一段时间的间隔  避免空转
{
	while (true)
	{
		if (flag_of_round == true)					//可以进入下一次调用函数
			return;
		else if (all_received >= 3)
		{
			flag_of_round = true;
			return;
		}
		else 
		{
			Sleep(1000*time_round/1000);
		}//否则等待   直到逻辑端告诉我下一回合开始了
				//			//暂时休息1/100回合免得空转			//不知道对线程会不会有很大影响？
	}
}
