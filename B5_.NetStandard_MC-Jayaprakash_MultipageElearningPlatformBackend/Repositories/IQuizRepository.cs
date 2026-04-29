using Elearning.Api.Models;

namespace Elearning.Api.Repositories;

public interface IQuizRepository
{
    Task<List<Quiz>> GetByCourseAsync(int courseId);
    Task<Quiz?> GetByIdWithQuestionsAsync(int quizId);
    Task<bool> CourseExistsAsync(int courseId);
    Task<bool> QuizExistsAsync(int quizId);
    Task<Quiz> AddQuizAsync(Quiz quiz);
    Task<Question> AddQuestionAsync(Question question);
    Task<List<Question>> GetQuestionsAsync(int quizId);
}
