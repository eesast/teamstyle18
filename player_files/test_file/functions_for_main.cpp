#include "communicate.h"
#include "head_for_main.h"
//#define WIN32_LEAN_AND_MEAN   // Exclude rarely-used stuff from Windows headers
 
// #include <windows.h>
 
extern bool flag_of_round;	
extern bool flag_of_gameOver;
extern recv_send_socket  * p_sock_receive_send;
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
//暂时约定不收hello直接开始吧
/*void recv_server_hello()				//从逻辑端接收一些可能初始必要的数据（这个函数可能是不需要的）				
{
	;									//接收信息
	flag1_of_round=true;
	flag2_of_round=true;				//回合开始？？？？
}*/
//待完善
//其实完全没有必要用这个函数，可以考虑删去
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
	while (game_not_end())
	{
		player_main();
		flag_of_round=false;									//等到下一回合flag再释放
		wait_till_next_round();								//等到下一回合时，flag会变为true
		//告诉杨应人我会把队伍编号先发送
		p_sock_receive_send->send_data();						//将所有的指令发送出去
																//这句话应该摆在哪里好？？？  在这里肯定是不对的是不是要再开一个线程？
		//Sleep(5);
	}
	
	return 0;
}


void wait_till_next_round()					//之后加一段时间的间隔  避免空转
{
	while (true)
	{
		if (flag_of_round==true)					//可以进入下一次调用函数
			return;
		else                                        //否则等待   直到逻辑端告诉我下一回合开始了
			Sleep(1000*time_round/1000);	//			//暂时休息1/100回合免得空转			//不知道对线程会不会有很大影响？
	}
}
