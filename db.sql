-- Create Users table
CREATE TABLE Users (
    UserId INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    MasterPasswordHash CHAR(60) NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Credentials table
CREATE TABLE Credentials (
    CredentialId INT AUTO_INCREMENT PRIMARY KEY,
    UserId INT NOT NULL,
    GroupId INT,
    Title VARCHAR(255) NOT NULL,
    Username VARCHAR(255),
    Password VARBINARY(255) NOT NULL,
    URL VARCHAR(255),
    Notes TEXT,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (UserId) REFERENCES Users(UserId) ON DELETE CASCADE,
    FOREIGN KEY (GroupId) REFERENCES Groups(GroupId) ON DELETE SET NULL
);

-- Create Groups table
CREATE TABLE Groups (
    GroupId INT AUTO_INCREMENT PRIMARY KEY,
    UserId INT NOT NULL,
    GroupName VARCHAR(255) NOT NULL,
    Description TEXT,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (UserId) REFERENCES Users(UserId) ON DELETE CASCADE
);

-- Create AuditLogs table
CREATE TABLE AuditLogs (
    LogId INT AUTO_INCREMENT PRIMARY KEY,
    UserId INT NOT NULL,
    CredentialId INT,
    Action VARCHAR(50) NOT NULL,
    Timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserId) REFERENCES Users(UserId) ON DELETE CASCADE,
    FOREIGN KEY (CredentialId) REFERENCES Credentials(CredentialId) ON DELETE SET NULL
);