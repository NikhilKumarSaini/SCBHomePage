package com.training.day3;

import java.util.*;

public class BankCustomerManagementSystem {
    private List<Customer> customers = new ArrayList<>();
    private Random rand = new Random();

    public void showMenu() {
        Scanner sc = new Scanner(System.in);
        int choice;
        do {
            System.out.println("Welcome to Standard Chartered Bank");
            System.out.println("Please enter your choice");
            System.out.println("1 for Add new Customer");
            System.out.println("2 for Display Customers");
            System.out.println("3 for Search Customer");
            System.out.println("4 for Delete Customer");
            System.out.println("5 for Exit the bank application");
            choice = sc.nextInt();
            sc.nextLine(); // consume newline

            switch(choice) {
                case 1: addCustomer(sc); break;
                case 2: displayCustomers(); break;
                case 3: searchCustomer(sc); break;
                case 4: deleteCustomer(sc); break;
                case 5: System.out.println("Exiting..."); break;
                default: System.out.println("Invalid choice!");
            }
        } while (choice != 5);
    }

    private void addCustomer(Scanner sc) {
        System.out.println("Enter name: ");
        String name = sc.nextLine();
        System.out.println("Enter email: ");
        String email = sc.nextLine();
        System.out.println("Enter contact: ");
        String contact = sc.nextLine();
        System.out.println("Enter account type (Savings or Current): ");
        String accountType = sc.nextLine();

        int customerId = 1000 + rand.nextInt(9000);
        Customer c = new Customer(customerId, name, email, contact, accountType);
        customers.add(c);
        System.out.println("Customer added successfully with customer id " + customerId);
    }

    private void displayCustomers() {
        for(Customer c : customers) {
            System.out.println(c);
        }
    }

    private void searchCustomer(Scanner sc) {
        System.out.println("Enter customer ID to search: ");
        int id = sc.nextInt();
        for(Customer c : customers) {
            if(c.getCustomerId() == id) {
                System.out.println(c);
                return;
            }
        }
        System.out.println("Customer not found.");
    }

    private void deleteCustomer(Scanner sc) {
        System.out.println("Enter customer ID to delete: ");
        int id = sc.nextInt();
        Iterator<Customer> it = customers.iterator();
        while(it.hasNext()) {
            Customer c = it.next();
            if(c.getCustomerId() == id) {
                it.remove();
                System.out.println("Customer deleted.");
                return;
            }
        }
        System.out.println("Customer not found.");
    }
}
