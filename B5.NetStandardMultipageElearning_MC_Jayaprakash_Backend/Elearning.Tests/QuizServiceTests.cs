using Elearning.Api.DTOs;
using Elearning.Api.Services;

namespace Elearning.Tests;

public class QuizServiceTests
{
    [Fact]
    public async Task SubmitAsync_ScoresQuizAndStoresResult()
    {
        var (db, user, _, quiz) = await TestFactory.SeedQuizAsync();
        var service = TestFactory.CreateQuizService(db);
        var questions = quiz.Questions.OrderBy(q => q.QuestionId).ToList();

        var result = await service.SubmitAsync(quiz.QuizId, new QuizSubmitDto
        {
            UserId = user.UserId,
            Answers =
            [
                new() { QuestionId = questions[0].QuestionId, SelectedAnswer = "A" },
                new() { QuestionId = questions[1].QuestionId, SelectedAnswer = "A" }
            ]
        });

        Assert.True(result.Success);
        Assert.Equal(1, result.Value!.Score);
        Assert.Equal(50m, result.Value.Percentage);
        Assert.Single(db.Results);
    }

    [Fact]
    public async Task SubmitAsync_InvalidQuiz_ReturnsNotFound()
    {
        var (db, user, _, _) = await TestFactory.SeedQuizAsync();
        var service = TestFactory.CreateQuizService(db);

        var result = await service.SubmitAsync(999, new QuizSubmitDto
        {
            UserId = user.UserId,
            Answers = [new() { QuestionId = 1, SelectedAnswer = "A" }]
        });

        Assert.False(result.Success);
        Assert.Equal(ServiceErrorType.NotFound, result.ErrorType);
    }
}
