using AutoMapper;
using Elearning.Api.DTOs;
using Elearning.Api.Repositories;

namespace Elearning.Api.Services;

public class ResultService(IResultRepository results, IMapper mapper) : IResultService
{
    public async Task<ServiceResult<IReadOnlyCollection<ResultDto>>> GetByUserAsync(int userId)
    {
        if (!await results.UserExistsAsync(userId))
        {
            return ServiceResult<IReadOnlyCollection<ResultDto>>.NotFound("User not found.");
        }

        return ServiceResult<IReadOnlyCollection<ResultDto>>.Ok(mapper.Map<List<ResultDto>>(await results.GetByUserAsync(userId)));
    }
}
