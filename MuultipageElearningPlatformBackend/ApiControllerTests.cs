using Elearning.Api.Controllers;
using Elearning.Api.DTOs;
using Elearning.Api.Repositories;
using Elearning.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace Elearning.Tests;

public class ApiControllerTests
{
    [Fact]
    public async Task GetCourses_ReturnsOkWithData()
    {
        var (db, _, _, _) = await TestFactory.SeedQuizAsync();
        var service = TestFactory.CreateCourseService(db);
        var controller = new CoursesController(service, new LessonService(new LessonRepository(db), TestFactory.CreateMapper()));

        var response = await controller.GetAll();

        var ok = Assert.IsType<OkObjectResult>(response.Result);
        var data = Assert.IsAssignableFrom<IReadOnlyCollection<CourseSummaryDto>>(ok.Value);
        Assert.Single(data);
    }
}
