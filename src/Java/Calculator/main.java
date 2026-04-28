import java.util.Scanner;

public class main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        double a, b;
        char op;

        System.out.print("Enter first number: ");
        a = sc.nextDouble();

        System.out.print("Enter operator: ");
        op = sc.next().charAt(0);

        System.out.print("Enter second number: ");
        b = sc.nextDouble();

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
            if (b == 0) {
                System.out.println("Cannot divide by zero");
                return;
            }
            result = a / b;
        }
        else {
            System.out.println("Invalid operator");
            return; // 🔥 THIS FIXES IT
        }

        System.out.println("Result: " + result);
    }
}