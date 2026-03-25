// ================= AI BUILDER SCRIPT =================

// ================= CSRF =================
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let cookie of cookies) {
			cookie = cookie.trim();
			if (cookie.startsWith(name + "=")) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
			}
		}
	}
	return cookieValue;
}

// ================= ELEMENTS =================
const textarea = document.querySelector("textarea[name='text']") || document.getElementById("projectText");

const loadingEl = document.getElementById("loading");

// ✅ FIXED container
let resultContainer = document.getElementById("projectResult") || document.getElementById("dynamicResult");

if (!resultContainer) {
	resultContainer = document.createElement("div");
	resultContainer.id = "dynamicResult";
	resultContainer.className = "result";
	document.body.appendChild(resultContainer);
}

// ================= FORM INTERCEPT =================
const form = document.getElementById("aiForm");

if (form) {
	form.addEventListener("submit", function (e) {
		e.preventDefault();

		const text = textarea?.value?.trim();

		if (!text) {
			alert("Please describe your project first.");
			return;
		}

		generateAI(text);
	});
}

// ================= AI CALL =================
async function generateAI(text) {
	try {
		if (loadingEl) loadingEl.style.display = "block";
		resultContainer.innerHTML = "";

		const res = await fetch("/api/ai/project/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": getCookie("csrftoken"),
			},
			body: JSON.stringify({ text }),
		});

		// ✅ FIX: response validation
		if (!res.ok) {
			throw new Error("API error");
		}

		const data = await res.json();

		renderResult(data);
	} catch (err) {
		resultContainer.innerHTML = "<p style='color:red;'>Error generating AI response</p>";
	} finally {
		if (loadingEl) loadingEl.style.display = "none";
	}
}

// ================= RENDER =================
function renderResult(data) {
	const techHTML = (data.tech || []).map((t) => `<span style="background:#e8f5e9;padding:5px 10px;border-radius:12px;margin-right:5px;font-size:12px;">${t}</span>`).join("");

	resultContainer.innerHTML = `
        <h3>AI Generated Project</h3>
        <p><strong>Title:</strong> ${data.title || "N/A"}</p>
        <p><strong>Description:</strong> ${data.description || "N/A"}</p>
        <div><strong>Tech:</strong> ${techHTML}</div>
        <button onclick="useGeneratedProject()">Use this project</button>
    `;
}

// ================= OPTIONAL =================
function useGeneratedProject() {
	alert("Project ready!");
}

// ================= AI PROFILE BUILDER =================

const aiBuildBtn = document.getElementById("aiBuildBtn");
const aiInput = document.getElementById("aiInput");
const aiProfileResult = document.getElementById("aiProfileResult");

if (aiBuildBtn) {
	aiBuildBtn.addEventListener("click", async () => {
		const text = aiInput?.value?.trim();

		if (!text) {
			alert("Please describe your profile");
			return;
		}

		aiProfileResult.innerHTML = "Generating AI profile...";

		try {
			const res = await fetch("/api/ai/profile/", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": getCookie("csrftoken"),
				},
				body: JSON.stringify({ text }),
			});

			// ✅ FIX: response validation
			if (!res.ok) {
				throw new Error("API error");
			}

			const data = await res.json();

			renderAIProfile(data);
		} catch {
			aiProfileResult.innerHTML = "<p style='color:red;'>Error generating profile</p>";
		}
	});
}

function renderAIProfile(data) {
	// ✅ FIX: safe access
	const projectTitle = data.project?.title || "N/A";
	const experienceRole = data.experience?.role || "N/A";
	const experienceCompany = data.experience?.company || "N/A";

	aiProfileResult.innerHTML = `
        <h3>AI Generated Profile</h3>

        <p><strong>Summary:</strong> ${data.summary || ""}</p>

        <p><strong>Skills:</strong> ${(data.skills || []).join(", ")}</p>

        <p><strong>Project:</strong> ${projectTitle}</p>

        <p><strong>Experience:</strong> ${experienceRole} at ${experienceCompany}</p>

        <button onclick="applyAIProfile()">Use This Profile</button>
    `;

	window.generatedAIProfile = data;
}

function applyAIProfile() {
	if (!window.generatedAIProfile) return;

	const summaryEl = document.getElementById("summary");
	const skillsEl = document.getElementById("skills");

	// ✅ FIX: null safety
	if (summaryEl) {
		summaryEl.value = window.generatedAIProfile.summary || "";
	}

	if (skillsEl) {
		skillsEl.value = (window.generatedAIProfile.skills || []).join(", ");
	}

	alert("AI data applied to profile!");
}
