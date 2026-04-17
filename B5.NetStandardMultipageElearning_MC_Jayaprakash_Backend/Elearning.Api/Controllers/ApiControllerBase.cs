using Elearning.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace Elearning.Api.Controllers;

[ApiController]
public abstract class ApiControllerBase : ControllerBase
{
    protected ActionResult<T> FromServiceResult<T>(ServiceResult<T> result)
    {
        if (result.Success && result.Value is not null)
        {
            return Ok(result.Value);
        }

        return result.ErrorType switch
        {
            ServiceErrorType.NotFound => NotFound(new { message = result.Error }),
            ServiceErrorType.BadRequest => BadRequest(new { message = result.Error }),
            _ => BadRequest(new { message = result.Error ?? "Request failed." })
        };
    }
}
