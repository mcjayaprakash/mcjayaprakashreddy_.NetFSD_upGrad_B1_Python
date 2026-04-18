CREATE DATABASE ElearningPlatformDb;
GO

USE ElearningPlatformDb;
GO

CREATE TABLE Users (
    UserId INT IDENTITY(1,1) PRIMARY KEY,
    FullName VARCHAR(120) NOT NULL,
    Email VARCHAR(180) NOT NULL UNIQUE,
    PasswordHash VARCHAR(500) NOT NULL,
    Role VARCHAR(30) NOT NULL DEFAULT 'Learner',
    CreatedAt DATETIME NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE Courses (
    CourseId INT IDENTITY(1,1) PRIMARY KEY,
    Title VARCHAR(160) NOT NULL,
    Description VARCHAR(1200) NOT NULL,
    CreatedBy INT NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETUTCDATE(),
    CONSTRAINT FK_Courses_Users_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Users(UserId)
);

CREATE TABLE Lessons (
    LessonId INT IDENTITY(1,1) PRIMARY KEY,
    CourseId INT NOT NULL,
    Title VARCHAR(160) NOT NULL,
    Content VARCHAR(MAX) NOT NULL,
    OrderIndex INT NOT NULL,
    CONSTRAINT FK_Lessons_Courses_CourseId FOREIGN KEY (CourseId) REFERENCES Courses(CourseId) ON DELETE CASCADE
);

CREATE TABLE Quizzes (
    QuizId INT IDENTITY(1,1) PRIMARY KEY,
    CourseId INT NOT NULL,
    Title VARCHAR(160) NOT NULL,
    CONSTRAINT FK_Quizzes_Courses_CourseId FOREIGN KEY (CourseId) REFERENCES Courses(CourseId) ON DELETE CASCADE
);

CREATE TABLE Questions (
    QuestionId INT IDENTITY(1,1) PRIMARY KEY,
    QuizId INT NOT NULL,
    QuestionText VARCHAR(600) NOT NULL,
    OptionA VARCHAR(250) NOT NULL,
    OptionB VARCHAR(250) NOT NULL,
    OptionC VARCHAR(250) NOT NULL,
    OptionD VARCHAR(250) NOT NULL,
    CorrectAnswer VARCHAR(1) NOT NULL,
    CONSTRAINT FK_Questions_Quizzes_QuizId FOREIGN KEY (QuizId) REFERENCES Quizzes(QuizId) ON DELETE CASCADE
);

CREATE TABLE Results (
    ResultId INT IDENTITY(1,1) PRIMARY KEY,
    UserId INT NOT NULL,
    QuizId INT NOT NULL,
    Score INT NOT NULL,
    AttemptDate DATETIME NOT NULL DEFAULT GETUTCDATE(),
    CONSTRAINT FK_Results_Users_UserId FOREIGN KEY (UserId) REFERENCES Users(UserId) ON DELETE CASCADE,
    CONSTRAINT FK_Results_Quizzes_QuizId FOREIGN KEY (QuizId) REFERENCES Quizzes(QuizId) ON DELETE CASCADE
);
GO

-- DML: INSERT
INSERT INTO Users (FullName, Email, PasswordHash, Role)
VALUES ('Jayaprakash', 'jp@gmail.com', 'HASHED_PASSWORD_FROM_APPLICATION', 'Learner');

INSERT INTO Users (FullName, Email, PasswordHash, Role)
VALUES ('Admin Manager', 'admin@learnify.com', 'HASHED_PASSWORD_FROM_APPLICATION', 'Admin');

INSERT INTO Courses (Title, Description, CreatedBy)
VALUES ('SQL', 'Practice joins, subqueries and aggregation.', 1);

INSERT INTO Lessons (CourseId, Title, Content, OrderIndex)
VALUES (1, 'Joins', 'INNER JOIN and LEFT JOIN practice.', 1);

-- Basic Queries: SELECT, WHERE, ORDER BY
SELECT CourseId, Title, Description
FROM Courses
WHERE Title LIKE '%SQL%'
ORDER BY Title;

-- INNER JOIN
SELECT c.Title AS CourseTitle, u.FullName AS CreatedBy
FROM Courses c
INNER JOIN Users u ON c.CreatedBy = u.UserId;

-- LEFT JOIN
SELECT c.Title AS CourseTitle, l.Title AS LessonTitle
FROM Courses c
LEFT JOIN Lessons l ON c.CourseId = l.CourseId
ORDER BY c.Title, l.OrderIndex;

-- Aggregation: GROUP BY, COUNT, AVG
SELECT q.Title, COUNT(r.ResultId) AS Attempts, AVG(CAST(r.Score AS DECIMAL(10,2))) AS AverageScore
FROM Quizzes q
LEFT JOIN Results r ON q.QuizId = r.QuizId
GROUP BY q.Title;

-- Subquery: users scoring above average
SELECT u.UserId, u.FullName, r.Score
FROM Users u
INNER JOIN Results r ON u.UserId = r.UserId
WHERE r.Score > (SELECT AVG(CAST(Score AS DECIMAL(10,2))) FROM Results);

-- Set operator: UNION
SELECT Title AS LearningItem FROM Courses
UNION
SELECT Title AS LearningItem FROM Lessons;

-- DML: UPDATE
UPDATE Courses
SET Description = 'Updated SQL course description.'
WHERE Title = 'SQL';

-- DML: DELETE
DELETE FROM Lessons
WHERE Title = 'Joins' AND CourseId = 1;
