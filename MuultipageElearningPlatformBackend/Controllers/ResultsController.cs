using Elearning.Api.DTOs;
using Elearning.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace Elearning.Api.Controllers;

[Route("api/results")]
public class ResultsController(IResultService results) : ApiControllerBase
{
    [HttpGet("{userId:int}")]
    public async Task<ActionResult<IReadOnlyCollection<ResultDto>>> GetByUser(int userId) =>
        FromServiceResult(await results.GetByUserAsync(userId));
}
