using Elearning.Api.DTOs;

namespace Elearning.Api.Services;

public interface IResultService
{
    Task<ServiceResult<IReadOnlyCollection<ResultDto>>> GetByUserAsync(int userId);
}
