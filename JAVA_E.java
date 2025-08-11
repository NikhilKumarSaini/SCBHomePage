Q7
import java.util.ArrayList;

public class AppArrayList {
    public static void main(String[] args) {
        ArrayList<Account> accounts = new ArrayList<>();

        accounts.add(new Account("A100", "John", 1000));
        accounts.add(new CreditAccount("C100", "Alice", 2000, 0, 500));
        accounts.add(new DebitAccount("D100", "Bob", 1500, "pass123"));

        for (Account acc : accounts) {
            System.out.println("Account Number: " + acc.accountNum + ", Owner: " + acc.accountOwner + ", Balance: " + acc.getBalance());
        }
    }
}