const form = document.getElementById("registrationForm");
const successMessage = document.getElementById("successMessage");
const genderSelect = document.getElementById("gender");
const weightSelect = document.getElementById("weight");
const ageInput = document.getElementById("age");

const menWeights = [
    "-54kg Fin Weight", "-58kg Fly Weight", "-63kg Bantam Weight",
    "-68kg Feather Weight", "-74kg Light Weight", "-80kg Welter Weight",
    "-87kg Middle Weight", "+87kg Heavy Weight"
];

const ladiesWeights = [
    "-46kg Fin Weight", "-49kg Fly Weight", "-53kg Bantam Weight",
    "-57kg Feather Weight", "-62kg Light Weight", "-67kg Welter Weight",
    "-73kg Middle Weight", "+73kg Heavy Weight"
];


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function showTab(tab) {
    document.getElementById("registerSection").style.display = tab === 'register' ? 'block' : 'none';
    document.getElementById("loginSection").style.display = tab === 'login' ? 'block' : 'none';
    document.getElementById("profileSection").style.display = 'none';
    document.getElementById("updateSection").style.display = 'none';
    document.getElementById("athletesSection").style.display = 'none';
    document.getElementById("tabRegister").style.background = tab === 'register' ? '#e94560' : 'rgba(255,255,255,0.2)';
    document.getElementById("tabLogin").style.background = tab === 'login' ? '#e94560' : 'rgba(255,255,255,0.2)';
}


function showAthletesSection() {
    document.getElementById("registerSection").style.display = 'none';
    document.getElementById("loginSection").style.display = 'none';
    document.getElementById("profileSection").style.display = 'none';
    document.getElementById("updateSection").style.display = 'none';
    document.getElementById("athletesSection").style.display = 'block';
    loadAthletes();
}


function goBackFromAthletes() {
    document.getElementById("athletesSection").style.display = "none";
    if (loggedInPlayer) {
        showProfile();
    } else {
        showTab('register');
    }
}


genderSelect.addEventListener("change", function () {
    weightSelect.innerHTML = '<option value="">Select Weight Category</option>';
    let weights = genderSelect.value === "male" ? menWeights : ladiesWeights;
    weights.forEach(weight => {
        const option = document.createElement("option");
        option.textContent = weight;
        option.value = weight;
        weightSelect.appendChild(option);
    });
});


document.getElementById("updateGender").addEventListener("change", function () {
    const updateWeight = document.getElementById("updateWeight");
    updateWeight.innerHTML = '<option value="">Select Weight Category</option>';
    let weights = this.value === "male" ? menWeights : ladiesWeights;
    weights.forEach(weight => {
        const option = document.createElement("option");
        option.textContent = weight;
        option.value = weight;
        updateWeight.appendChild(option);
    });
});


ageInput.addEventListener("input", function () {
    const age = parseInt(ageInput.value);
    if (ageInput.value === "" || age < 15 || age > 40) {
        ageInput.style.borderColor = "red";
        document.getElementById("ageError").style.display = "block";
        document.getElementById("submitBtn").disabled = true;
    } else {
        ageInput.style.borderColor = "green";
        document.getElementById("ageError").style.display = "none";
        document.getElementById("submitBtn").disabled = false;
    }
});


document.getElementById("fullname").addEventListener("input", function () {
    document.getElementById("duplicateError").style.display = "none";
    this.style.borderColor = "";
    document.getElementById("club").style.borderColor = "";
});

document.getElementById("club").addEventListener("input", function () {
    document.getElementById("duplicateError").style.display = "none";
    this.style.borderColor = "";
    document.getElementById("fullname").style.borderColor = "";
});


document.getElementById("email").addEventListener("input", function () {
    document.getElementById("emailError").style.display = "none";
    this.style.borderColor = "";
});


document.getElementById("photo").addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("photoPreview").src = e.target.result;
        };
        reader.readAsDataURL(file);
        document.getElementById("photoError").style.display = "none";
    }
});


document.getElementById("updatePhoto").addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("updatePhotoPreview").src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});


