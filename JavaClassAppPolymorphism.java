public class App {
    public static void main(String[] args) {
        // Polymorphism: Account reference to CreditAccount
        Account acc1 = new CreditAccount("C1001", "David", 2000, 3000);
        acc1.performPayment(1500);
        acc1.performDeposit(1000);
        System.out.println("Balance of David: " + acc1.getBalance());

        // Polymorphism: Account reference to DebitAccount
        Account acc2 = new DebitAccount("D1001", "Eva", 5000, "eva123");
        acc2.performDeposit(2000);
        acc2.performPayment(2500);
        System.out.println("Balance of Eva: " + acc2.getBalance());
    }
}