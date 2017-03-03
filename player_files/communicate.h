#pragma once
#include <stdio.h>  
#include <Winsock2.h>  
#pragma comment( lib, "ws2_32.lib" )  

#include "teamstyle18-my-1.h"
class recv_send_socket
{
public:

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
	SOCKET sockClient;
};

void wrapper_recv_data(SOCKET s,char* buf,int len,int flags);
