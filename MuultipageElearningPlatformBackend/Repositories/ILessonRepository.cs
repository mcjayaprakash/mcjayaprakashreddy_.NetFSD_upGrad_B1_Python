using Elearning.Api.Models;

namespace Elearning.Api.Repositories;

public interface ILessonRepository
{
    Task<List<Lesson>> GetByCourseAsync(int courseId);
    Task<Lesson?> GetByIdAsync(int id, bool tracking = false);
    Task<bool> CourseExistsAsync(int courseId);
    Task<Lesson> AddAsync(Lesson lesson);
    Task<bool> UpdateAsync(Lesson lesson);
    Task<bool> DeleteAsync(int id);
}
