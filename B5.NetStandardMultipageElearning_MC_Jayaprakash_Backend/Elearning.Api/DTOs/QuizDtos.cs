using System.ComponentModel.DataAnnotations;

namespace Elearning.Api.DTOs;

public record QuizDto(int QuizId, int CourseId, string Title, int QuestionCount);

public record QuestionDto(
    int QuestionId,
    int QuizId,
    string QuestionText,
    string OptionA,
    string OptionB,
    string OptionC,
    string OptionD);

public record QuizSubmitResponseDto(int ResultId, int QuizId, int UserId, int Score, int TotalQuestions, decimal Percentage, string Feedback);

public class QuizCreateDto
{
    [Range(1, int.MaxValue)]
    public int CourseId { get; set; }

    [Required, StringLength(160, MinimumLength = 3)]
    public string Title { get; set; } = string.Empty;
}

public class QuestionCreateDto
{
    [Range(1, int.MaxValue)]
    public int QuizId { get; set; }

    [Required, StringLength(600, MinimumLength = 5)]
    public string QuestionText { get; set; } = string.Empty;

    [Required, StringLength(250)]
    public string OptionA { get; set; } = string.Empty;

    [Required, StringLength(250)]
    public string OptionB { get; set; } = string.Empty;

    [Required, StringLength(250)]
    public string OptionC { get; set; } = string.Empty;

    [Required, StringLength(250)]
    public string OptionD { get; set; } = string.Empty;

    [Required, RegularExpression("^[ABCDabcd]$")]
    public string CorrectAnswer { get; set; } = string.Empty;
}

public class QuizSubmitDto
{
    [Range(1, int.MaxValue)]
    public int UserId { get; set; }

    [Required, MinLength(1)]
    public List<QuizAnswerDto> Answers { get; set; } = [];
}

public class QuizAnswerDto
{
    [Range(1, int.MaxValue)]
    public int QuestionId { get; set; }

    [Required, RegularExpression("^[ABCDabcd]$")]
    public string SelectedAnswer { get; set; } = string.Empty;
}
