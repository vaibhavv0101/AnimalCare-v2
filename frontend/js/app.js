// ========================================
// ANIMALCARE - MAIN APP.JS
// ========================================

let animalsCache = [];

// ========================================
// ANIMAL SPECIES ICONS
// ========================================

function getAnimalIcon(species) {

    const icons = {
        dog: "🐶",
        cat: "🐱",
        cow: "🐄",
        buffalo: "🐃",
        goat: "🐐",
        horse: "🐴",
        bird: "🐦",
        other: "🐾"
    };

    const key = String(species || "other")
        .trim()
        .toLowerCase();

    return icons[key] || "🐾";
}
// ============================================================
// PAGE INITIALIZATION
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    const token = getToken();

    if (token) {

        loadDashboard();

    } else {

        console.log(
            "No login token. Dashboard APIs skipped."
        );

    }

});
// ========================================
// DASHBOARD
// ========================================

async function loadDashboard() {

    await Promise.all([
        loadAnimals(),
        loadNGOs(),
        loadVolunteers(),
        loadRescues()
    ]);

}


// ========================================
// ANIMALS
// ========================================

async function loadAnimals() {

    const container =
        document.getElementById("animalsContainer");

    const countElement =
        document.getElementById("animalCount");

    if (!container) {
        return;
    }

    try {

        const data = await getAnimals();

        const animals = data.animals || [];

        // Save animals for View Details
        animalsCache = animals;

        if (countElement) {
            countElement.textContent =
                data.count ?? animals.length;
        }

        if (animals.length === 0) {

            container.innerHTML = `
                <div class="empty-state">
                    <h3>No animals available</h3>
                    <p>
                        There are currently no animals listed.
                    </p>
                </div>
            `;

            return;
        }

        container.innerHTML = animals.map(animal => {

            const adoptionStatus =
                animal.adoption_status || "Available";

            const statusLower =
                String(adoptionStatus).toLowerCase();

            const isAdopted =
                statusLower === "adopted";

            return `

                <div class="animal-card">

                    <div class="animal-image">
                        ${getAnimalIcon(animal.species)}
                    </div>

                    <div class="animal-content">

                        <span class="animal-status">
                            ${escapeHTML(adoptionStatus)}
                        </span>

                        <h3>
                            ${escapeHTML(
                                animal.name || `Animal #${animal.id}`
                            )}
                        </h3>

                        <p>
                            ${escapeHTML(
                                animal.breed ||
                                animal.species ||
                                "Animal"
                            )}
                        </p>

                        <div class="animal-details">

                            <span>
                                🎂 ${animal.age ?? "N/A"} years
                            </span>

                            <span>
                                ⚧ ${escapeHTML(
                                    animal.gender || "N/A"
                                )}
                            </span>

                        </div>

                        <button
                            class="btn btn-primary"
                            onclick="viewAnimal(${animal.id})">
                            View Details
                        </button>

                    </div>

                </div>

            `;

        }).join("");

    } catch (error) {

        console.error(
            "ANIMALS LOAD ERROR:",
            error
        );

        if (countElement) {
            countElement.textContent = "0";
        }

        container.innerHTML = `
            <div class="error-state">
                <h3>Unable to load animals</h3>
                <p>
                    Please make sure the AnimalCare
                    backend is running.
                </p>
            </div>
        `;
    }
}


// ========================================
// VIEW ANIMAL DETAILS
// ========================================

function viewAnimal(id) {

    const animal =
        animalsCache.find(
            item => Number(item.id) === Number(id)
        );

    if (!animal) {

        alert(
            "Unable to find animal details."
        );

        return;
    }

    const status =
        animal.adoption_status ||
        "Available";

    const statusLower =
        String(status).toLowerCase();

    const isAdopted =
        statusLower === "adopted";

    // Remove existing modal
    document
        .getElementById("animalDetailsModal")
        ?.remove();

    const modal =
        document.createElement("div");

    modal.id =
        "animalDetailsModal";

    modal.innerHTML = `

        <div class="animal-modal-overlay">

            <div class="animal-modal">

                <button
                    class="animal-modal-close"
                    onclick="closeAnimalDetails()">
                    ×
                </button>

                <div class="animal-modal-icon">
                    🐕
                </div>

                <div class="animal-modal-status">
                    ${escapeHTML(status)}
                </div>

                <h2>
                    ${escapeHTML(
                        animal.name ||
                        `Animal #${animal.id}`
                    )}
                </h2>

                <p class="animal-modal-subtitle">
                    ${escapeHTML(
                        animal.breed ||
                        animal.species ||
                        "Animal"
                    )}
                </p>

                <div class="animal-info-grid">

                    <div class="animal-info-box">
                        <span>Animal ID</span>
                        <strong>
                            #${animal.id}
                        </strong>
                    </div>

                    <div class="animal-info-box">
                        <span>Species</span>
                        <strong>
                            ${escapeHTML(
                                animal.species || "N/A"
                            )}
                        </strong>
                    </div>

                    <div class="animal-info-box">
                        <span>Breed</span>
                        <strong>
                            ${escapeHTML(
                                animal.breed || "N/A"
                            )}
                        </strong>
                    </div>

                    <div class="animal-info-box">
                        <span>Age</span>
                        <strong>
                            ${animal.age ?? "N/A"} years
                        </strong>
                    </div>

                    <div class="animal-info-box">
                        <span>Gender</span>
                        <strong>
                            ${escapeHTML(
                                animal.gender || "N/A"
                            )}
                        </strong>
                    </div>

                    <div class="animal-info-box">
                        <span>Status</span>
                        <strong>
                            ${escapeHTML(status)}
                        </strong>
                    </div>

                </div>

                <div class="animal-description">

                    <h3>About This Animal</h3>

                    <p>
                        ${escapeHTML(
                            animal.description ||
                            "This animal is looking for care, love and a safe home."
                        )}
                    </p>

                </div>

                <div class="animal-modal-actions">

                    ${
                        isAdopted

                        ? `

                            <button
                                class="btn btn-disabled"
                                disabled>
                                Already Adopted
                            </button>

                        `

                        : `

                            <button
                                class="btn btn-primary"
                                onclick="openAdoptionForm(${animal.id})">
                                🐾 Apply for Adoption
                            </button>

                        `
                    }

                    <button
                        class="btn btn-secondary"
                        onclick="closeAnimalDetails()">
                        Close
                    </button>

                </div>

            </div>

        </div>

    `;

    document.body.appendChild(modal);

    addAnimalModalStyles();
}


// ========================================
// CLOSE ANIMAL DETAILS
// ========================================

function closeAnimalDetails() {

    document
        .getElementById("animalDetailsModal")
        ?.remove();

}


// ========================================
// OPEN ADOPTION FORM
// ========================================

function openAdoptionForm(animalId) {

    const animal =
        animalsCache.find(
            item => Number(item.id) === Number(animalId)
        );

    if (!animal) {

        alert(
            "Animal details not found."
        );

        return;
    }

    closeAnimalDetails();

    document
        .getElementById("adoptionFormModal")
        ?.remove();

    const modal =
        document.createElement("div");

    modal.id =
        "adoptionFormModal";

    modal.innerHTML = `

        <div class="animal-modal-overlay">

            <div class="adoption-modal">

                <button
                    class="animal-modal-close"
                    onclick="closeAdoptionForm()">
                    ×
                </button>

                <div class="adoption-header">

                    <div class="animal-modal-icon small">
                        🐾
                    </div>

                    <h2>
                        Apply for Adoption
                    </h2>

                    <p>
                        Apply to give
                        <strong>
                            ${escapeHTML(
                                animal.name ||
                                `Animal #${animal.id}`
                            )}
                        </strong>
                        a loving home.
                    </p>

                </div>

                <form id="adoptionApplicationForm">

                    <input
                        type="hidden"
                        id="adoptionAnimalId"
                        value="${animal.id}"
                    >

                    <div class="adoption-form-grid">

                        <div class="form-field">

                            <label for="adoptionPhone">
                                Phone Number
                            </label>

                            <input
                                type="tel"
                                id="adoptionPhone"
                                placeholder="Enter your phone number"
                                required
                            >

                        </div>

                        <div class="form-field">

                            <label for="adoptionOccupation">
                                Occupation
                            </label>

                            <input
                                type="text"
                                id="adoptionOccupation"
                                placeholder="e.g. Student"
                                required
                            >

                        </div>

                    </div>

                    <div class="form-field">

                        <label for="adoptionAddress">
                            Address
                        </label>

                        <textarea
                            id="adoptionAddress"
                            rows="3"
                            placeholder="Enter your complete address"
                            required
                        ></textarea>

                    </div>

                    <div class="form-field">

                        <label for="adoptionReason">
                            Reason for Adoption
                        </label>

                        <textarea
                            id="adoptionReason"
                            rows="4"
                            placeholder="Why would you like to adopt this animal?"
                            required
                        ></textarea>

                    </div>

                    <div
                        id="adoptionMessage"
                        class="adoption-message">
                    </div>

                    <div class="animal-modal-actions">

                        <button
                            type="submit"
                            class="btn btn-primary"
                            id="submitAdoptionBtn">
                            Submit Adoption Application
                        </button>

                        <button
                            type="button"
                            class="btn btn-secondary"
                            onclick="closeAdoptionForm()">
                            Cancel
                        </button>

                    </div>

                </form>

            </div>

        </div>

    `;

    document.body.appendChild(modal);

    addAnimalModalStyles();

    document
        .getElementById("adoptionApplicationForm")
        .addEventListener(
            "submit",
            submitAdoptionApplication
        );
}


// ========================================
// CLOSE ADOPTION FORM
// ========================================

function closeAdoptionForm() {

    document
        .getElementById("adoptionFormModal")
        ?.remove();

}


// ========================================
// SUBMIT ADOPTION APPLICATION
// ========================================

async function submitAdoptionApplication(event) {

    event.preventDefault();

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");

    if (!token) {

        alert(
            "Please login before applying for adoption."
        );

        window.location.href =
            "login.html";

        return;
    }

    const animalId =
        Number(
            document.getElementById(
                "adoptionAnimalId"
            ).value
        );

    const phone =
        document.getElementById(
            "adoptionPhone"
        ).value.trim();

    const occupation =
        document.getElementById(
            "adoptionOccupation"
        ).value.trim();

    const address =
        document.getElementById(
            "adoptionAddress"
        ).value.trim();

    const reason =
        document.getElementById(
            "adoptionReason"
        ).value.trim();

    const message =
        document.getElementById(
            "adoptionMessage"
        );

    const button =
        document.getElementById(
            "submitAdoptionBtn"
        );

    if (
        !phone ||
        !occupation ||
        !address ||
        !reason
    ) {

        message.className =
            "adoption-message error";

        message.textContent =
            "Please fill in all fields.";

        return;
    }

    button.disabled = true;

    button.textContent =
        "Submitting...";

    message.className =
        "adoption-message";

    message.textContent =
        "";

    try {

        console.log(
            "Submitting adoption application:",
            {
                animal_id: animalId,
                phone,
                occupation,
                address,
                reason
            }
        );

        const response =
            await fetch(
                "http://127.0.0.1:5000/api/adoptions/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${token}`
                    },

                    body: JSON.stringify({
                        animal_id: animalId,
                        phone: phone,
                        occupation: occupation,
                        address: address,
                        reason: reason
                    })
                }
            );

        const data =
            await response.json()
                .catch(() => ({}));

        console.log(
            "ADOPTION API STATUS:",
            response.status
        );

        console.log(
            "ADOPTION API RESPONSE:",
            data
        );

        if (!response.ok) {

            throw new Error(
                data.message ||
                data.error ||
                "Failed to submit adoption application."
            );
        }

        message.className =
            "adoption-message success";

        message.textContent =
            "Adoption application submitted successfully!";

        button.textContent =
            "Application Submitted";

        // Wait briefly, then open applications
        setTimeout(() => {

            window.location.href =
                "adoptions.html";

        }, 1200);

    } catch (error) {

        console.error(
            "ADOPTION APPLICATION ERROR:",
            error
        );

        message.className =
            "adoption-message error";

        message.textContent =
            error.message ||
            "Unable to submit adoption application.";

        button.disabled = false;

        button.textContent =
            "Submit Adoption Application";
    }
}


