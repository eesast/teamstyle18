#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include "communicate.h"
#include "head_for_main.h"
#include <queue>
#include <ctime> 
using namespace std;
extern int team_id;
extern bool flag_of_round;	
extern resourse allResourse;
extern recv_send_socket  * p_sock_receive_send;
extern float buff[48]; 
extern Unit all_unit[500] = {};
extern int all_unit_size = 0;
extern int all_received = 0;
extern bool receiveable;
extern bool runAI;
extern bool flag_of_gameOver;
extern bool recv_except = false;
extern queue <Instr>  q_instruction;
int changed_building_num = 0;
int other_unit_num = 0;
BuildingHandle changed_building[200];

void recv_send_socket::create_recv_socket(void)  
{  
    wVersionRequested = MAKEWORD( 1, 1 );
    err = WSAStartup( wVersionRequested, &wsaData );
    if ( err != 0 )  
    {  
        return;  
    }  
  
    if ( LOBYTE( wsaData.wVersion ) != 1 ||HIBYTE( wsaData.wVersion ) != 1 )
    {  
        WSACleanup( );  
        return;  
    }  
  
}  
void recv_send_socket::InitialSocketClient(void)	
{
	sockClient=socket(AF_INET,SOCK_STREAM,0);  
	int nRecvBuf = 32 * 1024;
	setsockopt(sockClient, SOL_SOCKET, SO_RCVBUF, (const char*)&nRecvBuf, sizeof(int));
        SOCKADDR_IN addrClt;
        addrClt.sin_addr.S_un.S_addr=inet_addr("127.0.0.1");
        addrClt.sin_family=AF_INET;   
        addrClt.sin_port=htons(18223);  
  
        cout<<connect(sockClient,(SOCKADDR*)&addrClt,sizeof(SOCKADDR));

		recv(sockClient,(char*)&team_id,sizeof(int),0);
		cout << "i have receive the team_id: "<<team_id<<endl;

}
unsigned __stdcall recv_send_socket::static_recv_data(void * pThis)  
{  
	recv_send_socket * pthX = (recv_send_socket*)pThis; 
	cout << "Receiving";
	pthX->recv_data();
	return 1; 
}  
void wrapper_recv_data(SOCKET s,char* buf,int len,int flags)
{
	int remain = len;
	while (remain!=0)
	{
		int cur=recv(s,buf,len,flags);
		if (cur==-1)
		{
			cout<<"receive error"<<endl;
			continue;
		}
		buf+=cur;
		remain-=cur;
	}
	
}

int recv_send_socket::recv_data(void)
{
	bool first_round = true;
	while (!flag_of_gameOver)
	{
		
		int recvType=10;
		int data = 0;
		data = recv(sockClient,(char*)&recvType,sizeof(int),0);
		Sleep(1);
		switch (recvType)
		{
		case 302:						
			cout << "game is tie!!" << endl;
			runAI = false;
			flag_of_gameOver = true;
			break;
		case 301:
			cout << "winner is AI1!!" << endl;
			runAI = false;
			flag_of_gameOver = true;
			break;
		case 300:
			cout << "winner is AI0!!" << endl;
			runAI = false;
			flag_of_gameOver = true;
			break;
		case 2:
			data = recv(sockClient,(char*)&allResourse,sizeof(resourse),0);
			all_received++;
			break;
		case 1:	
			data = recv(sockClient,(char*)&buff,2*4*6*sizeof(float),0);
		        all_received++;
			break;
		case 0:	
			if (first_round)
			{
				recv(sockClient, (char*)&all_unit_size, sizeof(int), 0);
				recv(sockClient, (char*)&all_unit_size, sizeof(int), 0);
				for (int i = 0; i<all_unit_size; i++)
					recv(sockClient, (char*)(all_unit + i), sizeof(Unit), 0);
			}
			else 
			{
				recv(sockClient, (char*)&other_unit_num, sizeof(int), 0);
				recv(sockClient, (char*)&all_unit_size, sizeof(int), 0);
				for (int i = 0; i<other_unit_num; i++)
					recv(sockClient, (char*)(all_unit + i), sizeof(Unit), 0);
			}
			all_received++;
			break;
		case 450:
			recv(sockClient, (char*)&changed_building_num, sizeof(int), 0);
			for (int i = 0; i<changed_building_num; i++)
				recv(sockClient, (char*)(changed_building + i), sizeof(BuildingHandle), 0);
			all_received++;
			break;
		default:
			int k;
			recv(sockClient, (char*)(&k), sizeof(int), 0);
			cout << k;
			break;
		}
		if ((first_round&&all_received >= 3)|| (!first_round&&all_received >= 4))
		{
			if (!first_round)
			{
				for (int i = 0; i < changed_building_num; i++)
				{
					all_unit[other_unit_num + i] = Unit(changed_building[i].id, changed_building[i].flag, changed_building[i].type, changed_building[i].pos);
				}
			}
			first_round = false;
			all_received = 0;
			runAI = true;
		}
	}
	return 0;
}
void recv_send_socket::send_data(void)
{

	Instr Isttemp(1, -1, -1);
	q_instruction.push(Isttemp);
	int sizeQueue=q_instruction.size();
	if (sizeQueue != 0)
	{
		Instr * allInstr = new Instr[sizeQueue];
		for (int i = 0; i < sizeQueue; i++)
		{
			allInstr[i] = q_instruction.front();
			q_instruction.pop();
		}
		send(sockClient, (char*)allInstr, sizeQueue * sizeof(Instr), 0);
		delete[] allInstr;

	}

}

void recv_send_socket::close_recv_socket(void)
{
	WSACleanup();  
}

