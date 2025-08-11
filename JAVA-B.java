Q2 
public class App {
    public static void main(String[] args) {
        Account account = new Account("ACC123", "John Doe", 1000.0);

        account.performPayment(200.0);
        account.performDeposit(500.0);

        System.out.println("Balance after transactions: " + account.getBalance());
    }
}