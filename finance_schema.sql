
CREATE DATABASE FinanceDB;
USE FinanceDB;

CREATE TABLE Transactions (
    TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    Amount DECIMAL(10, 2),
    Date DATE,
    Category TEXT,
    Description TEXT
);
