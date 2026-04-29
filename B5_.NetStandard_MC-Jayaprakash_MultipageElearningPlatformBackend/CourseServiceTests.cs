using Elearning.Api.DTOs;
using Microsoft.EntityFrameworkCore;

namespace Elearning.Tests;

public class CourseServiceTests
{
    [Fact]
    public async Task CourseCrud_CreatesReadsUpdatesAndDeletesCourse()
    {
        var db = TestFactory.CreateDb();
        var userService = TestFactory.CreateUserService(db);
        var userResult = await userService.RegisterAsync(new UserRegisterDto
        {
            FullName = "Instructor",
            Email = "instructor@test.com",
            Password = "Password@123",
            Role = "Admin"
        });

        var service = TestFactory.CreateCourseService(db);

        var created = await service.CreateAsync(userResult.Value!.UserId, new CourseCreateDto
        {
            Title = "ASP.NET Core",
            Description = "Build REST APIs with .NET 8."
        });

        Assert.True(created.Success);
        Assert.Equal("ASP.NET Core", created.Value!.Title);

        var read = await service.GetByIdAsync(created.Value.CourseId);
        Assert.True(read.Success);

        var updated = await service.UpdateAsync(created.Value.CourseId, new CourseUpdateDto
        {
            Title = "ASP.NET Core 8",
            Description = "Build layered REST APIs with .NET 8."
        });

        Assert.Equal("ASP.NET Core 8", updated.Value!.Title);

        var deleted = await service.DeleteAsync(created.Value.CourseId);
        Assert.True(deleted.Success);

        var missing = await service.GetByIdAsync(created.Value.CourseId);
        Assert.False(missing.Success);
    }

    [Fact]
    public async Task LinqFiltering_ReturnsCoursesOrderedByTitle()
    {
        var (db, user, _, _) = await TestFactory.SeedQuizAsync();
        db.Courses.AddRange(
            new() { Title = "SQL", Description = "Query data.", CreatedBy = user.UserId },
            new() { Title = "Bootstrap", Description = "Build layouts.", CreatedBy = user.UserId });
        await db.SaveChangesAsync();

        var titles = await db.Courses
            .AsNoTracking()
            .Where(course => course.Title.Contains("S"))
            .OrderBy(course => course.Title)
            .Select(course => course.Title)
            .ToListAsync();

        Assert.Equal(["JavaScript Basics", "SQL"], titles);
    }
}
