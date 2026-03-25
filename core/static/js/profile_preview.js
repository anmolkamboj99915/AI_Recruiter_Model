// ================= PROFILE PREVIEW SCRIPT =================

// ================= ELEMENTS =================
const container = document.getElementById("profileContainer");
const printBtn = document.getElementById("printBtn");
const shareBtn = document.getElementById("shareBtn");

// ✅ FIX 1: safe fallback handling
let userId = localStorage.getItem("user_id") || 1;

// ================= LOAD PROFILE =================
async function loadProfile() {
	// ✅ FIX 2: prevent crash if container missing
	if (!container) return;

	try {
		const res = await fetch("/api/candidate/" + userId + "/");

		// ✅ FIX 3: response validation
		if (!res.ok) {
			throw new Error("API error");
		}

		const data = await res.json();

		if (!data || data.error) {
			container.innerHTML = "<p>Unable to load profile</p>";
			return;
		}

		const skillsHTML = data.skills && data.skills.length ? data.skills.map((s) => `<span>${s}</span>`).join("") : "<em>No skills added</em>";

		const projectsHTML =
			data.projects && data.projects.length
				? data.projects
						.map(
							(p) => `
                                <div class="project">
                                    <strong>${p.title || "Untitled"}</strong>
                                    <p>${p.description || ""}</p>
                                    <small>${p.tech || ""}</small>
                                </div>
                            `,
						)
						.join("")
				: "<p><em>No projects added</em></p>";

		const expHTML =
			data.experiences && data.experiences.length
				? data.experiences
						.map(
							(e) => `
                                <div class="experience">
                                    <strong>${e.role || ""} - ${e.company || ""}</strong>
                                    <p>${e.description || ""}</p>
                                    <small>${e.duration || ""}</small>
                                </div>
                            `,
						)
						.join("")
				: "<p><em>No experience added</em></p>";

		container.innerHTML = `
            <h2>${data.name || "Unnamed"}</h2>
            <div class="email">${data.email || ""}</div>

            <div class="section">
                <h3>Summary</h3>
                <p>${data.summary || "<em>No summary provided</em>"}</p>
            </div>

            <div class="section">
                <h3>Skills</h3>
                <div class="skills">${skillsHTML}</div>
            </div>

            <div class="section">
                <h3>Projects</h3>
                ${projectsHTML}
            </div>

            <div class="section">
                <h3>Experience</h3>
                ${expHTML}
            </div>
        `;
	} catch (err) {
		container.innerHTML = "<p>Error loading profile</p>";
	}
}

// ================= BUTTON EVENTS =================
if (printBtn) {
	printBtn.addEventListener("click", () => {
		window.print();
	});
}

if (shareBtn) {
	shareBtn.addEventListener("click", async () => {
		try {
			await navigator.clipboard.writeText(window.location.href);
			alert("Profile link copied!");
		} catch {
			alert("Unable to copy link");
		}
	});
}

// ================= INIT =================
document.addEventListener("DOMContentLoaded", loadProfile);
