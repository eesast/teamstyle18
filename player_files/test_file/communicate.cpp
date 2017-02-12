#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include "communicate.h"
#include "head_for_main.h"				//为了改变flag,也为了知道游戏是否结束了
#include <queue>
#include <ctime> 
using namespace std;
extern int team_id;
extern bool flag_of_round;	
extern resourse allResourse;
extern double buff[40]; //buff全局变量 阵营1[单位类型][buff类型]
extern Unit all_unit[300];			  //所有的unit
extern int all_unit_size;				//记录所有unit的个数
extern int all_received = 0;
extern bool receiveable;
extern bool runAI;
extern queue <Instr>  q_instruction;

void recv_send_socket::create_recv_socket(void)  
{  
	//建立通信的端口的一些准备
    wVersionRequested = MAKEWORD( 1, 1 );//第一个参数为低位字节；第二个参数为高位字节  
  
    err = WSAStartup( wVersionRequested, &wsaData );//对winsock DLL（动态链接库文件）进行初始化，协商Winsock的版本支持，并分配必要的资源。  
    if ( err != 0 )  
    {  
        return;  
    }  
  
    if ( LOBYTE( wsaData.wVersion ) != 1 ||HIBYTE( wsaData.wVersion ) != 1 )//LOBYTE（）取得16进制数最低位；HIBYTE（）取得16进制数最高（最左边）那个字节的内容        
    {  
        WSACleanup( );  
        return;  
    }  
  
}  
void recv_send_socket::InitialSocketClient(void)				//与python端建立连接、开始游戏
{
	sockClient=socket(AF_INET,SOCK_STREAM,0);  
  
        SOCKADDR_IN addrClt;//需要包含服务端IP信息  
        addrClt.sin_addr.S_un.S_addr=inet_addr("127.0.0.1");// inet_addr将IP地址从点数格式转换成网络字节格式整型。		//为什么是这个地址？？//←mdzz
        addrClt.sin_family=AF_INET;   
        addrClt.sin_port=htons(18223);  
  
        cout<<connect(sockClient,(SOCKADDR*)&addrClt,sizeof(SOCKADDR));//客户机向服务器发出连接请求 

		recv(sockClient,(char*)&team_id,sizeof(int),0);
		cout << "i have receive the team_id: "<<team_id<<endl;

}
unsigned __stdcall recv_send_socket::static_recv_data(void * pThis)  
{  
	recv_send_socket * pthX = (recv_send_socket*)pThis;   // the tricky cast  
	cout << "Receiving";
	pthX->recv_data();           // now call the true entry-point-function 
	return 1;                           // the thread exit code  
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
void recv_send_socket::recv_data(void)
{
	//
	while (game_not_end())						//
	{
		while (!receiveable) { Sleep(1); }
		//我只将0、1、2接收3次
		int recvType=10;				//等下会接收三种类型的数据
		int data = 0;
		data = recv(sockClient,(char*)&recvType,sizeof(int),0);
		cout << "数据类型" << recvType;
		switch (recvType)
		{
		case 2:						//资源
			data = recv(sockClient,(char*)&allResourse,sizeof(resourse),0);
			//cout << "收资源";
			all_received++;
			break;
		case 1:						//四个兵种的buff
			data = recv(sockClient,(char*)&buff,2*3*5*sizeof(double),0);
			all_received++;
			//cout << "收buff";
			break;
		case 0:						//双方各自可以获得的地图上的unit的信息
			recv(sockClient,(char*)&all_unit_size,sizeof(int),0);
			for (int i=0;i<all_unit_size;i++)
				recv(sockClient,(char*)(all_unit+i),sizeof(Unit),0);
			//all_unit[0].Print();
			all_received++;
			//cout << "收单位";
			break;
		default:
			break;
		}
		cout << "当前:" << all_received << ",";
		if (all_received >= 3)
		{
			//flag_of_round = true;
			all_received = 0;
			runAI = true;
		}
	}
	
}
void recv_send_socket::send_data(void)
{
	cout << "发发发！"<<endl;
	Instr Isttemp(1, -1, -1);
	q_instruction.push(Isttemp);
	int sizeQueue=q_instruction.size();
	//cout << "instr num:" << sizeQueue << endl;
	if (sizeQueue != 0)
	{
		Instr * allInstr = new Instr[sizeQueue];			//为0是会有问题
		for (int i = 0; i < sizeQueue; i++)
		{
			allInstr[i] = q_instruction.front();
			q_instruction.pop();
		}
		send(sockClient, (char*)allInstr, sizeQueue * sizeof(Instr), 0);		//将指令全部发送过去
		delete[] allInstr;
	}
	receiveable = true;
}

void recv_send_socket::close_recv_socket(void)
{
	WSACleanup();  
}

