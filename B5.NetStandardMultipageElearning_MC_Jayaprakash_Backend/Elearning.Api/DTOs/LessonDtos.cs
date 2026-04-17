using System.ComponentModel.DataAnnotations;

namespace Elearning.Api.DTOs;

public record LessonDto(int LessonId, int CourseId, string Title, string Content, int OrderIndex);

public class LessonCreateDto
{
    [Range(1, int.MaxValue)]
    public int CourseId { get; set; }

    [Required, StringLength(160, MinimumLength = 2)]
    public string Title { get; set; } = string.Empty;

    [Required, MinLength(5)]
    public string Content { get; set; } = string.Empty;

    [Range(1, 200)]
    public int OrderIndex { get; set; }
}

public class LessonUpdateDto
{
    [Required, StringLength(160, MinimumLength = 2)]
    public string Title { get; set; } = string.Empty;

    [Required, MinLength(5)]
    public string Content { get; set; } = string.Empty;

    [Range(1, 200)]
    public int OrderIndex { get; set; }
}
