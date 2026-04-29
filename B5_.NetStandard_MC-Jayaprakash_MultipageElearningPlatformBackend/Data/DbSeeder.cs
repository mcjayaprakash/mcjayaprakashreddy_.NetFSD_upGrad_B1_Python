using Elearning.Api.Models;
using Elearning.Api.Security;
using Microsoft.EntityFrameworkCore;

namespace Elearning.Api.Data;

public static class DbSeeder
{
    public static async Task SeedAsync(IServiceProvider services)
    {
        var db = services.GetRequiredService<ElearningDbContext>();
        var hasher = services.GetRequiredService<IPasswordHasher>();

        if (db.Database.IsRelational())
        {
            await db.Database.MigrateAsync();
        }
        else
        {
            await db.Database.EnsureCreatedAsync();
        }

        var learner = await db.Users.FirstOrDefaultAsync(u => u.Email == "jp@gmail.com");
        if (learner is null)
        {
            learner = new User
            {
                FullName = "Jayaprakash",
                Email = "jp@gmail.com",
                PasswordHash = hasher.Hash("Password@123"),
                Role = "Learner",
                CreatedAt = DateTime.UtcNow
            };

            db.Users.Add(learner);
            await db.SaveChangesAsync();
        }
        else if (!string.Equals(learner.Role, "Learner", StringComparison.OrdinalIgnoreCase))
        {
            learner.Role = "Learner";
            await db.SaveChangesAsync();
        }

        var instructor = await db.Users.FirstOrDefaultAsync(u => u.Email == "admin@learnify.com");
        if (instructor is null)
        {
            instructor = new User
            {
                FullName = "Admin Manager",
                Email = "admin@learnify.com",
                PasswordHash = hasher.Hash("Admin@123"),
                Role = "Admin",
                CreatedAt = DateTime.UtcNow
            };

            db.Users.Add(instructor);
            await db.SaveChangesAsync();
        }
        else if (!string.Equals(instructor.Role, "Admin", StringComparison.OrdinalIgnoreCase))
        {
            instructor.Role = "Admin";
            await db.SaveChangesAsync();
        }

        if (!await db.Courses.AnyAsync())
        {
            var courses = new List<Course>
            {
                CreateCourse("HTML & CSS", "Build semantic pages, forms, flexbox layouts and responsive grids.", instructor.UserId, ["HTML Tags", "Forms", "Flexbox", "Grid"]),
                CreateCourse("Bootstrap", "Create responsive production screens using Bootstrap grid, components, cards and navbars.", instructor.UserId, ["Grid System", "Components", "Cards", "Navbar"]),
                CreateCourse("JavaScript Basics", "Learn variables, functions, DOM updates and browser events.", instructor.UserId, ["Variables", "Functions", "DOM", "Events"]),
                CreateCourse("Java", "Understand data types, OOP, collections and multithreading fundamentals.", instructor.UserId, ["Data Types", "OOPS", "Collections", "Multithreading"]),
                CreateCourse("SQL", "Practice SQL statements, joins, subqueries and normalization.", instructor.UserId, ["SQL Statements", "Subqueries", "Joins", "Normalisation"]),
                CreateCourse(".NET 8 Web API", "Build REST APIs with ASP.NET Core, EF Core, DTOs and layered architecture.", instructor.UserId, ["Controllers", "EF Core", "DTOs", "Services"])
            };

            db.Courses.AddRange(courses);
            await db.SaveChangesAsync();
        }

        await SeedMissingQuizzesAsync(db);

        await db.SaveChangesAsync();
    }

