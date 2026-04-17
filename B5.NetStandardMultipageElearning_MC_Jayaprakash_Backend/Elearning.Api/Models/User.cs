using System.ComponentModel.DataAnnotations;

namespace Elearning.Api.Models;

public class User
{
    public int UserId { get; set; }

    [MaxLength(120)]
    public string FullName { get; set; } = string.Empty;

    [MaxLength(180)]
    public string Email { get; set; } = string.Empty;

    [MaxLength(500)]
    public string PasswordHash { get; set; } = string.Empty;

    [MaxLength(30)]
    public string Role { get; set; } = "Learner";

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public ICollection<Course> Courses { get; set; } = new List<Course>();

    public ICollection<Result> Results { get; set; } = new List<Result>();
}
