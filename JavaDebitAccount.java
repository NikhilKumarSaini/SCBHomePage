// DebitAccount with Overloaded Methods
class DebitAccount extends Account {
    String password;

    public DebitAccount(String accountNum, String accountOwner, double balance, String password) {
        super(accountNum, accountOwner, balance);
        this.password = password;
    }

    // Normal withdrawal without password
    @Override
    public void performPayment(double amount) {
        super.performPayment(amount);
    }

    // Overloaded withdrawal with password check
    public void performPayment(double amount, String pwd) {
        if (this.password.equals(pwd)) {
            super.performPayment(amount);
        } else {
            System.out.println("Incorrect password. Payment failed.");
        }
    }

    // Normal deposit without password
    @Override
    public void performDeposit(double amount) {
        super.performDeposit(amount);
    }

    // Overloaded deposit with password check
    public void performDeposit(double amount, String pwd) {
        if (this.password.equals(pwd)) {
            super.performDeposit(amount);
        } else {
            System.out.println("Incorrect password. Deposit failed.");
        }
    }
}