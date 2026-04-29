using Elearning.Api.Data;
using Elearning.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace Elearning.Api.Repositories;

public class CourseRepository(ElearningDbContext db) : ICourseRepository
{
    public Task<List<Course>> GetAllAsync() =>
        db.Courses
            .AsNoTracking()
            .Include(c => c.Creator)
            .Include(c => c.Lessons)
            .Include(c => c.Quizzes)
            .OrderBy(c => c.Title)
            .ToListAsync();

    public Task<Course?> GetByIdAsync(int id, bool tracking = false)
    {
        var query = db.Courses
            .Include(c => c.Creator)
            .Include(c => c.Lessons.OrderBy(l => l.OrderIndex))
            .Include(c => c.Quizzes)
            .ThenInclude(q => q.Questions)
            .Where(c => c.CourseId == id);

        return (tracking ? query : query.AsNoTracking()).FirstOrDefaultAsync();
    }

    public async Task<Course> AddAsync(Course course)
    {
        db.Courses.Add(course);
        await db.SaveChangesAsync();
        return course;
    }

    public async Task<bool> UpdateAsync(Course course)
    {
        db.Courses.Update(course);
        return await db.SaveChangesAsync() > 0;
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var course = await db.Courses.FindAsync(id);
        if (course is null)
        {
            return false;
        }

        db.Courses.Remove(course);
        await db.SaveChangesAsync();
        return true;
    }

    public Task<bool> CreatorExistsAsync(int userId) =>
        db.Users.AsNoTracking().AnyAsync(u => u.UserId == userId);
}
