#include <iostream>
#include <fstream>
#include "subtitle.h"

int main(int argc, char **argv){
	if(argc not_eq 3) return 1;
	std::ifstream 
		a( argv[1] ),
		b( argv[2] );

	subtitle::srt sub;
	while( a >> sub )
		std::cout << sub << '\n';

	int count = sub.id;
	while( b >> sub ){
		++count;
		sub.id = count;
		std::cout << sub << '\n';
	}
	return 0;
}
