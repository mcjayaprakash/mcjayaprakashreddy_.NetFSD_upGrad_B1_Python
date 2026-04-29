using Elearning.Api.Models;

namespace Elearning.Api.Repositories;

public interface ICourseRepository
{
    Task<List<Course>> GetAllAsync();
    Task<Course?> GetByIdAsync(int id, bool tracking = false);
    Task<Course> AddAsync(Course course);
    Task<bool> UpdateAsync(Course course);
    Task<bool> DeleteAsync(int id);
    Task<bool> CreatorExistsAsync(int userId);
}
