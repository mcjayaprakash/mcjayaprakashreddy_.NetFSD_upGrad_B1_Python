using Elearning.Api.Data;
using Elearning.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace Elearning.Api.Repositories;

public class LessonRepository(ElearningDbContext db) : ILessonRepository
{
    public Task<List<Lesson>> GetByCourseAsync(int courseId) =>
        db.Lessons
            .AsNoTracking()
            .Where(l => l.CourseId == courseId)
            .OrderBy(l => l.OrderIndex)
            .ToListAsync();

    public Task<Lesson?> GetByIdAsync(int id, bool tracking = false)
    {
        var query = db.Lessons.Where(l => l.LessonId == id);
        return (tracking ? query : query.AsNoTracking()).FirstOrDefaultAsync();
    }

    public Task<bool> CourseExistsAsync(int courseId) =>
        db.Courses.AsNoTracking().AnyAsync(c => c.CourseId == courseId);

    public async Task<Lesson> AddAsync(Lesson lesson)
    {
        db.Lessons.Add(lesson);
        await db.SaveChangesAsync();
        return lesson;
    }

    public async Task<bool> UpdateAsync(Lesson lesson)
    {
        db.Lessons.Update(lesson);
        return await db.SaveChangesAsync() > 0;
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var lesson = await db.Lessons.FindAsync(id);
        if (lesson is null)
        {
            return false;
        }

        db.Lessons.Remove(lesson);
        await db.SaveChangesAsync();
        return true;
    }
}
