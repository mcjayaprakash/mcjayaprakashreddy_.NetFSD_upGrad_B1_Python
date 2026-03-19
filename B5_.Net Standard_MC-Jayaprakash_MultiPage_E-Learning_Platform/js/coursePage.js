document.addEventListener("DOMContentLoaded", function () {

    const container = document.getElementById("courseList");
    const table = document.getElementById("courseTable");

    courses.forEach(course => {

        container.innerHTML += `
        <div class="course-card">
            <h3>${course.title}</h3>
            <ol>
                ${course.lessons.map(l => `<li>${l}</li>`).join("")}
            </ol>
            <button class="complete-btn" data-name="${course.title}">
                Mark Complete
            </button>
        </div>`;

        table.innerHTML += `
        <tr>
            <td>${course.title}</td>
            <td>${course.lessons.join(", ")}</td>
        </tr>`;
    });

    document.querySelectorAll(".complete-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            saveCompleted(this.dataset.name);
            alert("Course Completed!");
        });
    });
});