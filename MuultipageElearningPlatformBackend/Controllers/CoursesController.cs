using Elearning.Api.DTOs;
using Elearning.Api.Security;
using Elearning.Api.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Elearning.Api.Controllers;

[Route("api/courses")]
public class CoursesController(ICourseService courses, ILessonService lessons) : ApiControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IReadOnlyCollection<CourseSummaryDto>>> GetAll()
    {
        var data = await courses.GetAllAsync();
        return Ok(data);
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<CourseDetailDto>> GetById(int id) =>
        FromServiceResult(await courses.GetByIdAsync(id));

    [HttpPost]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<CourseDetailDto>> Create(CourseCreateDto dto)
    {
        var userId = User.GetUserId();
        if (userId is null)
        {
            return Unauthorized(new { message = "Missing user identity." });
        }

        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        var result = await courses.CreateAsync(userId.Value, dto);
        if (!result.Success)
        {
            return FromServiceResult(result);
        }

        return CreatedAtAction(nameof(GetById), new { id = result.Value!.CourseId }, result.Value);
    }

    [HttpPut("{id:int}")]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<CourseDetailDto>> Update(int id, CourseUpdateDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        return FromServiceResult(await courses.UpdateAsync(id, dto));
    }

    [HttpDelete("{id:int}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> Delete(int id)
    {
        var result = await courses.DeleteAsync(id);
        if (!result.Success)
        {
            return result.ErrorType == ServiceErrorType.NotFound
                ? NotFound(new { message = result.Error })
                : BadRequest(new { message = result.Error });
        }

        return Ok(new { message = "Course deleted." });
    }

    [HttpGet("{courseId:int}/lessons")]
    public async Task<ActionResult<IReadOnlyCollection<LessonDto>>> GetLessons(int courseId) =>
        FromServiceResult(await lessons.GetByCourseAsync(courseId));
}
