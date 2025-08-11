6q 
public class AppPolymorphism {
    public static void main(String[] args) {
        Account creditAcc = new CreditAccount("C123", "Alice", 2000, 0, 500);
        Account debitAcc = new DebitAccount("D123", "Bob", 1500, "pass123");

        // Using polymorphism to invoke overridden methods
        creditAcc.performPayment(300);
        creditAcc.performDeposit(700);

        // Need cast for overloaded methods with password for DebitAccount
        if (debitAcc instanceof DebitAccount) {
            DebitAccount dAcc = (DebitAccount) debitAcc;
            dAcc.performPayment(400, "pass123");
            dAcc.performDeposit(600, "pass123");
        }

        System.out.println("Credit Account Balance: " + creditAcc.getBalance());
        System.out.println("Debit Account Balance: " + debitAcc.getBalance());
    }
}