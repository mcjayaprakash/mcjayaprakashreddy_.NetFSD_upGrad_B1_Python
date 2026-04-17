using Elearning.Api.Data;
using Elearning.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace Elearning.Api.Repositories;

public class ResultRepository(ElearningDbContext db) : IResultRepository
{
    public async Task<Result> AddAsync(Result result)
    {
        db.Results.Add(result);
        await db.SaveChangesAsync();
        return result;
    }

    public Task<List<Result>> GetByUserAsync(int userId) =>
        db.Results
            .AsNoTracking()
            .Include(r => r.User)
            .Include(r => r.Quiz)
            .Where(r => r.UserId == userId)
            .OrderByDescending(r => r.AttemptDate)
            .ToListAsync();

    public Task<bool> UserExistsAsync(int userId) =>
        db.Users.AsNoTracking().AnyAsync(u => u.UserId == userId);
}
