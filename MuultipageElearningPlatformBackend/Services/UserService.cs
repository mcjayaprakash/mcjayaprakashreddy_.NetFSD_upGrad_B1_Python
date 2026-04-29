using AutoMapper;
using Elearning.Api.DTOs;
using Elearning.Api.Models;
using Elearning.Api.Repositories;
using Elearning.Api.Security;

namespace Elearning.Api.Services;

public class UserService(IUserRepository users, IPasswordHasher hasher, ITokenService tokens, IMapper mapper) : IUserService
{
    private static string NormalizeRole(string role) =>
        string.Equals(role?.Trim(), "Admin", StringComparison.OrdinalIgnoreCase) ? "Admin" : "Learner";

    public async Task<ServiceResult<UserDto>> RegisterAsync(UserRegisterDto dto)
    {
        var email = dto.Email.Trim().ToLowerInvariant();
        if (await users.EmailExistsAsync(email))
        {
            return ServiceResult<UserDto>.BadRequest("Email is already registered.");
        }

        var user = mapper.Map<User>(dto);
        user.Email = email;
        user.PasswordHash = hasher.Hash(dto.Password);
        user.Role = NormalizeRole(dto.Role);
        user.CreatedAt = DateTime.UtcNow;
        await users.AddAsync(user);

        return ServiceResult<UserDto>.Ok(mapper.Map<UserDto>(user));
    }

    public async Task<ServiceResult<AuthResponseDto>> LoginAsync(UserLoginDto dto)
    {
        var user = await users.GetByEmailAsync(dto.Email);
        if (user is null || !hasher.Verify(dto.Password, user.PasswordHash))
        {
            return ServiceResult<AuthResponseDto>.BadRequest("Invalid email or password.");
        }

        var requestedRole = NormalizeRole(dto.Role);
        if (!string.Equals(user.Role, requestedRole, StringComparison.OrdinalIgnoreCase))
        {
            return ServiceResult<AuthResponseDto>.BadRequest("Selected role does not match this account.");
        }

        var token = tokens.CreateToken(user);
        return ServiceResult<AuthResponseDto>.Ok(new AuthResponseDto(token, mapper.Map<UserDto>(user)));
    }

    public async Task<ServiceResult<UserDto>> GetByIdAsync(int id)
    {
        var user = await users.GetByIdAsync(id);
        return user is null
            ? ServiceResult<UserDto>.NotFound("User not found.")
            : ServiceResult<UserDto>.Ok(mapper.Map<UserDto>(user));
    }

    public async Task<ServiceResult<UserDto>> UpdateAsync(int id, UserUpdateDto dto)
    {
        var user = await users.GetByIdAsync(id, tracking: true);
        if (user is null)
        {
            return ServiceResult<UserDto>.NotFound("User not found.");
        }

        var email = dto.Email.Trim().ToLowerInvariant();
        if (await users.EmailExistsAsync(email, id))
        {
            return ServiceResult<UserDto>.BadRequest("Email is already registered.");
        }

        user.FullName = dto.FullName;
        user.Email = email;
        await users.UpdateAsync(user);
        return ServiceResult<UserDto>.Ok(mapper.Map<UserDto>(user));
    }

    public async Task<ServiceResult<bool>> ResetPasswordAsync(ResetPasswordDto dto)
    {
        var email = dto.Email.Trim().ToLowerInvariant();
        var requestedRole = NormalizeRole(dto.Role);
        var user = await users.GetByEmailAsync(email, tracking: true);

        if (user is null)
        {
            return ServiceResult<bool>.NotFound("User account was not found.");
        }

        if (!string.Equals(user.Role, requestedRole, StringComparison.OrdinalIgnoreCase))
        {
            return ServiceResult<bool>.BadRequest("Selected role does not match this account.");
        }

        user.PasswordHash = hasher.Hash(dto.NewPassword);
        await users.UpdateAsync(user);
        return ServiceResult<bool>.Ok(true);
    }
}
