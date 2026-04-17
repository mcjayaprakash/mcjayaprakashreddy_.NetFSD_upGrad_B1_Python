using Elearning.Api.Models;

namespace Elearning.Api.Security;

public interface ITokenService
{
    string CreateToken(User user);
}

