#include <iostream>
#include <stdio.h>
#include <process.h>   
#include "communicate.h"
#include "head_for_main.h"
#include "teamstyle18-my-1.h"

#include <windows.h> 
#define _WINSOCK_DEPRECATED_NO_WARNINGS 1
using namespace std;

int team_id = 0;
bool flag_info;
bool flag_of_round;	
bool flag_of_gameOver;
queue <Instr> q_instruction;
resourse allResourse;
//float buff[48] = { 0.0 }; 
//Unit all_unit[300];	
//int all_unit_size=0;
recv_send_socket  * p_sock_receive_send = new recv_send_socket;
int main()
{
	init_global_vars();
	p_sock_receive_send->create_recv_socket();
	send_client_hello();
	HANDLE   hth_receive_send,hth_player, except_handle;
    unsigned  ui_thread_recive_sendID,ui_thread_playerID, ui_thread_exceptID;
	hth_receive_send = (HANDLE)_beginthreadex( NULL,0,recv_send_socket::static_recv_data,p_sock_receive_send,CREATE_SUSPENDED,&ui_thread_recive_sendID );
	hth_player = (HANDLE)_beginthreadex( NULL,0,start_player,NULL,CREATE_SUSPENDED,&ui_thread_playerID );
	ResumeThread(hth_receive_send);	
	ResumeThread(hth_player);
	WaitForSingleObject(hth_receive_send,INFINITE);
	WaitForSingleObject(hth_player,INFINITE);
	CloseHandle(hth_receive_send);
	CloseHandle(hth_player);	
	p_sock_receive_send->close_recv_socket();
	system("pause");
	return 0;
}  