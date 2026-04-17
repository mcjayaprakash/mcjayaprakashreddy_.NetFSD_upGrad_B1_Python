using System.ComponentModel.DataAnnotations;

namespace Elearning.Api.Models;

public class Course
{
    public int CourseId { get; set; }

    [MaxLength(160)]
    public string Title { get; set; } = string.Empty;

    [MaxLength(1200)]
    public string Description { get; set; } = string.Empty;

    public int CreatedBy { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public User? Creator { get; set; }

    public ICollection<Lesson> Lessons { get; set; } = new List<Lesson>();

    public ICollection<Quiz> Quizzes { get; set; } = new List<Quiz>();
}