// ========================================
// NGOs
// ========================================

async function loadNGOs() {

    const container =
        document.getElementById("ngosContainer");

    const countElement =
        document.getElementById("ngoCount");

    if (!container) {
        return;
    }

    try {

        const data =
            await getNGOs();

        const ngos =
            data.ngos || [];

        if (countElement) {

            countElement.textContent =
                data.count ?? ngos.length;
        }

        if (ngos.length === 0) {

            container.innerHTML = `
                <div class="empty-state">
                    <h3>No NGOs registered</h3>
                </div>
            `;

            return;
        }

        container.innerHTML =
            ngos.map(ngo => `

                <div class="info-card">

                    <div class="info-icon">
                        🏢
                    </div>

                    <h3>
                        ${escapeHTML(
                            ngo.name
                        )}
                    </h3>

                    <p>
                        ${escapeHTML(
                            ngo.description ||
                            "Animal rescue organization"
                        )}
                    </p>

                    <div class="card-meta">
                        📍 ${escapeHTML(
                            ngo.address ||
                            "N/A"
                        )}
                    </div>

                    <span class="status-badge">
                        ${escapeHTML(
                            ngo.status ||
                            "Active"
                        )}
                    </span>

                </div>

            `).join("");

    } catch (error) {

        console.error(
            "NGOS LOAD ERROR:",
            error
        );

        if (countElement) {
            countElement.textContent = "0";
        }

        container.innerHTML = `
            <div class="error-state">
                <h3>Unable to load NGOs</h3>
            </div>
        `;
    }
}


