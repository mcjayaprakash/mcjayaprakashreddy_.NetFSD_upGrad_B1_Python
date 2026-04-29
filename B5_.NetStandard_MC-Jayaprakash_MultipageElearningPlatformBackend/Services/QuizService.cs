using AutoMapper;
using Elearning.Api.DTOs;
using Elearning.Api.Models;
using Elearning.Api.Repositories;

namespace Elearning.Api.Services;

public class QuizService(IQuizRepository quizzes, IResultRepository results, IMapper mapper) : IQuizService
{
    public async Task<ServiceResult<IReadOnlyCollection<QuizDto>>> GetByCourseAsync(int courseId)
    {
        if (!await quizzes.CourseExistsAsync(courseId))
        {
            return ServiceResult<IReadOnlyCollection<QuizDto>>.NotFound("Course not found.");
        }

        return ServiceResult<IReadOnlyCollection<QuizDto>>.Ok(mapper.Map<List<QuizDto>>(await quizzes.GetByCourseAsync(courseId)));
    }

    public async Task<ServiceResult<QuizDto>> CreateQuizAsync(QuizCreateDto dto)
    {
        if (!await quizzes.CourseExistsAsync(dto.CourseId))
        {
            return ServiceResult<QuizDto>.BadRequest("Course does not exist.");
        }

        var quiz = mapper.Map<Quiz>(dto);
        await quizzes.AddQuizAsync(quiz);
        return ServiceResult<QuizDto>.Ok(mapper.Map<QuizDto>(quiz));
    }

    public async Task<ServiceResult<IReadOnlyCollection<QuestionDto>>> GetQuestionsAsync(int quizId)
    {
        if (!await quizzes.QuizExistsAsync(quizId))
        {
            return ServiceResult<IReadOnlyCollection<QuestionDto>>.NotFound("Quiz not found.");
        }

        return ServiceResult<IReadOnlyCollection<QuestionDto>>.Ok(mapper.Map<List<QuestionDto>>(await quizzes.GetQuestionsAsync(quizId)));
    }

    public async Task<ServiceResult<QuestionDto>> CreateQuestionAsync(QuestionCreateDto dto)
    {
        if (!await quizzes.QuizExistsAsync(dto.QuizId))
        {
            return ServiceResult<QuestionDto>.BadRequest("Quiz does not exist.");
        }

        var question = mapper.Map<Question>(dto);
        await quizzes.AddQuestionAsync(question);
        return ServiceResult<QuestionDto>.Ok(mapper.Map<QuestionDto>(question));
    }

    public async Task<ServiceResult<QuizSubmitResponseDto>> SubmitAsync(int quizId, QuizSubmitDto dto)
    {
        if (!await results.UserExistsAsync(dto.UserId))
        {
            return ServiceResult<QuizSubmitResponseDto>.BadRequest("User does not exist.");
        }

        var quiz = await quizzes.GetByIdWithQuestionsAsync(quizId);
        if (quiz is null)
        {
            return ServiceResult<QuizSubmitResponseDto>.NotFound("Quiz not found.");
        }

        if (quiz.Questions.Count == 0)
        {
            return ServiceResult<QuizSubmitResponseDto>.BadRequest("Quiz has no questions.");
        }

        var answerLookup = dto.Answers.ToDictionary(a => a.QuestionId, a => a.SelectedAnswer.ToUpperInvariant());
        var invalidQuestion = answerLookup.Keys.Any(questionId => quiz.Questions.All(q => q.QuestionId != questionId));
        if (invalidQuestion)
        {
            return ServiceResult<QuizSubmitResponseDto>.BadRequest("Submission contains a question that is not part of this quiz.");
        }

        var score = quiz.Questions.Count(question =>
            answerLookup.TryGetValue(question.QuestionId, out var answer)
            && answer == question.CorrectAnswer.ToUpperInvariant());

        var result = await results.AddAsync(new Result
        {
            QuizId = quizId,
            UserId = dto.UserId,
            Score = score,
            AttemptDate = DateTime.UtcNow
        });

        var percentage = Math.Round((decimal)score / quiz.Questions.Count * 100, 2);
        var feedback = percentage switch
        {
            >= 80 => "Excellent",
            >= 50 => "Good",
            _ => "Needs Improvement"
        };

        return ServiceResult<QuizSubmitResponseDto>.Ok(new QuizSubmitResponseDto(
            result.ResultId,
            quizId,
            dto.UserId,
            score,
            quiz.Questions.Count,
            percentage,
            feedback));
    }
}
