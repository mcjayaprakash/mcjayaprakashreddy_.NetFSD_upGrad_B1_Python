using Elearning.Api.DTOs;

namespace Elearning.Api.Services;

public interface IUserService
{
    Task<ServiceResult<UserDto>> RegisterAsync(UserRegisterDto dto);
    Task<ServiceResult<AuthResponseDto>> LoginAsync(UserLoginDto dto);
    Task<ServiceResult<UserDto>> GetByIdAsync(int id);
    Task<ServiceResult<UserDto>> UpdateAsync(int id, UserUpdateDto dto);
    Task<ServiceResult<bool>> ResetPasswordAsync(ResetPasswordDto dto);
}
