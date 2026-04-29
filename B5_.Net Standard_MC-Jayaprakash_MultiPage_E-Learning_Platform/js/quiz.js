const quizData = [
    {
        question: "JavaScript is?",
        options: ["Programming Language", "Database", "OS"],
        answer: "Programming Language"
    },
    {
        question: "CSS is used for?",
        options: ["Styling", "Backend", "Database"],
        answer: "Styling"
    },
    {
        question: "HTML is used for?",
        options: ["Styling", "Backend", "Frontend"],
        answer: "Styling"
    }
];

function loadQuiz() {
    return new Promise(resolve => {
        setTimeout(() => resolve(quizData), 1000);
    });
}

async function startQuiz() {
    const data = await loadQuiz();
    const container = document.getElementById("quiz");

    data.forEach((q, index) => {
        const div = document.createElement("div");

        div.innerHTML = `
        <p>${q.question}</p>
        ${q.options.map(opt =>
            `<label>
            <input type="radio" name="q${index}" value="${opt}">
            ${opt}
            </label><br>`
        ).join("")}
        `;

        container.appendChild(div);
    });
}

function submitQuiz() {
    let score = 0;

    quizData.forEach((q, i) => {
        let selected = document.querySelector(`input[name="q${i}"]:checked`);
        if (selected && selected.value === q.answer) score++;
    });

    let percent = (score / quizData.length) * 100;

    saveResult(percent);

    let result = percent >= 50 ? "Pass" : "Fail";

    let feedback;
    switch(true){
        case percent >= 80: feedback = "Excellent"; break;
        case percent >= 50: feedback = "Good"; break;
        default: feedback = "Needs Improvement";
    }

    document.getElementById("result").innerHTML =
        `Score: ${percent}% - ${result} (${feedback})`;
}

document.addEventListener("DOMContentLoaded", startQuiz);

document.getElementById("submitBtn")?.addEventListener("click", submitQuiz);