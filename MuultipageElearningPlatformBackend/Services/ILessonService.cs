using Elearning.Api.DTOs;

namespace Elearning.Api.Services;

public interface ILessonService
{
    Task<ServiceResult<IReadOnlyCollection<LessonDto>>> GetByCourseAsync(int courseId);
    Task<ServiceResult<LessonDto>> CreateAsync(LessonCreateDto dto);
    Task<ServiceResult<LessonDto>> UpdateAsync(int id, LessonUpdateDto dto);
    Task<ServiceResult<bool>> DeleteAsync(int id);
}
