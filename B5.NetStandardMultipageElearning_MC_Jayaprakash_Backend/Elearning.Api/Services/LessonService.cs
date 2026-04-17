using AutoMapper;
using Elearning.Api.DTOs;
using Elearning.Api.Models;
using Elearning.Api.Repositories;

namespace Elearning.Api.Services;

public class LessonService(ILessonRepository lessons, IMapper mapper) : ILessonService
{
    public async Task<ServiceResult<IReadOnlyCollection<LessonDto>>> GetByCourseAsync(int courseId)
    {
        if (!await lessons.CourseExistsAsync(courseId))
        {
            return ServiceResult<IReadOnlyCollection<LessonDto>>.NotFound("Course not found.");
        }

        return ServiceResult<IReadOnlyCollection<LessonDto>>.Ok(mapper.Map<List<LessonDto>>(await lessons.GetByCourseAsync(courseId)));
    }

    public async Task<ServiceResult<LessonDto>> CreateAsync(LessonCreateDto dto)
    {
        if (!await lessons.CourseExistsAsync(dto.CourseId))
        {
            return ServiceResult<LessonDto>.BadRequest("Course does not exist.");
        }

        var lesson = mapper.Map<Lesson>(dto);
        await lessons.AddAsync(lesson);
        return ServiceResult<LessonDto>.Ok(mapper.Map<LessonDto>(lesson));
    }

    public async Task<ServiceResult<LessonDto>> UpdateAsync(int id, LessonUpdateDto dto)
    {
        var lesson = await lessons.GetByIdAsync(id, tracking: true);
        if (lesson is null)
        {
            return ServiceResult<LessonDto>.NotFound("Lesson not found.");
        }

        mapper.Map(dto, lesson);
        await lessons.UpdateAsync(lesson);
        return ServiceResult<LessonDto>.Ok(mapper.Map<LessonDto>(lesson));
    }

    public async Task<ServiceResult<bool>> DeleteAsync(int id)
    {
        var deleted = await lessons.DeleteAsync(id);
        return deleted
            ? ServiceResult<bool>.Ok(true)
            : ServiceResult<bool>.NotFound("Lesson not found.");
    }
}
