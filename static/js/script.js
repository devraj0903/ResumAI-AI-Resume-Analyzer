document.addEventListener("DOMContentLoaded", function () {

    // Get HTML elements
    const resumeInput = document.querySelector('input[name="resume"]');
    const jobDescription = document.querySelector('textarea[name="job_description"]');
    const form = document.querySelector("form");
    const submitButton = document.querySelector('button[type="submit"]');

    // ===== PDF UPLOAD =====

    const fileMessage = document.createElement("p");

    fileMessage.style.color = "#754B5A";
    fileMessage.style.fontSize = "13px";
    fileMessage.style.marginTop = "8px";

    resumeInput.after(fileMessage);

    resumeInput.addEventListener("change", function () {

        const file = resumeInput.files[0];

        if (file) {

            if (!file.name.toLowerCase().endsWith(".pdf")) {
                fileMessage.textContent = "Please upload a PDF file.";
                resumeInput.value = "";
                return;
            }

            fileMessage.textContent = "✓ " + file.name;
        } else {
            fileMessage.textContent = "";
        }
    });

    const counter = document.createElement("p");

    counter.style.textAlign = "right";
    counter.style.fontSize = "12px";
    counter.style.color = "#A66F7B";
    counter.style.marginTop = "5px";

    jobDescription.after(counter);

    function updateCounter() {

        const count = jobDescription.value.length;

        counter.textContent = count + " characters";
    }

    jobDescription.addEventListener("input", updateCounter);

    updateCounter();


    form.addEventListener("submit", function (event) {

        const file = resumeInput.files[0];
        const description = jobDescription.value.trim();

        if (!file || !file.name.toLowerCase().endsWith(".pdf")) {
            event.preventDefault();
            alert("Please upload a valid PDF resume.");
            return;
        }

        if (description.length === 0) {
            event.preventDefault();
            alert("Please enter a job description.");
            return;
        }

        // Loading effect
        submitButton.textContent = "Analysing Resume...";
        submitButton.disabled = true;

    });

});