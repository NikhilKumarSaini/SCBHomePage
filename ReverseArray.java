import java.util.Scanner;

public class ReverseArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of elements: ");
        int size = sc.nextInt();

        int[] numbers = new int[size];

        System.out.println("Enter " + size + " numbers:");
        for (int i = 0; i < size; i++) {
            numbers[i] = sc.nextInt();
        }

        System.out.print("Original Array: ");
        for (int i = 0; i < size; i++) {
            System.out.print(numbers[i] + " ");
        }

        System.out.print("\nReverse Order: ");
        for (int i = size - 1; i >= 0; i--) {
            System.out.print(numbers[i] + " ");
        }

        sc.close();
    }
}