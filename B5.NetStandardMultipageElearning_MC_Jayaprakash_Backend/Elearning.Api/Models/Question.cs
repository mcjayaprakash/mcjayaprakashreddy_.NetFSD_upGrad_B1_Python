using System.ComponentModel.DataAnnotations;

namespace Elearning.Api.Models;

public class Question
{
    public int QuestionId { get; set; }

    public int QuizId { get; set; }

    [MaxLength(600)]
    public string QuestionText { get; set; } = string.Empty;

    [MaxLength(250)]
    public string OptionA { get; set; } = string.Empty;

    [MaxLength(250)]
    public string OptionB { get; set; } = string.Empty;

    [MaxLength(250)]
    public string OptionC { get; set; } = string.Empty;

    [MaxLength(250)]
    public string OptionD { get; set; } = string.Empty;

    [MaxLength(1)]
    public string CorrectAnswer { get; set; } = string.Empty;

    public Quiz? Quiz { get; set; }
}
