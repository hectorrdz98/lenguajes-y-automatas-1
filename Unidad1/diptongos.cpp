#include <iostream>
#include <fstream>
#include <string.h>

using namespace std;

int main() {
    ifstream file;
    char line[200];
    file.open("parrafo.txt");
	if (file.is_open()) {
		while(file.getline(line, 200)) {
            char *word = strtok(line," \t");
            while (word != NULL) {
                for (char letra : word) {
                    cout << letra << endl;
                }
                word = strtok(NULL, " \t");
            }
		}
		file.close();
	}
    return 0;
}