Q3 
public class DebitAccount extends Account {
    String password;

    public DebitAccount(String accountNum, String accountOwner, double balance, String password) {
        super(accountNum, accountOwner, balance);
        this.password = password;
    }

    // Overload performPayment with password checking
    public void performPayment(double amount, String inputPassword) {
        if (this.password.equals(inputPassword)) {
            super.performPayment(amount);
        } else {
            System.out.println("Password incorrect. Payment failed.");
        }
    }

    // Overload performDeposit with password checking
    public void performDeposit(double amount, String inputPassword) {
        if (this.password.equals(inputPassword)) {
            super.performDeposit(amount);
        } else {
            System.out.println("Password incorrect. Deposit failed.");
        }
    }
}

public class CreditAccount extends Account {
    int bonusPoint;
    double limit;

    public CreditAccount(String accountNum, String accountOwner, double balance, int bonusPoint, double limit) {
        super(accountNum, accountOwner, balance);
        this.bonusPoint = bonusPoint;
        this.limit = limit;
    }

    // Override performPayment with limit checking and bonusPoint update
    @Override
    public void performPayment(double amount) {
        if (amount > 0 && amount <= balance + limit) {
            balance -= amount;
            bonusPoint += (int)(amount * 0.01);  // 1% bonus points
            System.out.println(amount + " withdrawn successfully with bonus points added.");
        } else {
            System.out.println("Exceeded credit limit or invalid amount.");
        }
    }

    // Override performDeposit with bonusPoint update
    @Override
    public void performDeposit(double amount) {
        if (amount > 0) {
            balance += amount;
            bonusPoint += (int)(amount * 0.005);  // 0.5% bonus points
            System.out.println(amount + " deposited successfully with bonus points added.");
        } else {
            System.out.println("Invalid deposit amount.");
        }
    }
}