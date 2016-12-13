//问题：怎么控制多个线程？

//#include "pthread.h"
//#define DEBUG

#include <iostream>
#include <stdio.h>					//为了开启多线程 而 include 一些头文件
#include <process.h>   


 
#include "communicate.h"
#include "head_for_main.h"				//main函数 需要调用的一些函数
#include "teamstyle18-my-1.h"

#include <windows.h> 
#define _WINSOCK_DEPRECATED_NO_WARNINGS 1
using namespace std;
//这个地方应该怎么分配双方的信息？
bool team_id = false; //队伍id    //也可能是true 要跟杨应人商量
//用来标识那块地址给选手用，那块地址存入新的数据
bool flag_info;						//false 时选手取用第一块地址，新的数据放入第二块地址，true时反之
//标志游戏回合、总的是否结束的量
bool flag_of_round;	
bool flag_of_gameOver;


//传指令的量
queue <Instr> q_instruction;

//收数据的量
resourse allResourse;
//二维数组不好返回，用以为数组
double buff[40] = { 0.0 }; //buff全局变量 前20个 阵营1[单位类型][buff类型] 后20个 阵营2[单位类型][buff类型]  2*5*5?

Unit * all_unit= new Unit[1];	 //变成 所有的unit (信息对双方都是透明的)
int all_unit_size=0;	
/*
Unit * all_unit_1= new Unit[1];			  //可以知道的所有的阵营1的unit      //变成 所有的unit (信息对双方都是透明的)
int all_unit_size_1=0;				//记录阵营1所有unit的个数
Unit * all_unit_2= new Unit[1];			  //可以知道的所有的阵营2的unit 
int all_unit_size_2=0;				//记录阵营2所有unit的个数
*/
//其实应该可以不定义为全局变量
recv_send_socket  * p_sock_receive_send = new recv_send_socket;			//通信的socket

int main()
{
	
	init_global_vars();		//定义所有需要定义的全局变量
	//建两个socket
	
	p_sock_receive_send->create_recv_socket();
	send_client_hello();	//告诉逻辑端两个选手已经启动了游戏						//这个地方地址要和杨应人协商！
	//recv_server_hello();	//获取逻辑端用python通过socket发来的所有数据（建筑、金钱、单位等）

	//开启六个线程//不对是2个，调用选手ai的线程里实现发送指令
	HANDLE   hth_receive_send,hth_player;				
    unsigned  ui_thread_recive_sendID,ui_thread_playerID;	
	//线程1，用来接收数据
	hth_receive_send = (HANDLE)_beginthreadex( NULL,0,recv_send_socket::static_recv_data,p_sock_receive_send,CREATE_SUSPENDED,&ui_thread_recive_sendID );			//这个地方可能写的有点问题，我应该把这个线程一直开着就够了
	//和杨应人商量，发数据之前，一定需要把 是哪一方的数据告诉我        （选手、对手的信息怎么区分？需要有一个对偶的量？）
	//线程2，用来 控制调用选手1的ai 的线程
	hth_player = (HANDLE)_beginthreadex( NULL,0,start_player,NULL,CREATE_SUSPENDED,&ui_thread_playerID );
	
     
	//开启三个线程
	//多加一个   hth_receive1   hth_receive2	
	ResumeThread(hth_receive_send);					//就把它打开来一直用来接收
	ResumeThread(hth_player);						//这样实现太复杂了，肯定还是要改的
	
	WaitForSingleObject(hth_receive_send,INFINITE);
	WaitForSingleObject(hth_player,INFINITE);
	
	CloseHandle(hth_receive_send);
	CloseHandle(hth_player);
	
	p_sock_receive_send->close_recv_socket();
	
	//这里逻辑变得好复杂啊						//这个逻辑变到了 在选手的线程里分别实现
	/*while(game_not_end())		//只要游戏没有结束
	{
		player_main();			//不断执行选手的playermain函数
		wait_till_next_round();		//等执行完playermain之后的下一回合、再进入while循环
	}*/
	delete [] all_unit;
	/*
	delete [] all_unit_1;					//释放空间
	delete [] all_unit_2;	
	*/
	cout<<"1"<<endl;
	return 0;
}  