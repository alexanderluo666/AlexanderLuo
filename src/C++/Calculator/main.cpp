#include <iostream>
using namespace std;

int main() {
    double a, b;
    char op;
    while (true) {
    cout << "Enter first number: ";
    cin >> a;

    cout << "Enter operator (+ - * /): ";
    cin >> op;

    cout << "Enter second number: ";
    cin >> b;

    double result;

    if (op == '+') {
    result = a + b;
    }
    else if (op == '-') {
        result = a - b;
    }
    else if (op == '*') {
        result = a * b;
    }
    else if (op == '/') {
        if (b == 0){
            cout << "Cannot be divided by zero\n";
        }
        result = a / b;
    }
    else {
        cout << "Invalid operator\n";
}

    cout << "Result: " << result << "\n";


    char again;
    cout << "Again? (y/n): ";
    cin >> again;

    if (again == 'n') break;
}
}