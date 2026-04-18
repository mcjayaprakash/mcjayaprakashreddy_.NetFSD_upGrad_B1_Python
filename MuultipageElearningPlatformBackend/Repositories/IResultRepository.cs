using Elearning.Api.Models;

namespace Elearning.Api.Repositories;

public interface IResultRepository
{
    Task<Result> AddAsync(Result result);
    Task<List<Result>> GetByUserAsync(int userId);
    Task<bool> UserExistsAsync(int userId);
}
