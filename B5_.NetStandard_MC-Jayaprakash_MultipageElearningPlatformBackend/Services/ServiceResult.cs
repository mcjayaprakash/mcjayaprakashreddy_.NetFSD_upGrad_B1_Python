namespace Elearning.Api.Services;

public class ServiceResult<T>
{
    private ServiceResult(bool success, T? value, string? error, ServiceErrorType errorType)
    {
        Success = success;
        Value = value;
        Error = error;
        ErrorType = errorType;
    }

    public bool Success { get; }
    public T? Value { get; }
    public string? Error { get; }
    public ServiceErrorType ErrorType { get; }

    public static ServiceResult<T> Ok(T value) => new(true, value, null, ServiceErrorType.None);
    public static ServiceResult<T> NotFound(string error) => new(false, default, error, ServiceErrorType.NotFound);
    public static ServiceResult<T> BadRequest(string error) => new(false, default, error, ServiceErrorType.BadRequest);
}

public enum ServiceErrorType
{
    None,
    NotFound,
    BadRequest
}