// ========================================
// VOLUNTEERS
// ========================================

async function loadVolunteers() {

    const container =
        document.getElementById(
            "volunteersContainer"
        );

    const countElement =
        document.getElementById(
            "volunteerCount"
        );

    if (!container) {
        return;
    }

    try {

        const data =
            await getVolunteers();

        const volunteers =
            data.volunteers || [];

        if (countElement) {

            countElement.textContent =
                data.count ?? volunteers.length;
        }

        if (volunteers.length === 0) {

            container.innerHTML = `
                <div class="empty-state">
                    <h3>
                        No volunteers registered
                    </h3>
                </div>
            `;

            return;
        }

        container.innerHTML =
            volunteers.map(
                volunteer => `

                    <div class="info-card">

                        <div class="info-icon">
                            🤝
                        </div>

                        <h3>
                            ${escapeHTML(
                                volunteer.name
                            )}
                        </h3>

                        <p>
                            ${escapeHTML(
                                volunteer.email || ""
                            )}
                        </p>

                        <div class="card-meta">
                            📍 ${escapeHTML(
                                volunteer.address ||
                                "N/A"
                            )}
                        </div>

                        <div class="card-meta">
                            🟢 ${escapeHTML(
                                volunteer.availability ||
                                "N/A"
                            )}
                        </div>

                    </div>

                `
            ).join("");

    } catch (error) {

        console.error(
            "VOLUNTEERS LOAD ERROR:",
            error
        );

        if (countElement) {
            countElement.textContent = "0";
        }

        container.innerHTML = `
            <div class="error-state">
                <h3>
                    Unable to load volunteers
                </h3>
            </div>
        `;
    }
}


