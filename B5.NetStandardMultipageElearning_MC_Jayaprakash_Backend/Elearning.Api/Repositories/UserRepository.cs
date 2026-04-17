using Elearning.Api.Data;
using Elearning.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace Elearning.Api.Repositories;

public class UserRepository(ElearningDbContext db) : IUserRepository
{
    public Task<User?> GetByIdAsync(int id, bool tracking = false)
    {
        var query = db.Users.Where(u => u.UserId == id);
        return (tracking ? query : query.AsNoTracking()).FirstOrDefaultAsync();
    }

    public Task<User?> GetByEmailAsync(string email, bool tracking = false)
    {
        var normalized = email.Trim().ToLowerInvariant();
        var query = db.Users.Where(u => u.Email == normalized);
        return (tracking ? query : query.AsNoTracking()).FirstOrDefaultAsync();
    }

    public Task<bool> EmailExistsAsync(string email, int? excludedUserId = null) =>
        db.Users.AsNoTracking().AnyAsync(u => u.Email == email && (excludedUserId == null || u.UserId != excludedUserId));

    public async Task<User> AddAsync(User user)
    {
        db.Users.Add(user);
        await db.SaveChangesAsync();
        return user;
    }

    public async Task<bool> UpdateAsync(User user)
    {
        db.Users.Update(user);
        return await db.SaveChangesAsync() > 0;
    }
}
