namespace Elearning.Api.DTOs;

public record ResultDto(
    int ResultId,
    int UserId,
    string UserName,
    int QuizId,
    string QuizTitle,
    int Score,
    DateTime AttemptDate);
