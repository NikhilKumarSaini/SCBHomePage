// Base Account class
class Account {
    String accountNum;
    String accountOwner;
    double balance;

    // Parameterized Constructor
    public Account(String accountNum, String accountOwner, double balance) {
        this.accountNum = accountNum;
        this.accountOwner = accountOwner;
        this.balance = balance;
    }

    // Method to withdraw money
    public void performPayment(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            System.out.println("Payment of " + amount + " successful. Remaining balance: " + balance);
        } else {
            System.out.println("Payment failed. Insufficient funds or invalid amount.");
        }
    }

    // Method to deposit money
    public void performDeposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposit of " + amount + " successful. New balance: " + balance);
        } else {
            System.out.println("Deposit failed. Invalid amount.");
        }
    }

    // Getter for balance
    public double getBalance() {
        return balance;
    }
}

// DebitAccount class extending Account
class DebitAccount extends Account {
    String password;

    public DebitAccount(String accountNum, String accountOwner, double balance, String password) {
        super(accountNum, accountOwner, balance);
        this.password = password;
    }
}

// CreditAccount class extending Account
class CreditAccount extends Account {
    int bonusPoint;
    double limit;

    public CreditAccount(String accountNum, String accountOwner, double balance, double limit) {
        super(accountNum, accountOwner, balance);
        this.limit = limit;
        this.bonusPoint = 0;
    }

    // Override performPayment to check credit limit
    @Override
    public void performPayment(double amount) {
        if (amount > 0 && (balance - amount) >= -limit) {
            balance -= amount;
            bonusPoint += (int)(amount / 100); // earn 1 point for every 100 spent
            System.out.println("Payment of " + amount + " successful (Credit). New balance: " + balance);
            System.out.println("Bonus Points: " + bonusPoint);
        } else {
            System.out.println("Payment failed. Credit limit exceeded or invalid amount.");
        }
    }

    // Override performDeposit to add bonus points
    @Override
    public void performDeposit(double amount) {
        if (amount > 0) {
            balance += amount;
            bonusPoint += (int)(amount / 200); // earn 1 point for every 200 deposited
            System.out.println("Deposit of " + amount + " successful (Credit). New balance: " + balance);
            System.out.println("Bonus Points: " + bonusPoint);
        } else {
            System.out.println("Deposit failed. Invalid amount.");
        }
    }
}

// App class to test everything
public class App {
    public static void main(String[] args) {
        // 2. Create Account object and test deposit & withdraw
        Account acc1 = new Account("A1001", "Alice", 5000);
        acc1.performDeposit(2000);
        acc1.performPayment(1500);
        System.out.println("Final Balance (Alice): " + acc1.getBalance());

        System.out.println("--------------------------------------------------");

        // 3. Create DebitAccount
        DebitAccount debitAcc = new DebitAccount("D2001", "Bob", 8000, "bob123");
        debitAcc.performDeposit(1000);
        debitAcc.performPayment(2500);
        System.out.println("Final Balance (Bob): " + debitAcc.getBalance());

        System.out.println("--------------------------------------------------");

        // 4. Create CreditAccount and test overridden methods
        CreditAccount creditAcc = new CreditAccount("C3001", "Charlie", 3000, 5000);
        creditAcc.performPayment(4000); // uses credit limit
        creditAcc.performDeposit(2000);
        creditAcc.performPayment(2500);
        System.out.println("Final Balance (Charlie): " + creditAcc.getBalance());
        System.out.println("Bonus Points (Charlie): " + creditAcc.bonusPoint);
    }
}