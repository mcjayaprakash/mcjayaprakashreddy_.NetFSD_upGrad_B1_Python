using AutoMapper;
using Elearning.Api.Data;
using Elearning.Api.Mapping;
using Elearning.Api.Models;
using Elearning.Api.Repositories;
using Elearning.Api.Security;
using Elearning.Api.Services;
using Microsoft.EntityFrameworkCore;

namespace Elearning.Tests;

public static class TestFactory
{
    private sealed class FakeTokenService : ITokenService
    {
        public string CreateToken(User user) => $"fake-token-{user.UserId}";
    }

    public static ElearningDbContext CreateDb()
    {
        var options = new DbContextOptionsBuilder<ElearningDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;

        return new ElearningDbContext(options);
    }

    public static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => cfg.AddProfile<ElearningProfile>());
        return config.CreateMapper();
    }

    public static async Task<(ElearningDbContext Db, User User, Course Course, Quiz Quiz)> SeedQuizAsync()
    {
        var db = CreateDb();
        var user = new User
        {
            FullName = "Test Learner",
            Email = "learner@test.com",
            PasswordHash = "hash",
            Role = "Learner",
            CreatedAt = DateTime.UtcNow
        };

        db.Users.Add(user);
        await db.SaveChangesAsync();

        var course = new Course
        {
            Title = "JavaScript Basics",
            Description = "Learn variables and DOM events.",
            CreatedBy = user.UserId,
            CreatedAt = DateTime.UtcNow
        };

        db.Courses.Add(course);
        await db.SaveChangesAsync();

        var quiz = new Quiz
        {
            CourseId = course.CourseId,
            Title = "JavaScript Basics Quiz",
            Questions =
            [
                new Question
                {
                    QuestionText = "JavaScript is?",
                    OptionA = "Programming Language",
                    OptionB = "Database",
                    OptionC = "OS",
                    OptionD = "Network",
                    CorrectAnswer = "A"
                },
                new Question
                {
                    QuestionText = "CSS is used for?",
                    OptionA = "Database",
                    OptionB = "Styling",
                    OptionC = "Backend",
                    OptionD = "Hosting",
                    CorrectAnswer = "B"
                }
            ]
        };

        db.Quizzes.Add(quiz);
        await db.SaveChangesAsync();

        return (db, user, course, quiz);
    }

    public static CourseService CreateCourseService(ElearningDbContext db) =>
        new(new CourseRepository(db), CreateMapper());

    public static QuizService CreateQuizService(ElearningDbContext db) =>
        new(new QuizRepository(db), new ResultRepository(db), CreateMapper());

    public static UserService CreateUserService(ElearningDbContext db) =>
        new(new UserRepository(db), new PasswordHasher(), new FakeTokenService(), CreateMapper());
}
