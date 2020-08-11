#include <iostream>
#include <string>
#include <algorithm>

std::string dot2coma(std::string s){
	std::replace(s.begin(), s.end(), '.', ',');
	return s;
}

int main(){
	//ignore until the start of the dialogue
	std::string line;
	while(std::getline(std::cin, line) and line not_eq "[Events]")
		;

	//Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
	std::getline(std::cin, line);
	for(int count=1; std::getline(std::cin, line); ++count){
		if(line.empty()) continue;

		int marked = line.find(',',line.find(':'))+1;
		std::string start, end, text;
		start = line.substr(marked, line.find(',', marked)-marked );
		marked = line.find(',', marked)+1;
		end = line.substr(marked, line.find(',', marked)-marked );
		int n=7;
		for(int K=0; K<n; ++K)
			marked = line.find(',', marked)+1;
		text = line.substr(marked);

		start = dot2coma(start);
		end = dot2coma(end);

		//saltos de línea
		for(int pos=0; (pos=text.find("\\N",pos)) not_eq std::string::npos; )
			text.replace(pos,2,1,'\n');

		//efectos
		std::string italica = "{\\ I1} ";
		if(text.find(italica) not_eq std::string::npos){
			text.replace(0,italica.size(), "<i>");
			text += "</i>";
		}
		

		std::cout << count << '\n';
		std::cout << start << " --> " << end << '\n';
		std::cout << text << "\n\n";
	}
	

}
