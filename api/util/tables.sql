CREATE TABLE IF NOT EXISTS users
    (
        id SERIAL PRIMARY KEY,
        firstname VARCHAR(15) NOT NULL,
        lastname VARCHAR(15) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        recoveryEmail VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(150) NOT NULL,
        createdOn TIMESTAMP DEFAULT NOW()
    );
 
CREATE TABLE IF NOT EXISTS messages
    (
        id SERIAL PRIMARY KEY,
        subject VARCHAR(255) NOT NULL,
        msgBody TEXT NOT NULL,
        parentId INT NOT NULL,
        status VARCHAR(50) NOT NULL,
        readStatus VARCHAR(50) DEFAULT 'unread',
        IsGroupMail BOOLEAN DEFAULT FALSE,
        createdOn TIMESTAMP DEFAULT NOW(),
        createdBy INT NOT NULL,
        FOREIGN KEY (createdBy) REFERENCES users (id)
    );

CREATE TABLE IF NOT EXISTS messages_sent
    ( 
        messageId INT NOT NULL UNIQUE,
        senderId INT NOT NULL,
        createdOn TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (messageId) REFERENCES messages (id),
        FOREIGN KEY (senderId) REFERENCES users (id)
    );

CREATE TABLE IF NOT EXISTS messages_received
    (
        messageId INT NOT NULL UNIQUE,
        receiverId INT NOT NULL,
        createOn TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (messageId) REFERENCES messages (id),
        FOREIGN KEY (receiverId) REFERENCES users (id)
    );

CREATE TABLE IF NOT EXISTS groups
    (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        role VARCHAR(50) NOT NULL,
        createdBy INT NOT NULL,
        createOn TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (createdBy) REFERENCES users (id)
    );

CREATE TABLE IF NOT EXISTS group_users
    (
        groupId INT NOT NULL,
        userId INT NOT NULL,
        userRole VARCHAR(100) NOT NULL,
        createOn TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (userId) REFERENCES users (id),
        FOREIGN KEY (groupId) REFERENCES groups (id)
    );
