import java.util.*;

public class App {
    public static void main(String[] args) {
        ArrayList<Account> accounts = new ArrayList<>();

        // Adding different account types
        accounts.add(new Account("A1001", "Alice", 4000));
        accounts.add(new DebitAccount("D1002", "Bob", 6000, "bob123"));
        accounts.add(new CreditAccount("C1003", "Charlie", 3000, 5000));

        // Iterating using Polymorphism
        for (Account acc : accounts) {
            System.out.println("Account Owner: " + acc.accountOwner + ", Balance: " + acc.getBalance());
        }
    }
}