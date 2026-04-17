document.addEventListener("DOMContentLoaded", function () {

    saveUser();

    const container = document.getElementById("dashboard");

    const completed = getCompleted();
    const total = courses.length;

    const percent = (completed.length / total) * 100;

    container.innerHTML = `
        <div class="card">
            <h3>Total Courses</h3>
            <p>${total}</p>
        </div>

        <div class="card">
            <h3>Completed Courses</h3>
            <p>${completed.length}</p>
        </div>

        <div class="card">
            <h3>Overall Progress</h3>
            <progress value="${percent}" max="100"></progress>
            <p>${percent.toFixed(0)}%</p>
        </div>
    `;

    courses.forEach(course => {
        container.innerHTML += `
        <div class="card">
            <h3>${course.title}</h3>
            <progress value="${course.progress}" max="100"></progress>
            <p>${course.progress}%</p>
        </div>`;
    });
});