form.addEventListener("submit", function (event) {
    event.preventDefault();

    const photoInput = document.getElementById("photo");
    if (!photoInput.files || photoInput.files.length === 0) {
        document.getElementById("photoError").style.display = "block";
        return;
    }

    const age = parseInt(ageInput.value);
    if (isNaN(age) || age < 15 || age > 40) {
        document.getElementById("ageError").style.display = "block";
        ageInput.style.borderColor = "red";
        document.getElementById("submitBtn").disabled = true;
        return;
    }

    document.getElementById("submitBtn").disabled = true;
    document.getElementById("submitBtn").innerText = "Submitting...";

    const formData = new FormData(form);
    formData.append("photo", photoInput.files[0]);

    fetch("/register/", {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("submitBtn").disabled = false;
            document.getElementById("submitBtn").innerText = "Submit Registration";

            if (data.status === "success") {
                document.getElementById("ageError").style.display = "none";
                document.getElementById("duplicateError").style.display = "none";
                document.getElementById("emailError").style.display = "none";
                document.getElementById("photoError").style.display = "none";
                document.getElementById("fullname").style.borderColor = "";
                document.getElementById("club").style.borderColor = "";
                document.getElementById("email").style.borderColor = "";
                ageInput.style.borderColor = "";

                document.getElementById("regNumber").innerText = data.registration_number;
                document.getElementById("photoPreview").src = "/static/registration/images/default_avator.png";

                successMessage.style.display = "block";
                successMessage.scrollIntoView({ behavior: "smooth" });
                setTimeout(() => { successMessage.style.display = "none"; }, 15000);

                form.reset();
                weightSelect.innerHTML = '<option value="">Select Weight Category</option>';

            } else if (data.status === "error") {
                if (data.field === "age") {
                    document.getElementById("ageError").innerText = data.message;
                    document.getElementById("ageError").style.display = "block";
                    ageInput.style.borderColor = "red";
                    document.getElementById("submitBtn").disabled = true;
                } else if (data.field === "duplicate") {
                    const dupError = document.getElementById("duplicateError");
                    dupError.innerText = data.message;
                    dupError.style.display = "block";
                    document.getElementById("fullname").style.borderColor = "red";
                    document.getElementById("club").style.borderColor = "red";
                    setTimeout(() => {
                        dupError.style.display = "none";
                        document.getElementById("fullname").style.borderColor = "";
                        document.getElementById("club").style.borderColor = "";
                    }, 5000);
                } else if (data.field === "email") {
                    const emailError = document.getElementById("emailError");
                    emailError.innerText = data.message;
                    emailError.style.display = "block";
                    document.getElementById("email").style.borderColor = "red";
                    setTimeout(() => {
                        emailError.style.display = "none";
                        document.getElementById("email").style.borderColor = "";
                    }, 5000);
                } else if (data.field === "server") {
                    alert(data.message);
                }
            }
        })
        .catch(error => {
            document.getElementById("submitBtn").disabled = false;
            document.getElementById("submitBtn").innerText = "Submit Registration";
            console.error("Error:", error);
        });
});


let loggedInPlayer = null;

function loginPlayer() {
    const regNumber = document.getElementById("loginRegNumber").value.trim().toUpperCase();

    if (!regNumber) {
        document.getElementById("loginError").innerText = "Please enter your registration number.";
        document.getElementById("loginError").style.display = "block";
        return;
    }

    const formData = new FormData();
    formData.append("registration_number", regNumber);
    formData.append("csrfmiddlewaretoken", getCookie('csrftoken'));

    fetch("/login/", {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                loggedInPlayer = data.player;
                document.getElementById("loginError").style.display = "none";
                showProfile();
            } else {
                document.getElementById("loginError").innerText = data.message;
                document.getElementById("loginError").style.display = "block";
            }
        })
        .catch(error => {
            console.error("Login error:", error);
            document.getElementById("loginError").innerText = "Connection error. Please try again.";
            document.getElementById("loginError").style.display = "block";
        });
}


function showProfile() {
    document.getElementById("loginSection").style.display = "none";
    document.getElementById("updateSection").style.display = "none";
    document.getElementById("profileSection").style.display = "block";
    document.getElementById("registerSection").style.display = "none";
    document.getElementById("athletesSection").style.display = "none";

    document.getElementById("profileName").innerText = loggedInPlayer.full_name;
    document.getElementById("profileRegNum").innerText = loggedInPlayer.registration_number;
    document.getElementById("profileAge").innerText = loggedInPlayer.age;
    document.getElementById("profileClub").innerText = loggedInPlayer.club_name;
    document.getElementById("profileGender").innerText = loggedInPlayer.gender;
    document.getElementById("profileWeight").innerText = loggedInPlayer.weight_category;
    document.getElementById("profileNationality").innerText = loggedInPlayer.nationality;

    if (loggedInPlayer.photo) {
        document.getElementById("profilePhoto").src = loggedInPlayer.photo;
    }
}


function showUpdateForm() {
    document.getElementById("profileSection").style.display = "none";
    document.getElementById("updateSection").style.display = "block";

    document.getElementById("updateRegNumber").value = loggedInPlayer.registration_number;
    document.getElementById("updateFullname").value = loggedInPlayer.full_name;
    document.getElementById("updateAge").value = loggedInPlayer.age;
    document.getElementById("updateClub").value = loggedInPlayer.club_name;
    document.getElementById("updateNationality").value = loggedInPlayer.nationality;
    document.getElementById("updateGender").value = loggedInPlayer.gender;

    const updateWeight = document.getElementById("updateWeight");
    updateWeight.innerHTML = '<option value="">Select Weight Category</option>';
    let weights = loggedInPlayer.gender === "male" ? menWeights : ladiesWeights;
    weights.forEach(weight => {
        const option = document.createElement("option");
        option.textContent = weight;
        option.value = weight;
        updateWeight.appendChild(option);
    });
    updateWeight.value = loggedInPlayer.weight_category;

    if (loggedInPlayer.photo) {
        document.getElementById("updatePhotoPreview").src = loggedInPlayer.photo;
    }
}


