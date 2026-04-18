using System.ComponentModel.DataAnnotations;

namespace Elearning.Api.DTOs;

public record UserDto(int UserId, string FullName, string Email, string Role, DateTime CreatedAt);

public record AuthResponseDto(string Token, UserDto User);

public class UserLoginDto
{
    [Required, EmailAddress, StringLength(180)]
    public string Email { get; set; } = string.Empty;

    [Required, StringLength(100, MinimumLength = 8)]
    public string Password { get; set; } = string.Empty;

    [Required, RegularExpression("^(Learner|Admin)$", ErrorMessage = "Role must be Learner or Admin.")]
    public string Role { get; set; } = "Learner";
}

public class UserRegisterDto
{
    [Required, StringLength(120, MinimumLength = 2)]
    public string FullName { get; set; } = string.Empty;

    [Required, EmailAddress, StringLength(180)]
    public string Email { get; set; } = string.Empty;

    [Required, StringLength(100, MinimumLength = 8)]
    public string Password { get; set; } = string.Empty;

    [Required, RegularExpression("^(Learner|Admin)$", ErrorMessage = "Role must be Learner or Admin.")]
    public string Role { get; set; } = "Learner";
}

public class UserUpdateDto
{
    [Required, StringLength(120, MinimumLength = 2)]
    public string FullName { get; set; } = string.Empty;

    [Required, EmailAddress, StringLength(180)]
    public string Email { get; set; } = string.Empty;
}

public class ResetPasswordDto
{
    [Required, EmailAddress, StringLength(180)]
    public string Email { get; set; } = string.Empty;

    [Required, StringLength(100, MinimumLength = 8)]
    public string NewPassword { get; set; } = string.Empty;

    [Required, RegularExpression("^(Learner|Admin)$", ErrorMessage = "Role must be Learner or Admin.")]
    public string Role { get; set; } = "Learner";
}