// ========================================
// RESCUES
// ========================================

async function loadRescues() {

    const countElement =
        document.getElementById(
            "rescueCount"
        );

    if (!countElement) {
        return;
    }

    try {

        const data =
            await getRescues();

        countElement.textContent =
            data.count ??
            data.rescues?.length ??
            0;

    } catch (error) {

        console.error(
            "RESCUES LOAD ERROR:",
            error
        );

        countElement.textContent =
            "0";
    }
}


// ========================================
// LOGIN BUTTON
// ========================================

document
    .getElementById("loginBtn")
    ?.addEventListener(
        "click",
        () => {

            window.location.href =
                "login.html";

        }
    );


// ========================================
// FIND ANIMAL BUTTON
// ========================================

document
    .getElementById("exploreAnimalsBtn")
    ?.addEventListener(
        "click",
        () => {

            document
                .getElementById("animals")
                ?.scrollIntoView({
                    behavior: "smooth"
                });

        }
    );


// ========================================
// REPORT RESCUE BUTTON
// ========================================

document
    .getElementById("reportRescueBtn")
    ?.addEventListener(
        "click",
        () => {

            window.location.href =
                "rescues.html";

        }
    );


// ========================================
// VIEW ADOPTIONS BUTTON
// ========================================

document
    .getElementById("viewAdoptionsBtn")
    ?.addEventListener(
        "click",
        () => {

            window.location.href =
                "adoptions.html";

        }
    );


// ========================================
// MODAL STYLES
// ========================================

