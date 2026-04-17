document.addEventListener("DOMContentLoaded", function () {

    let user = getUser();


    document.getElementById("name").innerText = user.name;
    document.getElementById("email").innerText = user.email;

    document.getElementById("score").innerText = getResult();

    const completed = getCompleted();
    const list = document.getElementById("completed");

    completed.forEach(c => {
        const li = document.createElement("li");
        li.innerText = c;
        list.appendChild(li);
    });

});