using Elearning.Api.DTOs;
using Elearning.Api.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Elearning.Api.Controllers;

[Route("api/lessons")]
public class LessonsController(ILessonService lessons) : ApiControllerBase
{
    [HttpPost]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<LessonDto>> Create(LessonCreateDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        var result = await lessons.CreateAsync(dto);
        if (!result.Success)
        {
            return FromServiceResult(result);
        }

        return CreatedAtAction(nameof(Create), new { id = result.Value!.LessonId }, result.Value);
    }

    [HttpPut("{id:int}")]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<LessonDto>> Update(int id, LessonUpdateDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        return FromServiceResult(await lessons.UpdateAsync(id, dto));
    }

    [HttpDelete("{id:int}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> Delete(int id)
    {
        var result = await lessons.DeleteAsync(id);
        if (!result.Success)
        {
            return NotFound(new { message = result.Error });
        }

        return Ok(new { message = "Lesson deleted." });
    }
}
