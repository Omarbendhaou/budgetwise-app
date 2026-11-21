package com.budgetwise.model;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.util.Objects;

/**
 * Immutable financial transaction entity using scale-2 BigDecimal for monetary precision.
 */
public final class Transaction {
    public enum Type { INCOME, EXPENSE }

    private final String id;
    private final String accountId;
    private final LocalDate date;
    private final String description;
    private final BigDecimal amount;
    private final Type type;
    private final Category category;

    public Transaction(String id, String accountId, LocalDate date, String description,
                       BigDecimal amount, Type type, Category category) {
        this.id = Objects.requireNonNull(id, "ID cannot be null");
        this.accountId = Objects.requireNonNull(accountId, "Account ID cannot be null");
        this.date = Objects.requireNonNull(date, "Date cannot be null");
        this.description = Objects.requireNonNull(description, "Description cannot be null");
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Transaction amount must be strictly positive");
        }
        this.amount = amount.setScale(2, RoundingMode.HALF_UP);
        this.type = Objects.requireNonNull(type, "Type cannot be null");
        this.category = Objects.requireNonNull(category, "Category cannot be null");
    }

    public String getId() { return id; }
    public String getAccountId() { return accountId; }
    public LocalDate getDate() { return date; }
    public String getDescription() { return description; }
    public BigDecimal getAmount() { return amount; }
    public Type getType() { return type; }
    public Category getCategory() { return category; }

    @Override
    public String toString() {
        String sign = (type == Type.INCOME) ? "+" : "-";
        return String.format("%s | %-8s | %s$%8.2f | %-14s | %s",
                date, id, sign, amount, category, description);
    }
}
