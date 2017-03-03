#include "communicate.h"
#include "head_for_main.h"

extern bool flag_of_round;	
extern bool flag_of_gameOver;
extern recv_send_socket  * p_sock_receive_send;
extern int all_received;
extern bool receiveable = true;
extern bool runAI = false;
extern int turn=0;
void player_main(void);	


void init_global_vars()	
{
	flag_of_round=false;	
	flag_of_gameOver=false;
}

void send_client_hello()
{
	p_sock_receive_send->InitialSocketClient();
	
}

bool game_not_end()	
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

unsigned int __stdcall start_player(void* arg)
{
	while (!flag_of_gameOver)
	{
		if (runAI)
		{
		cout<<"turns£º"<<turn<<endl;
		player_main();
		turn++;
		runAI = false;
		p_sock_receive_send->send_data();
		}	

	}
	return 0;
}


void wait_till_next_round()	
{
	while (true)
	{
		if (flag_of_round == true)	
			return;
		else if (all_received >= 3)
		{
			flag_of_round = true;
			return;
		}
		else 
		{
			Sleep(1000*time_round/1000);
		}

	}
}
