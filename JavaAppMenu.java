import java.util.*;

public class AppMenu {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<Account> accounts = new ArrayList<>();

        while (true) {
            System.out.println("\nWelcome to Bank System");
            System.out.println("1. Add New Account");
            System.out.println("2. Perform Deposit");
            System.out.println("3. Perform Withdrawal");
            System.out.println("4. Show All Accounts");
            System.out.println("5. Exit");
            System.out.print("Enter choice: ");
            int choice = sc.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter Account Number: ");
                    String num = sc.next();
                    System.out.print("Enter Owner Name: ");
                    String owner = sc.next();
                    System.out.print("Enter Initial Balance: ");
                    double bal = sc.nextDouble();
                    accounts.add(new Account(num, owner, bal));
                    System.out.println("Account Created Successfully!");
                    break;

                case 2:
                    System.out.print("Enter Account Number: ");
                    num = sc.next();
                    System.out.print("Enter Deposit Amount: ");
                    double dep = sc.nextDouble();
                    for (Account a : accounts) {
                        if (a.accountNum.equals(num)) {
                            a.performDeposit(dep);
                        }
                    }
                    break;

                case 3:
                    System.out.print("Enter Account Number: ");
                    num = sc.next();
                    System.out.print("Enter Withdrawal Amount: ");
                    double wd = sc.nextDouble();
                    for (Account a : accounts) {
                        if (a.accountNum.equals(num)) {
                            a.performPayment(wd);
                        }
                    }
                    break;

                case 4:
                    System.out.println("All Accounts:");
                    for (Account a : accounts) {
                        System.out.println(a.accountNum + " | " + a.accountOwner + " | " + a.getBalance());
                    }
                    break;

                case 5:
                    System.out.println("Thank you for using Bank System!");
                    return;

                default:
                    System.out.println("Invalid Choice!");
            }
        }
    }
}