    private static async Task SeedMissingQuizzesAsync(ElearningDbContext db)
    {
        var courses = await db.Courses
            .Include(course => course.Quizzes)
            .ThenInclude(quiz => quiz.Questions)
            .ToListAsync();

        foreach (var course in courses)
        {
            var quiz = course.Quizzes.FirstOrDefault();
            if (quiz is null)
            {
                quiz = new Quiz { CourseId = course.CourseId, Title = $"{course.Title} Quiz" };
                db.Quizzes.Add(quiz);
                await db.SaveChangesAsync();
            }

            var expectedQuestions = GetSeedQuestions(course.Title, quiz.QuizId).ToList();
            var expectedTexts = expectedQuestions
                .Select(question => question.QuestionText)
                .ToHashSet(StringComparer.OrdinalIgnoreCase);
            var staleQuestions = quiz.Questions
                .Where(question => !expectedTexts.Contains(question.QuestionText))
                .ToList();

            if (staleQuestions.Count > 0)
            {
                db.Questions.RemoveRange(staleQuestions);
                await db.SaveChangesAsync();
                quiz = await db.Quizzes
                    .Include(q => q.Questions)
                    .FirstAsync(q => q.QuizId == quiz.QuizId);
            }

            var existingQuestions = quiz.Questions
                .Select(question => question.QuestionText)
                .ToHashSet(StringComparer.OrdinalIgnoreCase);
            var missingQuestions = expectedQuestions
                .Where(question => !existingQuestions.Contains(question.QuestionText))
                .ToList();

            if (missingQuestions.Count > 0)
            {
                db.Questions.AddRange(missingQuestions);
            }
        }
    }

    private static Course CreateCourse(string title, string description, int userId, string[] lessons)
    {
        var course = new Course
        {
            Title = title,
            Description = description,
            CreatedBy = userId,
            CreatedAt = DateTime.UtcNow
        };

        for (var index = 0; index < lessons.Length; index++)
        {
            course.Lessons.Add(new Lesson
            {
                Title = lessons[index],
                Content = $"Complete the {lessons[index]} lesson and mark progress in the course dashboard.",
                OrderIndex = index + 1
            });
        }

        return course;
    }

    private static Question Question(int quizId, string text, string a, string b, string c, string d, string answer) =>
        new()
        {
            QuizId = quizId,
            QuestionText = text,
            OptionA = a,
            OptionB = b,
            OptionC = c,
            OptionD = d,
            CorrectAnswer = answer
        };

