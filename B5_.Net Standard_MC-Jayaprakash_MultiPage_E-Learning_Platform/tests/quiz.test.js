function calculatePercentage(score, total) {
    return (score / total) * 100;
}

function isPass(percent) {
    return percent >= 50;
}

function getGrade(percent) {
    if (percent >= 80) return "A";
    else if (percent >= 50) return "B";
    else return "F";
}

test("percentage", () => {
    expect(calculatePercentage(2,2)).toBe(100);
});

test("pass", () => {
    expect(isPass(60)).toBe(true);
});

test("grade", () => {
    expect(getGrade(85)).toBe("A");
});