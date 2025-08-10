import java.sql.*;

public class AccountDB {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/bankdb";
        String user = "root";
        String pass = "root";

        try (Connection con = DriverManager.getConnection(url, user, pass)) {
            Statement stmt = con.createStatement();

            // Create table
            String createTable = "CREATE TABLE IF NOT EXISTS Accounts (" +
                                 "accountNum VARCHAR(20) PRIMARY KEY," +
                                 "accountOwner VARCHAR(50)," +
                                 "balance DOUBLE)";
            stmt.executeUpdate(createTable);

            // Insert record (Create)
            String insert = "INSERT INTO Accounts VALUES('A1001','Alice',5000)";
            stmt.executeUpdate(insert);

            // Read records
            ResultSet rs = stmt.executeQuery("SELECT * FROM Accounts");
            while (rs.next()) {
                System.out.println(rs.getString("accountNum") + " | " +
                                   rs.getString("accountOwner") + " | " +
                                   rs.getDouble("balance"));
            }

            // Update record
            String update = "UPDATE Accounts SET balance=6000 WHERE accountNum='A1001'";
            stmt.executeUpdate(update);

            // Delete record
            String delete = "DELETE FROM Accounts WHERE accountNum='A1001'";
            stmt.executeUpdate(delete);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}