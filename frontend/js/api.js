// ============================================================
// AnimalCare Frontend API
// ============================================================

const API_BASE_URL = "https://animalcare-v2-production.up.railway.app";

// ============================================================
// TOKEN HELPERS
// ============================================================

function getToken() {
    return localStorage.getItem("access_token");
}


function saveToken(token) {

    if (!token) {
        console.error("No access token received.");
        return false;
    }

    localStorage.setItem(
        "access_token",
        token
    );

    return (
        localStorage.getItem(
            "access_token"
        ) === token
    );
}


function getCurrentUser() {

    const user =
        localStorage.getItem("user");

    if (!user) {
        return null;
    }

    try {

        return JSON.parse(user);

    } catch (error) {

        console.error(
            "Invalid stored user data."
        );

        return null;
    }
}


function logout() {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "user"
    );

    window.location.href =
        "login.html";
}


// ============================================================
// GENERIC API REQUEST
// ============================================================

async function apiRequest(
    endpoint,
    options = {}
) {

    const token =
        getToken();


    const headers = {

        "Content-Type":
            "application/json",

        ...(options.headers || {})

    };


    // Add JWT if available

    if (token) {

        headers[
            "Authorization"
        ] =
            `Bearer ${token}`;

    }


    console.log(
        "API REQUEST:",
        endpoint
    );

    console.log(
        "TOKEN AVAILABLE:",
        !!token
    );


    try {

        const response =
            await fetch(
                `${API_BASE_URL}${endpoint}`,
                {
                    ...options,
                    headers: headers
                }
            );


        let data;


        try {

            data =
                await response.json();

        } catch (error) {

            data = {};

        }


        console.log(
            "API RESPONSE:",
            endpoint,
            response.status
        );


        // ====================================================
        // UNAUTHORIZED
        // ====================================================

        if (
            response.status === 401
        ) {

            console.warn(
                "Unauthorized request:",
                endpoint
            );


            if (!getToken()) {

                window.location.href =
                    "login.html";

            }


            throw new Error(
                data.message ||
                data.msg ||
                "Authentication required."
            );

        }


        // ====================================================
        // OTHER ERRORS
        // ====================================================

        if (!response.ok) {

            throw new Error(
                data.message ||
                data.msg ||
                "API request failed."
            );

        }


        return data;


    } catch (error) {

        console.error(
            "API ERROR:",
            endpoint,
            error
        );

        throw error;

    }

}


// ============================================================
// AUTHENTICATION
// ============================================================

async function login(
    email,
    password
) {

    const data =
        await apiRequest(
            "/api/auth/login",
            {
                method: "POST",

                body:
                    JSON.stringify({
                        email:
                            email,

                        password:
                            password
                    })
            }
        );


    console.log(
        "LOGIN RESPONSE RECEIVED:",
        data
    );


    // Save JWT

    if (
        data.access_token
    ) {

        const saved =
            saveToken(
                data.access_token
            );


        console.log(
            "TOKEN SAVED:",
            saved
        );

    }


    // Save user

    if (
        data.user
    ) {

        localStorage.setItem(
            "user",
            JSON.stringify(
                data.user
            )
        );

    }


    return data;

}


// ============================================================
// ANIMALS
// ============================================================

async function getAnimals() {

    return await apiRequest(
        "/api/animals/",
        {
            method: "GET"
        }
    );

}


// ============================================================
// NGOs
// ============================================================

async function getNGOs() {

    return await apiRequest(
        "/api/ngos/",
        {
            method: "GET"
        }
    );

}


// Compatibility alias

async function getNgos() {

    return await getNGOs();

}


// ============================================================
// VOLUNTEERS
// ============================================================

async function getVolunteers() {

    return await apiRequest(
        "/api/volunteers/",
        {
            method: "GET"
        }
    );

}


// ============================================================
// RESCUES
// ============================================================

async function getRescues() {

    return await apiRequest(
        "/api/rescues/",
        {
            method: "GET"
        }
    );

}


async function getRescue(
    id
) {

    return await apiRequest(
        `/api/rescues/${id}`,
        {
            method: "GET"
        }
    );

}


// ============================================================
// ADOPTIONS
// ============================================================

async function getAdoptions() {

    return await apiRequest(
        "/api/adoptions/",
        {
            method: "GET"
        }
    );

}


async function getAdoption(
    id
) {

    return await apiRequest(
        `/api/adoptions/${id}`,
        {
            method: "GET"
        }
    );

}


// ============================================================
// BACKEND HEALTH
// ============================================================

async function checkBackend() {

    return await apiRequest(
        "/",
        {
            method: "GET"
        }
    );

}