package com.budgetwise.model;

import com.budgetwise.exception.ValidationException;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Objects;

/**
 * Deeply immutable value object representing a financial transaction.
 * Monetary calculations strictly use BigDecimal with scale 2.
 */
public final class Transaction {
    private final String id;
    private final String accountId;
    private final LocalDate date;
    private final String description;
    private final BigDecimal amount;
    private final TransactionType type;
    private final Category category;

    public Transaction(String id, String accountId, LocalDate date, String description,
                       BigDecimal amount, TransactionType type, Category category) {
        if (id == null || id.trim().isEmpty()) {
            throw new ValidationException("Transaction ID cannot be null or empty.");
        }
        if (accountId == null || accountId.trim().isEmpty()) {
            throw new ValidationException("Account ID cannot be null or empty.");
        }
        if (date == null) {
            throw new ValidationException("Transaction date cannot be null.");
        }
        if (description == null || description.trim().isEmpty()) {
            throw new ValidationException("Transaction description cannot be null or empty.");
        }
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new ValidationException("Transaction amount must be strictly positive.");
        }
        if (amount.scale() > 2) {
            throw new ValidationException("Transaction amount cannot have more than 2 decimal places.");
        }
        if (type == null) {
            throw new ValidationException("Transaction type cannot be null.");
        }
        this.id = id.trim();
        this.accountId = accountId.trim();
        this.date = date;
        this.description = description.trim();
        this.amount = amount;
        this.type = type;
        this.category = category != null ? category : Category.UNCATEGORIZED;
    }

    public String getId() { return id; }
    public String getAccountId() { return accountId; }
    public LocalDate getDate() { return date; }
    public String getDescription() { return description; }
    public BigDecimal getAmount() { return amount; }
    public TransactionType getType() { return type; }
    public Category getCategory() { return category; }

    public BigDecimal getSignedAmount() {
        return amount.multiply(type.getMultiplier());
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Transaction that)) return false;
        return id.equalsIgnoreCase(that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id.toLowerCase());
    }

    @Override
    public String toString() {
        return String.format("[%s] %s | %s | %s %s | Category: %s",
                id, date, description, type, amount, category.getName());
    }
}
