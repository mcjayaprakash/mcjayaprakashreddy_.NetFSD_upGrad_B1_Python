using Elearning.Api.Data;
using Elearning.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace Elearning.Api.Repositories;

public class QuizRepository(ElearningDbContext db) : IQuizRepository
{
    public Task<List<Quiz>> GetByCourseAsync(int courseId) =>
        db.Quizzes
            .AsNoTracking()
            .Include(q => q.Questions)
            .Where(q => q.CourseId == courseId)
            .OrderBy(q => q.Title)
            .ToListAsync();

    public Task<Quiz?> GetByIdWithQuestionsAsync(int quizId) =>
        db.Quizzes
            .AsNoTracking()
            .Include(q => q.Questions)
            .FirstOrDefaultAsync(q => q.QuizId == quizId);

    public Task<bool> CourseExistsAsync(int courseId) =>
        db.Courses.AsNoTracking().AnyAsync(c => c.CourseId == courseId);

    public Task<bool> QuizExistsAsync(int quizId) =>
        db.Quizzes.AsNoTracking().AnyAsync(q => q.QuizId == quizId);

    public async Task<Quiz> AddQuizAsync(Quiz quiz)
    {
        db.Quizzes.Add(quiz);
        await db.SaveChangesAsync();
        return quiz;
    }

    public async Task<Question> AddQuestionAsync(Question question)
    {
        db.Questions.Add(question);
        await db.SaveChangesAsync();
        return question;
    }

    public Task<List<Question>> GetQuestionsAsync(int quizId) =>
        db.Questions
            .AsNoTracking()
            .Where(q => q.QuizId == quizId)
            .OrderBy(q => q.QuestionId)
            .ToListAsync();
}
