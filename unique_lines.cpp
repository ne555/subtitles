#include <iostream>
#include <fstream>
#include "subtitle.h"
/* 
 * Trabaja con .srt
 * Une los tiempos de las líneas si estas son iguales
 * y los tiempos se solapan
 */

bool continuation(const subtitle::srt &prev, const subtitle::srt &next){
	return
		prev.dialog == next.dialog
		and prev.fin == next.inicio;
}

subtitle::srt& merge(subtitle::srt &prev, const subtitle::srt &next){
	prev.fin = next.fin;
	return prev;
}

int main(int argc, char **argv){
	std::string filename;
	if(argc==1) filename = "/dev/stdin";
	else filename = argv[1];

	std::ifstream input(filename);
	subtitle::srt dialog, previous;
	int count = 0;
	input>>dialog;
	previous=dialog;
	while(input>>dialog){
		if(continuation(previous, dialog))
			previous = merge(previous, dialog);
		else{ //cambio
			++count;
			previous.id = count;
			std::cout << previous << '\n';
			previous = dialog;
		}
	}

	previous.id = count;
	std::cout << previous << '\n';
	return 0;
}

