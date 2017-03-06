#pragma once


void init_global_vars();	

void send_client_hello();
void recv_server_hello();
bool game_not_end();

unsigned int __stdcall start_player(void* arg);	
void wait_till_next_round();
const float time_round=0.1;