function submitUpdate() {
    const age = parseInt(document.getElementById("updateAge").value);
    if (isNaN(age) || age < 15 || age > 40) {
        document.getElementById("updateAgeError").style.display = "block";
        return;
    }
    document.getElementById("updateAgeError").style.display = "none";

    const formData = new FormData();
    formData.append("csrfmiddlewaretoken", getCookie('csrftoken'));
    formData.append("registration_number", document.getElementById("updateRegNumber").value);
    formData.append("fullname", document.getElementById("updateFullname").value);
    formData.append("age", age);
    formData.append("club_name", document.getElementById("updateClub").value);
    formData.append("gender", document.getElementById("updateGender").value);
    formData.append("weight_category", document.getElementById("updateWeight").value);
    formData.append("nationality", document.getElementById("updateNationality").value);

    const photoFile = document.getElementById("updatePhoto").files[0];
    if (photoFile) {
        formData.append("photo", photoFile);
    }

    fetch("/update/", {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                document.getElementById("updateSuccess").innerText = data.message;
                document.getElementById("updateSuccess").style.display = "block";
                document.getElementById("updateError").style.display = "none";

                loggedInPlayer.full_name = document.getElementById("updateFullname").value;
                loggedInPlayer.age = age;
                loggedInPlayer.club_name = document.getElementById("updateClub").value;
                loggedInPlayer.gender = document.getElementById("updateGender").value;
                loggedInPlayer.weight_category = document.getElementById("updateWeight").value;
                loggedInPlayer.nationality = document.getElementById("updateNationality").value;

                setTimeout(() => {
                    document.getElementById("updateSuccess").style.display = "none";
                    showProfile();
                }, 2000);
            } else {
                document.getElementById("updateError").innerText = data.message;
                document.getElementById("updateError").style.display = "block";
            }
        })
        .catch(error => console.error("Error:", error));
}


function logout() {
    loggedInPlayer = null;
    document.getElementById("profileSection").style.display = "none";
    document.getElementById("loginRegNumber").value = "";
    showTab('login');
}


let allAthletes = [];

function loadAthletes() {
    document.getElementById("athletesList").innerHTML = '<p style="color:white; text-align:center;">Loading...</p>';

    fetch("/athletes/")
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                allAthletes = data.athletes;
                renderAthletes(allAthletes);
            }
        })
        .catch(error => console.error("Error loading athletes:", error));
}


function renderAthletes(athletes) {
    const container = document.getElementById("athletesList");
    const countEl = document.getElementById("athleteCount");

    countEl.innerText = `Total Athletes: ${athletes.length}`;

    if (athletes.length === 0) {
        container.innerHTML = '<p style="color:white; text-align:center;">No athletes registered yet.</p>';
        return;
    }

    container.innerHTML = athletes.map((athlete, index) => `
        <div style="
            display: flex;
            align-items: center;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            padding: 8px 10px;
            margin-bottom: 8px;
            border: 1px solid rgba(255,255,255,0.15);
        ">
            <span style="color: #e94560; font-weight: bold; font-size: 13px; margin-right: 10px; min-width: 20px;">${index + 1}</span>
            <img src="${athlete.photo || '/static/registration/images/default_avator.png'}"
                style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid #e94560; margin-right: 10px;">
            <div style="flex: 1;">
                <p style="color: white; font-weight: bold; font-size: 13px; margin: 0;">${athlete.full_name}</p>
                <p style="color: rgba(255,255,255,0.6); font-size: 11px; margin: 2px 0;">⚖️ ${athlete.weight_category}</p>
                <p style="color: rgba(255,255,255,0.6); font-size: 11px; margin: 0;">🏛️ ${athlete.club_name} &nbsp;|&nbsp; 🌍 ${athlete.nationality}</p>
            </div>
            <span style="
                background: ${athlete.gender === 'male' ? 'rgba(0,100,255,0.3)' : 'rgba(255,0,100,0.3)'};
                color: white;
                font-size: 10px;
                padding: 3px 7px;
                border-radius: 10px;
            ">${athlete.gender === 'male' ? '♂ Male' : '♀ Female'}</span>
        </div>
    `).join('');
}


function filterAthletes() {
    const query = document.getElementById("athleteSearch").value.toLowerCase();
    const filtered = allAthletes.filter(athlete =>
        athlete.full_name.toLowerCase().includes(query) ||
        athlete.club_name.toLowerCase().includes(query) ||
        athlete.nationality.toLowerCase().includes(query) ||
        athlete.weight_category.toLowerCase().includes(query)
    );
    renderAthletes(filtered);
}

