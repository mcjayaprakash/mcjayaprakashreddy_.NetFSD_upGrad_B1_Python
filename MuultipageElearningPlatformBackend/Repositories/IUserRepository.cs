using Elearning.Api.Models;

namespace Elearning.Api.Repositories;

public interface IUserRepository
{
    Task<User?> GetByIdAsync(int id, bool tracking = false);
    Task<User?> GetByEmailAsync(string email, bool tracking = false);
    Task<bool> EmailExistsAsync(string email, int? excludedUserId = null);
    Task<User> AddAsync(User user);
    Task<bool> UpdateAsync(User user);
}
