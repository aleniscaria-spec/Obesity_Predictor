const form = document.getElementById("predictionForm");
const predictBtn = document.getElementById("predictBtn");
const btnText = document.getElementById("btnText");
const loader = document.getElementById("loader");

const resultCard = document.getElementById("resultCard");
const predictionText = document.getElementById("predictionText");
const confidenceValue = document.getElementById("confidenceValue");
const confidenceBar = document.getElementById("confidenceBar");
const statusBadge = document.getElementById("statusBadge");

const modal = document.getElementById("infoModal");
const modalTitle = document.getElementById("modalTitle");
const modalDescription = document.getElementById("modalDescription");
const closeModal = document.querySelector(".close-modal");


// ======================================
// Field Information
// ======================================

const infoData = {
    fcvc: {
        title: "FCVC - Vegetable Consumption",
        description:
            "FCVC indicates how often vegetables are consumed in daily meals. Values typically range from 1 to 3. Higher values indicate healthier eating habits."
    },

    ncp: {
        title: "NCP - Number of Main Meals",
        description:
            "NCP represents the number of main meals consumed per day. Usually ranges between 1 and 5."
    },

    ch2o: {
        title: "CH2O - Daily Water Consumption",
        description:
            "CH2O measures daily water intake. Values generally range from 1 to 3, where higher values indicate better hydration."
    },

    faf: {
        title: "FAF - Physical Activity Frequency",
        description:
            "FAF represents how often physical activities or exercises are performed. Higher values indicate a more active lifestyle."
    },

    tue: {
        title: "TUE - Technology Usage Time",
        description:
            "TUE measures time spent using electronic devices such as computers, smartphones, or television."
    }
};


// ======================================
// Modal Handling
// ======================================

document.querySelectorAll(".info-btn").forEach(button => {

    button.addEventListener("click", () => {

        const key = button.dataset.info;

        modalTitle.textContent = infoData[key].title;
        modalDescription.textContent = infoData[key].description;

        modal.style.display = "flex";
    });

});

closeModal.addEventListener("click", () => {
    modal.style.display = "none";
});

window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});


// ======================================
// Status Badge Styling
// ======================================

function updateStatusBadge(status) {

    statusBadge.textContent = status;

    statusBadge.style.background = "#10b981";

    if (status === "Warning") {
        statusBadge.style.background = "#f59e0b";
    }

    if (status === "Risk") {
        statusBadge.style.background = "#ef4444";
    }
}


// ======================================
// Form Submit
// ======================================

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const formData = new FormData(form);

    const data = Object.fromEntries(formData.entries());

    predictBtn.disabled = true;

    btnText.textContent = "Analyzing Health Data...";
    loader.classList.remove("hidden");

    try {

        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.error || "Prediction failed"
            );
        }

        predictionText.textContent =
            result.prediction;

        confidenceValue.textContent =
            `${result.confidence}%`;

        updateStatusBadge(result.status);

        resultCard.classList.remove("hidden");

        setTimeout(() => {
            confidenceBar.style.width =
                `${result.confidence}%`;
        }, 100);

        resultCard.scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {

        alert(
            "Error: " + error.message
        );

        console.error(error);
    }

    finally {

        loader.classList.add("hidden");

        btnText.textContent =
            "Predict Health Status";

        predictBtn.disabled = false;
    }

});


// ======================================
// Input Validation
// ======================================

document.querySelectorAll("input").forEach(input => {

    input.addEventListener("input", () => {

        if (
            input.value !== "" &&
            Number(input.value) < 0
        ) {
            input.value = "";
        }

    });

});


// ======================================
// Confidence Bar Reset
// ======================================

window.addEventListener("load", () => {
    confidenceBar.style.width = "0%";
});