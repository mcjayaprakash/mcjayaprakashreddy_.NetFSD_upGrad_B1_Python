using Elearning.Api.DTOs;
using Elearning.Api.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Elearning.Api.Controllers;

[Route("api")]
public class QuizzesController(IQuizService quizzes) : ApiControllerBase
{
    [HttpGet("quizzes/{courseId:int}")]
    public async Task<ActionResult<IReadOnlyCollection<QuizDto>>> GetByCourse(int courseId) =>
        FromServiceResult(await quizzes.GetByCourseAsync(courseId));

    [HttpPost("quizzes")]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<QuizDto>> CreateQuiz(QuizCreateDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        var result = await quizzes.CreateQuizAsync(dto);
        if (!result.Success)
        {
            return FromServiceResult(result);
        }

        return CreatedAtAction(nameof(GetByCourse), new { courseId = result.Value!.CourseId }, result.Value);
    }

    [HttpGet("quizzes/{quizId:int}/questions")]
    public async Task<ActionResult<IReadOnlyCollection<QuestionDto>>> GetQuestions(int quizId) =>
        FromServiceResult(await quizzes.GetQuestionsAsync(quizId));

    [HttpPost("questions")]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<QuestionDto>> CreateQuestion(QuestionCreateDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        var result = await quizzes.CreateQuestionAsync(dto);
        if (!result.Success)
        {
            return FromServiceResult(result);
        }

        return CreatedAtAction(nameof(GetQuestions), new { quizId = result.Value!.QuizId }, result.Value);
    }

    [HttpPost("quizzes/{quizId:int}/submit")]
    [Authorize]
    public async Task<ActionResult<QuizSubmitResponseDto>> Submit(int quizId, QuizSubmitDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        return FromServiceResult(await quizzes.SubmitAsync(quizId, dto));
    }
}
