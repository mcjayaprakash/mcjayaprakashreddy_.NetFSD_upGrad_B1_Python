using AutoMapper;
using Elearning.Api.DTOs;
using Elearning.Api.Models;
using Elearning.Api.Repositories;

namespace Elearning.Api.Services;

public class CourseService(ICourseRepository courses, IMapper mapper) : ICourseService
{
    public async Task<IReadOnlyCollection<CourseSummaryDto>> GetAllAsync() =>
        mapper.Map<List<CourseSummaryDto>>(await courses.GetAllAsync());

    public async Task<ServiceResult<CourseDetailDto>> GetByIdAsync(int id)
    {
        var course = await courses.GetByIdAsync(id);
        return course is null
            ? ServiceResult<CourseDetailDto>.NotFound("Course not found.")
            : ServiceResult<CourseDetailDto>.Ok(mapper.Map<CourseDetailDto>(course));
    }

    public async Task<ServiceResult<CourseDetailDto>> CreateAsync(int createdByUserId, CourseCreateDto dto)
    {
        if (!await courses.CreatorExistsAsync(createdByUserId))
        {
            return ServiceResult<CourseDetailDto>.BadRequest("CreatedBy user does not exist.");
        }

        var course = mapper.Map<Course>(dto);
        course.CreatedBy = createdByUserId;
        course.CreatedAt = DateTime.UtcNow;
        await courses.AddAsync(course);

        var saved = await courses.GetByIdAsync(course.CourseId);
        return ServiceResult<CourseDetailDto>.Ok(mapper.Map<CourseDetailDto>(saved));
    }

    public async Task<ServiceResult<CourseDetailDto>> UpdateAsync(int id, CourseUpdateDto dto)
    {
        var course = await courses.GetByIdAsync(id, tracking: true);
        if (course is null)
        {
            return ServiceResult<CourseDetailDto>.NotFound("Course not found.");
        }

        mapper.Map(dto, course);
        await courses.UpdateAsync(course);
        var saved = await courses.GetByIdAsync(id);
        return ServiceResult<CourseDetailDto>.Ok(mapper.Map<CourseDetailDto>(saved));
    }

    public async Task<ServiceResult<bool>> DeleteAsync(int id)
    {
        var deleted = await courses.DeleteAsync(id);
        return deleted
            ? ServiceResult<bool>.Ok(true)
            : ServiceResult<bool>.NotFound("Course not found.");
    }
}
