using Elearning.Api.DTOs;

namespace Elearning.Api.Services;

public interface IQuizService
{
    Task<ServiceResult<IReadOnlyCollection<QuizDto>>> GetByCourseAsync(int courseId);
    Task<ServiceResult<QuizDto>> CreateQuizAsync(QuizCreateDto dto);
    Task<ServiceResult<IReadOnlyCollection<QuestionDto>>> GetQuestionsAsync(int quizId);
    Task<ServiceResult<QuestionDto>> CreateQuestionAsync(QuestionCreateDto dto);
    Task<ServiceResult<QuizSubmitResponseDto>> SubmitAsync(int quizId, QuizSubmitDto dto);
}