function addAnimalModalStyles() {

    if (
        document.getElementById(
            "animalModalStyles"
        )
    ) {
        return;
    }

    const style =
        document.createElement("style");

    style.id =
        "animalModalStyles";

    style.textContent = `

        .animal-modal-overlay {

            position: fixed;
            inset: 0;

            background:
                rgba(15, 23, 42, 0.65);

            display: flex;

            align-items: center;
            justify-content: center;

            padding: 20px;

            z-index: 99999;

            overflow-y: auto;
        }


        .animal-modal {

            position: relative;

            width: 100%;
            max-width: 650px;

            max-height: 90vh;

            overflow-y: auto;

            background: #ffffff;

            border-radius: 24px;

            padding: 35px;

            box-shadow:
                0 25px 70px
                rgba(0, 0, 0, 0.25);
        }


        .adoption-modal {

            position: relative;

            width: 100%;
            max-width: 650px;

            max-height: 90vh;

            overflow-y: auto;

            background: #ffffff;

            border-radius: 24px;

            padding: 35px;

            box-shadow:
                0 25px 70px
                rgba(0, 0, 0, 0.25);
        }


        .animal-modal-close {

            position: absolute;

            top: 18px;
            right: 18px;

            width: 42px;
            height: 42px;

            border: none;

            border-radius: 50%;

            background: #f1f5f4;

            font-size: 26px;

            cursor: pointer;

            color: #1f2937;
        }


        .animal-modal-close:hover {

            background: #e5e7e9;
        }


        .animal-modal-icon {

            width: 90px;
            height: 90px;

            display: flex;

            align-items: center;
            justify-content: center;

            margin: 5px auto 15px;

            border-radius: 50%;

            background: #eafaf7;

            font-size: 45px;
        }


        .animal-modal-icon.small {

            width: 70px;
            height: 70px;

            font-size: 35px;

            margin-bottom: 10px;
        }


        .animal-modal h2 {

            text-align: center;

            margin: 8px 0;

            color: #17202a;

            font-size: 2rem;
        }


        .animal-modal-subtitle {

            text-align: center;

            color: #566573;

            font-size: 1.05rem;

            margin-bottom: 25px;
        }


        .animal-modal-status {

            width: fit-content;

            margin: 0 auto;

            padding: 8px 18px;

            border-radius: 30px;

            background: #eafaf1;

            color: #117864;

            font-weight: 700;

            font-size: 0.9rem;

            text-transform: uppercase;
        }


        .animal-info-grid {

            display: grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap: 14px;

            margin-top: 25px;
        }


        .animal-info-box {

            padding: 18px;

            border-radius: 14px;

            background: #f7f9f9;

            border: 1px solid #edf0f0;
        }


        .animal-info-box span {

            display: block;

            color: #7b8a8b;

            font-size: 0.85rem;

            margin-bottom: 6px;
        }


        .animal-info-box strong {

            color: #17202a;

            font-size: 1rem;
        }


        .animal-description {

            margin-top: 20px;

            padding: 20px;

            border-radius: 14px;

            background: #f7f9f9;
        }


        .animal-description h3 {

            margin-top: 0;

            color: #17202a;
        }


        .animal-description p {

            color: #566573;

            line-height: 1.6;

            margin-bottom: 0;
        }


        .animal-modal-actions {

            display: flex;

            gap: 12px;

            margin-top: 25px;
        }


        .animal-modal-actions .btn {

            flex: 1;

            min-height: 48px;
        }


        .btn-disabled {

            background: #bdc3c7;

            color: white;

            cursor: not-allowed;

            border: none;
        }


        .adoption-header {

            text-align: center;

            margin-bottom: 25px;
        }


        .adoption-header h2 {

            margin-bottom: 8px;
        }


        .adoption-header p {

            color: #566573;

            line-height: 1.5;
        }


        .adoption-form-grid {

            display: grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap: 16px;
        }


        .form-field {

            margin-bottom: 18px;
        }


        .form-field label {

            display: block;

            margin-bottom: 7px;

            font-weight: 700;

            color: #17202a;
        }


        .form-field input,
        .form-field textarea {

            width: 100%;

            box-sizing: border-box;

            padding: 13px 14px;

            border: 1px solid #d5dbdb;

            border-radius: 10px;

            outline: none;

            font-family: inherit;

            font-size: 15px;
        }


        .form-field textarea {

            resize: vertical;
        }


        .form-field input:focus,
        .form-field textarea:focus {

            border-color: #16a085;

            box-shadow:
                0 0 0 3px
                rgba(22, 160, 133, 0.1);
        }


        .adoption-message {

            display: none;

            padding: 12px 15px;

            border-radius: 10px;

            margin-bottom: 15px;

            text-align: center;

            font-weight: 600;
        }


        .adoption-message.success {

            display: block;

            background: #eafaf1;

            color: #1e8449;
        }


        .adoption-message.error {

            display: block;

            background: #fdedec;

            color: #c0392b;
        }


        @media (max-width: 600px) {

            .animal-modal,
            .adoption-modal {

                padding: 25px;

                border-radius: 18px;
            }


            .animal-info-grid,
            .adoption-form-grid {

                grid-template-columns:
                    1fr;
            }


            .animal-modal-actions {

                flex-direction: column;
            }

        }

    `;

    document.head.appendChild(style);
}


// ========================================
// SECURITY HELPER
// ========================================

function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}