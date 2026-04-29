using AutoMapper;
using Elearning.Api.DTOs;
using Elearning.Api.Models;

namespace Elearning.Api.Mapping;

public class ElearningProfile : Profile
{
    public ElearningProfile()
    {
        CreateMap<Course, CourseSummaryDto>()
            .ForCtorParam("CreatedByName", opt => opt.MapFrom(src => src.Creator == null ? string.Empty : src.Creator.FullName))
            .ForCtorParam("LessonCount", opt => opt.MapFrom(src => src.Lessons.Count))
            .ForCtorParam("QuizCount", opt => opt.MapFrom(src => src.Quizzes.Count));
        CreateMap<Course, CourseDetailDto>()
            .ForCtorParam("CreatedByName", opt => opt.MapFrom(src => src.Creator == null ? string.Empty : src.Creator.FullName));
        CreateMap<CourseCreateDto, Course>();
        CreateMap<CourseUpdateDto, Course>();

        CreateMap<Lesson, LessonDto>();
        CreateMap<LessonCreateDto, Lesson>();
        CreateMap<LessonUpdateDto, Lesson>();

        CreateMap<Quiz, QuizDto>()
            .ForCtorParam("QuestionCount", opt => opt.MapFrom(src => src.Questions.Count));
        CreateMap<QuizCreateDto, Quiz>();
        CreateMap<Question, QuestionDto>();
        CreateMap<QuestionCreateDto, Question>()
            .ForMember(dest => dest.CorrectAnswer, opt => opt.MapFrom(src => src.CorrectAnswer.ToUpperInvariant()));

        CreateMap<User, UserDto>();
        CreateMap<UserRegisterDto, User>()
            .ForMember(dest => dest.PasswordHash, opt => opt.Ignore());
        CreateMap<UserUpdateDto, User>();

        CreateMap<Result, ResultDto>()
            .ForCtorParam("UserName", opt => opt.MapFrom(src => src.User == null ? string.Empty : src.User.FullName))
            .ForCtorParam("QuizTitle", opt => opt.MapFrom(src => src.Quiz == null ? string.Empty : src.Quiz.Title));
    }
}
