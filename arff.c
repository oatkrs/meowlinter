#include <stdio.h>

#include <string.h>



void insecureFunction(char *input) {

    char buffer[10]; // CWE-121: Stack-based Buffer Overflow - insufficient buffer size



    strcpy(buffer, input); // CWE- strcpy() without length check, leading to buffer overflow

    printf("Input: %s\n", buffer);

}



int main() {

    char userInput[20];

    printf("Enter input: ");

    gets(userInput); // CWE-242: Use of Insecure Function 'gets()' - no bounds checking, can lead to buffer overflow



    insecureFunction(userInput);



    return 0;

}

