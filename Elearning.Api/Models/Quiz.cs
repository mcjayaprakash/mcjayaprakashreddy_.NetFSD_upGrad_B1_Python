using System.ComponentModel.DataAnnotations;

namespace Elearning.Api.Models;

public class Quiz
{
    public int QuizId { get; set; }

    public int CourseId { get; set; }

    [MaxLength(160)]
    public string Title { get; set; } = string.Empty;

    public Course? Course { get; set; }

    public ICollection<Question> Questions { get; set; } = new List<Question>();

    public ICollection<Result> Results { get; set; } = new List<Result>();
}
