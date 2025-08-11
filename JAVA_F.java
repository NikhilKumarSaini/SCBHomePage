Q9 
import java.util.Scanner;

public class AppMenu {
    private static Scanner scanner = new Scanner(System.in);
    private static ArrayList<Account> accounts = new ArrayList<>();

    public static void main(String[] args) {
        // Sample accounts for testing
        accounts.add(new Account("A100", "John", 1000));
        accounts.add(new CreditAccount("C100", "Alice", 2000, 0, 500));
        accounts.add(new DebitAccount("D100", "Bob", 1500, "pass123"));

        boolean exit = false;

        while (!exit) {
            displayMenu();
            int choice = scanner.nextInt();
            scanner.nextLine();  // consume newline

            switch (choice) {
                case 1:
                    createAccount();
                    break;
                case 2:
                    performPayment();
                    break;
                case 3:
                    performDeposit();
                    break;
                case 4:
                    displayAllAccounts();
                    break;
                case 5:
                    exit = true;
                    System.out.println("Exiting system.");
                    break;
                default:
                    System.out.println("Invalid choice. Try again.");
            }
        }
    }

    private static void displayMenu() {
        System.out.println("\nBank Account Management System Menu");
        System.out.println("1. Create New Account");
        System.out.println("2. Perform Payment (Withdraw)");
        System.out.println("3. Perform Deposit");
        System.out.println("4. Display All Accounts");
        System.out.println("5. Exit");
        System.out.print("Enter your choice: ");
    }

    private static void createAccount() {
        System.out.print("Enter Account Number: ");
        String accNum = scanner.nextLine();

        System.out.print("Enter Account Owner Name: ");
        String owner = scanner.nextLine();

        System.out.print("Enter Initial Balance: ");
        double balance = scanner.nextDouble();
        scanner.nextLine();

        System.out.print("Account Type (1 = General, 2 = Credit, 3 = Debit): ");
        int type = scanner.nextInt();
        scanner.nextLine();

        switch (type) {
            case 1:
                accounts.add(new Account(accNum, owner, balance));
                break;
            case 2:
                System.out.print("Enter Credit Limit: ");
                double limit = scanner.nextDouble();
                scanner.nextLine();
                accounts.add(new CreditAccount(accNum, owner, balance, 0, limit));
                break;
            case 3:
                System.out.print("Set password for Debit Account: ");
                String password = scanner.nextLine();
                accounts.add(new DebitAccount(accNum, owner, balance, password));
                break;
            default:
                System.out.println("Invalid account type. Account not created.");
                return;
        }
        System.out.println("Account created successfully!");
    }

    private static Account findAccountByNumber(String accNum) {
        for (Account acc : accounts) {
            if (acc.accountNum.equals(accNum)) {
                return acc;
            }
        }
        return null;
    }

    private static void performPayment() {
        System.out.print("Enter Account Number for Payment: ");
        String accNum = scanner.nextLine();

        Account acc = findAccountByNumber(accNum);
        if (acc == null) {
            System.out.println("Account not found.");
            return;
        }

        System.out.print("Enter amount to withdraw: ");
        double amount = scanner.nextDouble();
        scanner.nextLine();

        if (acc instanceof DebitAccount) {
            System.out.print("Enter password: ");
            String password = scanner.nextLine();
            ((DebitAccount) acc).performPayment(amount, password);
        } else {
            acc.performPayment(amount);
        }
    }

    private static void performDeposit() {
        System.out.print("Enter Account Number for Deposit: ");
        String accNum = scanner.nextLine();

        Account acc = findAccountByNumber(accNum);
        if (acc == null) {
            System.out.println("Account not found.");
            return;
        }

        System.out.print("Enter amount to deposit: ");
        double amount = scanner.nextDouble();
        scanner.nextLine();

        if (acc instanceof DebitAccount) {
            System.out.print("Enter password: ");
            String password = scanner.nextLine();
            ((DebitAccount) acc).performDeposit(amount, password);
        } else {
            acc.performDeposit(amount);
        }
    }

    private static void displayAllAccounts() {
        System.out.println("\nAll Accounts:");
        for (Account acc : accounts) {
            System.out.println("Account Number: " + acc.accountNum + ", Owner: " + acc.accountOwner + ", Balance: " + acc.getBalance());
            if (acc instanceof CreditAccount) {
                System.out.println("Bonus Points: " + ((CreditAccount) acc).bonusPoint + ", Credit Limit: " + ((CreditAccount) acc).limit);
            }
        }
    }
}