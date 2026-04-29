using Elearning.Api.DTOs;

namespace Elearning.Api.Services;

public interface ICourseService
{
    Task<IReadOnlyCollection<CourseSummaryDto>> GetAllAsync();
    Task<ServiceResult<CourseDetailDto>> GetByIdAsync(int id);
    Task<ServiceResult<CourseDetailDto>> CreateAsync(int createdByUserId, CourseCreateDto dto);
    Task<ServiceResult<CourseDetailDto>> UpdateAsync(int id, CourseUpdateDto dto);
    Task<ServiceResult<bool>> DeleteAsync(int id);
}
