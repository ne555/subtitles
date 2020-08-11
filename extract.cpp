#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>

/*
 * Trabaja con .srt
 * Extrae los diálogos
 * standard input/output
 */

namespace subtitle{
	struct tiempo{
		int hora, minuto, segundo, milesima;
		tiempo& operator+=(double offset){
			double total = hora*3600 + minuto*60 + segundo;
			total = total*1000+milesima;

			total += offset;
			total /= 1000;
			hora = total/3600;
			minuto = (total-hora*3600)/60;
			segundo = total-hora*3600-minuto*60;
			//milesima = total-hora*3600-minuto*60-segundo;
			milesima = (total - (int) total)*1000;
			return *this;
		}
	};

	std::istream& operator>>(std::istream &in, tiempo &t){
		char dummy;
		in >> t.hora >> dummy;
		in >> t.minuto >> dummy;
		in >> t.segundo >> dummy;
		in >> t.milesima;
		return in;
	}

	std::ostream& operator<<(std::ostream &out, const tiempo &t){
		out << t.hora << ':';
		out << t.minuto << ':';
		out << t.segundo << ',';
		out << t.milesima;
		return out;
	}

	struct srt{
		int id;
		tiempo inicio, fin;
		std::vector<std::string> dialog;
	};

	std::istream& operator>>(std::istream &in, srt &sub){
		std::string dummy;
		in >> sub.id;
		in >> sub.inicio >> dummy >> sub.fin;
		in.ignore();

		sub.dialog.clear();
		std::string line;
		while( std::getline(in, line) and not line.empty() )
			sub.dialog.push_back(line);

		return in;
	}

	std::ostream& operator<<(std::ostream &out, const srt &sub){
		out << sub.id << '\n';
		out << sub.inicio << " --> " << sub.fin << '\n';

		for( auto &x : sub.dialog )
			out << x << '\n';
		out << '\n';

		return out;
	}
}

int main(int argc, char **argv){
	subtitle::srt sub;
	while( std::cin >> sub ){
		//todo en una linea
		for( auto &x : sub.dialog )
			std::cout << x << '\n';
		std::cout << "\n";
	}

	return 0;
}
