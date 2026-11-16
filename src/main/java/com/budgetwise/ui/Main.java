package com.budgetwise.ui;

import com.budgetwise.factory.DefaultApplicationFactory;

public class Main {
    public static void main(String[] args) {
        System.out.println("Initializing BudgetWise Financial Engine...");
        DefaultApplicationFactory factory = new DefaultApplicationFactory();
        ConsoleMenu menu = new ConsoleMenu(factory);
        menu.runDemoScenarioB();
    }
}
