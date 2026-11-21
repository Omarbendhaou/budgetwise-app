package com.budgetwise.model;

import java.util.Objects;

/**
 * Immutable warning alert issued by anomaly detection rules.
 */
public final class Alert {
    public enum Severity { INFO, WARNING, CRITICAL }

    private final String ruleName;
    private final String message;
    private final Severity severity;

    public Alert(String ruleName, String message, Severity severity) {
        this.ruleName = Objects.requireNonNull(ruleName, "Rule name cannot be null");
        this.message = Objects.requireNonNull(message, "Message cannot be null");
        this.severity = Objects.requireNonNull(severity, "Severity cannot be null");
    }

    public String getRuleName() { return ruleName; }
    public String getMessage() { return message; }
    public Severity getSeverity() { return severity; }

    @Override
    public String toString() {
        return String.format("[%s] (%s): %s", severity, ruleName, message);
    }
}
