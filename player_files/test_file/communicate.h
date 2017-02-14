#pragma once
#include <stdio.h>  
#include <Winsock2.h>  
#pragma comment( lib, "ws2_32.lib" )  

#include "teamstyle18-my-1.h"
class recv_send_socket							//觉得只有这样才能够在main函数中实现
{
public:
	//recv_send_socket(bool team);				//false表示第一阵营，true表示第二阵营
	void create_recv_socket(void);
	void InitialSocketClient(void);
	static unsigned __stdcall static_recv_data(void * pThis);
	int __stdcall recv_data(void);
	void send_data(void);
	void close_recv_socket(void);
	
private:
	WORD wVersionRequested;  
    WSADATA wsaData;  
    int err;  
	SOCKET sockClient;					//请求端的socket
};

void wrapper_recv_data(SOCKET s,char* buf,int len,int flags);


//SkillInstr * p_all_1 = new SkillInstr[10000];
