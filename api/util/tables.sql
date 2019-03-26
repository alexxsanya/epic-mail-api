CREATE TABLE IF NOT EXISTS users
    (
        id SERIAL PRIMARY KEY,
        firstname VARCHAR(15) NOT NULL UNIQUE,
        lastname VARCHAR(15) NOT NULL UNIQUE,
        email VARCHAR(50) UNIQUE NOT NULL,
        recoveryEmail VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(150) NOT NULL)
        createdOn TIMESTAMP DEFAULT NOW()
    );
 
CREATE TABLE IF NOT EXISTS messages
    (
        id SERIAL PRIMARY KEY,
        subject VARCHAR(15) NOT NULL UNIQUE,
        msgBody VARCHAR(15) NOT NULL UNIQUE,
        parentId INT UNIQUE NOT NULL,
        status VARCHAR(50) UNIQUE NOT NULL,
        createdOn TIMESTAMP DEFAULT NOW(),
        createdBy INT NOT NULL,
        FOREIGN KEY (createdBy) REFERENCES users (id)
    );

CREATE TABLE IF NOT EXISTS messages_sent
    ( 
        messageId INT NOT NULL,
        senderId INT NOT NULL,
        createdOn TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (messageId) REFERENCES messages (id),
        FOREIGN KEY (senderId) REFERENCES users (id)
    );

CREATE TABLE IF NOT EXISTS messages_received
    (
        messageId INT NOT NULL UNIQUE,
        receiverId INT NOT NULL UNIQUE,
        createOn TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (messageId) REFERENCES messages (id),
        FOREIGN KEY (senderId) REFERENCES users (id)
    );

CREATE TABLE IF NOT EXISTS groups
    (
        id SERIAL PRIMARY KEY,
        name VARCHAR(25) NOT NULL UNIQUE,
        role VARCHAR(25) NOT NULL UNIQUE,
        createOn TIMESTAMP DEFAULT NOW()
    );

CREATE TABLE IF NOT EXISTS group_users
    (
        groupId INT NOT NULL UNIQUE,
        userId INT NOT NULL UNIQUE,
        userRole VARCHAR(25) NOT NULL UNIQUE,
        createOn TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (userId) REFERENCES users (id),
        FOREIGN KEY (groupId) REFERENCES groups (id)
    );
