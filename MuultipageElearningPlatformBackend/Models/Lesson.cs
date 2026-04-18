using System.ComponentModel.DataAnnotations;

namespace Elearning.Api.Models;

public class Lesson
{
    public int LessonId { get; set; }

    public int CourseId { get; set; }

    [MaxLength(160)]
    public string Title { get; set; } = string.Empty;

    public string Content { get; set; } = string.Empty;

    public int OrderIndex { get; set; }

    public Course? Course { get; set; }
}
