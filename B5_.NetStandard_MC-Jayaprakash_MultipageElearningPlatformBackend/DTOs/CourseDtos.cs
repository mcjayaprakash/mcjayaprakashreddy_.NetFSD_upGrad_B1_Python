using System.ComponentModel.DataAnnotations;

namespace Elearning.Api.DTOs;

public record CourseSummaryDto(
    int CourseId,
    string Title,
    string Description,
    int CreatedBy,
    string CreatedByName,
    DateTime CreatedAt,
    int LessonCount,
    int QuizCount);

public record CourseDetailDto(
    int CourseId,
    string Title,
    string Description,
    int CreatedBy,
    string CreatedByName,
    DateTime CreatedAt,
    IReadOnlyCollection<LessonDto> Lessons,
    IReadOnlyCollection<QuizDto> Quizzes);

public class CourseCreateDto
{
    [Required, StringLength(160, MinimumLength = 3)]
    public string Title { get; set; } = string.Empty;

    [Required, StringLength(1200, MinimumLength = 10)]
    public string Description { get; set; } = string.Empty;
}

public class CourseUpdateDto
{
    [Required, StringLength(160, MinimumLength = 3)]
    public string Title { get; set; } = string.Empty;

    [Required, StringLength(1200, MinimumLength = 10)]
    public string Description { get; set; } = string.Empty;
}
