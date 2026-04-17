using Elearning.Api.DTOs;
using Elearning.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace Elearning.Api.Controllers;

[Route("api/users")]
public class UsersController(IUserService users) : ApiControllerBase
{
    [HttpPost("register")]
    public async Task<ActionResult<UserDto>> Register(UserRegisterDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        var result = await users.RegisterAsync(dto);
        if (!result.Success)
        {
            return FromServiceResult(result);
        }

        return CreatedAtAction(nameof(GetById), new { id = result.Value!.UserId }, result.Value);
    }

    [HttpPost("login")]
    public async Task<ActionResult<AuthResponseDto>> Login(UserLoginDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        return FromServiceResult(await users.LoginAsync(dto));
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<UserDto>> GetById(int id) =>
        FromServiceResult(await users.GetByIdAsync(id));

    [HttpPut("{id:int}")]
    public async Task<ActionResult<UserDto>> Update(int id, UserUpdateDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        return FromServiceResult(await users.UpdateAsync(id, dto));
    }

    [HttpPost("reset-password")]
    public async Task<IActionResult> ResetPassword(ResetPasswordDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        var result = await users.ResetPasswordAsync(dto);
        if (!result.Success)
        {
            return result.ErrorType == ServiceErrorType.NotFound
                ? NotFound(new { message = result.Error })
                : BadRequest(new { message = result.Error });
        }

        return Ok(new { message = "Password reset successfully." });
    }
}
