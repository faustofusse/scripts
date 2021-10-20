#include <stdio.h>
#include <string.h>

char* CONTROL_CHARACTERS[33] = { "NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI", "DLE", "DC1", "DC2", "DC3", "DC4", "NAK", "SYN", "ETB", "CAN", "EM", "SUB", "ESC", "FS", "GS", "RS", "US", "DEL" }; 

void print_table();
void print_info(char* value);

int main(int argc, char** argv) {
	if (argc <= 1) print_table();
	else print_info(argv[1]);
	return 0;
}

void print_table() {
	int printable = 32;
	int extended = 128;
	for (int c = 0; c <= 32; c++) {
		printf("%.2d %.2o 0x%.2X  %s\t\t%d %.3o 0x%.2X  %c\t\t%d %o 0x%.2X  %c\t\t%.3d %o 0x%.2X  %c\n", 
			c, c, c, CONTROL_CHARACTERS[c], 
			printable, printable, printable, printable, 
			printable + 32, printable + 32, printable + 32, printable + 32, 
			printable + 64, printable + 64, printable + 64, printable + 64
		);
		printable++;
	}
}

void print_info(char* value) {
	char caracter = strlen(value) == 3 ? value[1] : value[0];
	printf("Decimal: %.2d - Octal: %.2o - Hexa: 0x%.2X\n", caracter, caracter, caracter);
}
