//functions for "main"

#pragma once


void init_global_vars();	

void send_client_hello();
void recv_server_hello();
bool game_not_end();

unsigned int __stdcall start_player(void* arg);					//启动选手的线程

void wait_till_next_round();				//参数得用来标记是哪一个选手的flag 1表示选手，2表示选手2

//因为要使选手函数一回合至多只能被执行一次，得立一个标志记录新的一回合是否开始了（选手这回合函数是否被调用过）
//这里假设  回合是否开始，有逻辑端通知我，我就不管了。接到通知，flag=true;选手函数调用完后，flag=false;


const float time_round=0.1;		//我暂时假定每回合0.01s



//尝试用队列存储所有指令：
