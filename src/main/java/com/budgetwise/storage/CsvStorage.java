package com.budgetwise.storage;

import com.budgetwise.model.Category;
import com.budgetwise.model.Transaction;
import java.io.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/**
 * Clean CSV file persistence for transactions using standard BufferedReader and PrintWriter.
 */
public class CsvStorage {

    public static List<Transaction> loadTransactions(File file) throws IOException {
        List<Transaction> list = new ArrayList<>();
        if (!file.exists()) return list;

        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line = reader.readLine(); // skip header: id,accountId,date,description,amount,type,category
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) continue;
                String[] parts = line.split(",");
                if (parts.length >= 7) {
                    String id = parts[0].trim();
                    String accId = parts[1].trim();
                    LocalDate date = LocalDate.parse(parts[2].trim());
                    String desc = parts[3].trim();
                    BigDecimal amount = new BigDecimal(parts[4].trim());
                    Transaction.Type type = Transaction.Type.valueOf(parts[5].trim());
                    Category category = Category.valueOf(parts[6].trim());
                    list.add(new Transaction(id, accId, date, desc, amount, type, category));
                }
            }
        }
        return list;
    }

    public static void saveTransactions(File file, List<Transaction> transactions) throws IOException {
        File parent = file.getParentFile();
        if (parent != null && !parent.exists()) {
            parent.mkdirs();
        }
        try (PrintWriter writer = new PrintWriter(new FileWriter(file))) {
            writer.println("id,accountId,date,description,amount,type,category");
            for (Transaction tx : transactions) {
                writer.printf("%s,%s,%s,%s,%.2f,%s,%s%n",
                        tx.getId(), tx.getAccountId(), tx.getDate(),
                        tx.getDescription().replace(",", " "),
                        tx.getAmount(), tx.getType(), tx.getCategory());
            }
        }
    }
}
