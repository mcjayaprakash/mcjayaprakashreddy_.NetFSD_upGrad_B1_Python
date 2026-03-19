function saveUser() {
    if (!localStorage.getItem("user")) {
        const user = {
            name: "Jayaprakash",
            email: "jp@gmail.com"
        };
        localStorage.setItem("user", JSON.stringify(user));
    }
}

function getUser() {
    return JSON.parse(localStorage.getItem("user"));
}

function saveResult(score) {
    localStorage.setItem("quizScore", score);
}

function getResult() {
    return localStorage.getItem("quizScore") || 0;
}

function saveCompleted(course) {
    let completed = JSON.parse(localStorage.getItem("completed")) || [];

    if (!completed.includes(course)) {
        completed.push(course);
        localStorage.setItem("completed", JSON.stringify(completed));
    }
}

function getCompleted() {
    return JSON.parse(localStorage.getItem("completed")) || [];
}