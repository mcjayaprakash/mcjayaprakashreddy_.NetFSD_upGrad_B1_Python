using Elearning.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace Elearning.Api.Data
{
    public class ElearningDbContext : DbContext
    {
        public ElearningDbContext(DbContextOptions<ElearningDbContext> options)
            : base(options)
        {
        }

        public DbSet<User> Users { get; set; }
        public DbSet<Course> Courses { get; set; }
        public DbSet<Lesson> Lessons { get; set; }
        public DbSet<Quiz> Quizzes { get; set; }
        public DbSet<Question> Questions { get; set; }
        public DbSet<Result> Results { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<User>(entity =>
            {
                entity.HasKey(u => u.UserId);
                entity.Property(u => u.FullName).HasColumnType("varchar(120)").IsRequired();
                entity.Property(u => u.Email).HasColumnType("varchar(180)").IsRequired();
                entity.Property(u => u.PasswordHash).HasColumnType("varchar(500)").IsRequired();
                entity.Property(u => u.Role).HasColumnType("varchar(30)").HasDefaultValue("Learner").IsRequired();
                entity.Property(u => u.CreatedAt).HasColumnType("datetime");
                entity.HasIndex(u => u.Email).IsUnique();
            });

            modelBuilder.Entity<Course>(entity =>
            {
                entity.HasKey(c => c.CourseId);
                entity.Property(c => c.Title).HasColumnType("varchar(160)").IsRequired();
                entity.Property(c => c.Description).HasColumnType("varchar(1200)").IsRequired();
                entity.Property(c => c.CreatedAt).HasColumnType("datetime");

                entity.HasOne(c => c.Creator)
                    .WithMany(u => u.Courses)
                    .HasForeignKey(c => c.CreatedBy)
                    .OnDelete(DeleteBehavior.Restrict);
            });

            modelBuilder.Entity<Lesson>(entity =>
            {
                entity.HasKey(l => l.LessonId);
                entity.Property(l => l.Title).HasColumnType("varchar(160)").IsRequired();
                entity.Property(l => l.Content).HasColumnType("varchar(max)").IsRequired();

                entity.HasOne(l => l.Course)
                    .WithMany(c => c.Lessons)
                    .HasForeignKey(l => l.CourseId)
                    .OnDelete(DeleteBehavior.Cascade);
            });

            modelBuilder.Entity<Quiz>(entity =>
            {
                entity.HasKey(q => q.QuizId);
                entity.Property(q => q.Title).HasColumnType("varchar(160)").IsRequired();

                entity.HasOne(q => q.Course)
                    .WithMany(c => c.Quizzes)
                    .HasForeignKey(q => q.CourseId)
                    .OnDelete(DeleteBehavior.Cascade);
            });

            modelBuilder.Entity<Question>(entity =>
            {
                entity.HasKey(q => q.QuestionId);
                entity.Property(q => q.QuestionText).HasColumnType("varchar(600)").IsRequired();
                entity.Property(q => q.OptionA).HasColumnType("varchar(250)").IsRequired();
                entity.Property(q => q.OptionB).HasColumnType("varchar(250)").IsRequired();
                entity.Property(q => q.OptionC).HasColumnType("varchar(250)").IsRequired();
                entity.Property(q => q.OptionD).HasColumnType("varchar(250)").IsRequired();
                entity.Property(q => q.CorrectAnswer).HasColumnType("varchar(1)").IsRequired();

                entity.HasOne(q => q.Quiz)
                    .WithMany(qz => qz.Questions)
                    .HasForeignKey(q => q.QuizId)
                    .OnDelete(DeleteBehavior.Cascade);
            });

            modelBuilder.Entity<Result>(entity =>
            {
                entity.HasKey(r => r.ResultId);
                entity.Property(r => r.AttemptDate).HasColumnType("datetime");

                entity.HasOne(r => r.User)
                    .WithMany(u => u.Results)
                    .HasForeignKey(r => r.UserId)
                    .OnDelete(DeleteBehavior.Cascade);

                entity.HasOne(r => r.Quiz)
                    .WithMany(q => q.Results)
                    .HasForeignKey(r => r.QuizId)
                    .OnDelete(DeleteBehavior.Cascade);
            });
        }
    }
}