    private static IEnumerable<Question> GetSeedQuestions(string courseTitle, int quizId)
    {
        return courseTitle switch
        {
            "HTML & CSS" => [
                Question(quizId, "What is the main purpose of HTML in web development?", "To define the structure of a webpage", "To connect a database", "To compile JavaScript", "To store API tokens", "A"),
                Question(quizId, "Which CSS feature is used to create one-dimensional layouts?", "Flexbox", "Grid Template Areas", "Media Query", "Box Shadow", "A"),
                Question(quizId, "Which HTML tag creates a hyperlink?", "<a>", "<link>", "<nav>", "<button>", "A"),
                Question(quizId, "Which CSS property changes the text color?", "color", "font-style", "background-color", "text-transform", "A"),
                Question(quizId, "Which HTML element stores metadata such as title and charset?", "<head>", "<header>", "<main>", "<section>", "A"),
                Question(quizId, "Which CSS layout system is best for arranging content in rows and columns?", "CSS Grid", "Inline Block", "Position Absolute", "Float Only", "A"),
                Question(quizId, "Which CSS unit is relative to the root element font size?", "rem", "px", "%", "vh", "A"),
                Question(quizId, "Which HTML attribute provides alternate text for an image?", "alt", "title", "src", "target", "A"),
                Question(quizId, "Which CSS selector targets an element with class='card'?", ".card", "#card", "card", "*card", "A"),
                Question(quizId, "What is the main goal of responsive web design?", "To adapt layouts to different screen sizes", "To make SQL queries faster", "To disable CSS on mobile", "To replace HTML forms", "A")
            ],
            "Bootstrap" => [
                Question(quizId, "What is Bootstrap mainly used for?", "Building responsive user interfaces quickly", "Writing database queries", "Managing Java threads", "Hosting backend APIs", "A"),
                Question(quizId, "Which Bootstrap class is used to create a card component?", ".card", ".panel", ".box", ".content-wrap", "A"),
                Question(quizId, "Bootstrap's layout system is built around which concept?", "A 12-column grid", "XML nodes", "Database tables", "Package namespaces", "A"),
                Question(quizId, "Which Bootstrap class styles a blue primary button?", ".btn-primary", ".button-main", ".primary-color", ".btn-default", "A"),
                Question(quizId, "Which Bootstrap component is commonly used for top navigation?", "Navbar", "Carousel", "Badge", "Toast", "A"),
                Question(quizId, "Which Bootstrap class is commonly used to wrap page content with responsive spacing?", ".container", ".wrapper-fluid", ".page-box", ".content-grid", "A"),
                Question(quizId, "Which class makes an image responsive in Bootstrap?", ".img-fluid", ".img-responsive", ".image-fit", ".photo-scale", "A"),
                Question(quizId, "Which Bootstrap utility classes control margin and padding?", "Spacing utilities like m-* and p-*", "Color utilities only", "Border utilities only", "Display utilities only", "A"),
                Question(quizId, "Which Bootstrap class centers text?", ".text-center", ".align-center", ".center-text", ".font-center", "A"),
                Question(quizId, "What are Bootstrap modals primarily used for?", "Displaying dialog windows and popups", "Rendering SQL data", "Compiling Sass files", "Loading API routes", "A")
            ],
            "JavaScript Basics" => [
                Question(quizId, "Why is JavaScript used in the browser?", "To add interactivity to web pages", "To define HTML structure", "To replace CSS styling", "To create SQL tables", "A"),
                Question(quizId, "Which browser API lets you select and update page elements?", "DOM", "SMTP", "FTP", "DNS", "A"),
                Question(quizId, "Which keyword declares a block-scoped variable in JavaScript?", "let", "var", "static", "constvar", "A"),
                Question(quizId, "Which method attaches an event handler to an element?", "addEventListener", "onBind", "attachHandler", "listenToEvent", "A"),
                Question(quizId, "Which value represents an intentional absence of an object value?", "null", "false", "0", "NaN", "A"),
                Question(quizId, "Which format is commonly used when sending data in web APIs?", "JSON", "PNG", "PDF", "ZIP", "A"),
                Question(quizId, "Which keyword is used to define a function?", "function", "method", "define", "fun", "A"),
                Question(quizId, "Which operator checks both value and data type?", "===", "==", "=", "!=", "A"),
                Question(quizId, "Which browser storage keeps key-value pairs even after closing the tab?", "localStorage", "sessionEvents", "cookieJarOnly", "domCache", "A"),
                Question(quizId, "Which method converts JSON text into a JavaScript object?", "JSON.parse", "JSON.stringify", "Object.parse", "Array.from", "A")
            ],
            "Java" => [
                Question(quizId, "Why is Java called platform independent?", "Because compiled bytecode runs on the JVM", "Because it only runs in browsers", "Because it requires no compiler", "Because it uses only HTML", "A"),
                Question(quizId, "Which Java concept bundles data and methods together?", "Class", "Interface file", "CSS rule", "SQL view", "A"),
                Question(quizId, "Which toolkit includes the Java compiler and runtime tools?", "JDK", "JRE only", "JVM only", "JUnit", "A"),
                Question(quizId, "Which method is the entry point of a Java application?", "main", "start", "run", "init", "A"),
                Question(quizId, "What allows one Java class to acquire properties from another class?", "Inheritance", "Encapsulation", "Overloading", "Abstraction", "A"),
                Question(quizId, "Which Java collection does not allow duplicate values?", "Set", "List", "ArrayList", "Queue", "A"),
                Question(quizId, "Which keyword is used to create a new object in Java?", "new", "create", "class", "make", "A"),
                Question(quizId, "Which Java type stores true or false?", "boolean", "int", "String", "double", "A"),
                Question(quizId, "Which statement structure is used to handle exceptions in Java?", "try-catch", "if-else", "switch-case", "for-each", "A"),
                Question(quizId, "What is the purpose of multithreading in Java?", "To run multiple tasks concurrently", "To style desktop windows", "To create HTML forms", "To write SQL joins", "A")
            ],
            "SQL" => [
                Question(quizId, "What is SQL primarily used for?", "Managing and querying relational databases", "Styling webpages", "Running Java programs", "Editing images", "A"),
                Question(quizId, "Which SQL clause is used to filter rows?", "WHERE", "ORDER BY", "GROUP BY", "FROM", "A"),
                Question(quizId, "Which SQL keyword combines rows from related tables?", "JOIN", "MERGE", "UNION ONLY", "LINK", "A"),
                Question(quizId, "Which SQL command retrieves data from a table?", "SELECT", "INSERT", "UPDATE", "DELETE", "A"),
                Question(quizId, "Which SQL command adds a new row into a table?", "INSERT", "CREATE", "SELECT", "ALTER", "A"),
                Question(quizId, "Which aggregate function returns the number of rows?", "COUNT", "SUM", "AVG", "MAX", "A"),
                Question(quizId, "Which clause groups rows that share the same values?", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "A"),
                Question(quizId, "Which key uniquely identifies each row in a table?", "Primary key", "Foreign key", "Unique index", "Join key", "A"),
                Question(quizId, "What is the purpose of normalization in database design?", "To reduce data redundancy", "To increase font size", "To build UI components", "To speed up CSS rendering", "A"),
                Question(quizId, "Which clause sorts query results?", "ORDER BY", "WHERE", "GROUP BY", "HAVING", "A")
            ],
            ".NET 8 Web API" => [
                Question(quizId, "What format does an ASP.NET Core Web API commonly return?", "JSON", "CSS", "PNG", "MP4", "A"),
                Question(quizId, "What is Entity Framework Core mainly used for?", "Data access and ORM mapping", "Building HTML layouts", "Managing browser storage", "Creating animations", "A"),
                Question(quizId, "Why are DTOs used in Web API projects?", "To shape request and response data", "To compress image files", "To host controllers", "To replace models in the database", "A"),
                Question(quizId, "Which attribute is used on an action to mark a GET endpoint?", "HttpGet", "RouteGet", "GetApi", "FromGet", "A"),
                Question(quizId, "Which framework maps C# models to database tables in many .NET projects?", "Entity Framework Core", "Bootstrap", "SignalR", "Serilog", "A"),
                Question(quizId, "Which file usually stores connection strings in an ASP.NET Core app?", "appsettings.json", "index.html", "site.css", "launch.json", "A"),
                Question(quizId, "Which pattern is commonly used to provide services to controllers?", "Dependency injection", "Method chaining", "CSS inheritance", "Static rendering", "A"),
                Question(quizId, "Which HTTP status code means 'Not Found'?", "404", "200", "201", "500", "A"),
                Question(quizId, "Which HTTP method is typically used to create a new resource?", "POST", "GET", "DELETE", "PATCH", "A"),
                Question(quizId, "What is Swagger commonly used for in Web API development?", "Viewing and testing API documentation", "Styling controllers", "Storing login sessions", "Compiling migrations", "A")
            ],
            _ => [
                Question(quizId, "What should learners do before taking a quiz?", "Complete the course", "Skip all lessons", "Delete progress", "Logout first", "A"),
                Question(quizId, "A quiz is used to check?", "Understanding", "Screen brightness", "Internet speed", "Keyboard color", "A"),
                Question(quizId, "Good learning progress requires?", "Practice", "Guessing only", "Ignoring lessons", "No review", "A"),
                Question(quizId, "What helps learners improve after a low score?", "Reviewing lessons and trying again", "Deleting the course", "Skipping the next quiz", "Avoiding feedback", "A"),
                Question(quizId, "Why should every question be answered before submission?", "To get an accurate result", "To change the course title", "To unlock admin access", "To reset the timer", "A"),
                Question(quizId, "What is a quiz result useful for?", "Measuring understanding", "Changing screen brightness", "Updating passwords", "Formatting CSS", "A"),
                Question(quizId, "Which habit supports better learning outcomes?", "Regular practice", "Guessing answers only", "Ignoring lessons", "Skipping reviews", "A"),
                Question(quizId, "What should learners do after completing a course?", "Attempt the related quiz", "Delete their profile", "Disable progress", "Clear browser storage", "A"),
                Question(quizId, "Why is progress tracking helpful?", "It shows what has been completed", "It removes lessons", "It changes quiz answers", "It disables login", "A"),
                Question(quizId, "What is the goal of an e-learning quiz?", "To assess learning", "To edit videos", "To create databases", "To host images", "A")
            ]
        };
    }
}
