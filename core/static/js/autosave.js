// ================= AUTO SAVE SYSTEM =================

// ================= CSRF =================
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let cookie of cookies) {
			cookie = cookie.trim();
			if (cookie.startsWith(name + "=")) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

// ================= ELEMENTS =================
const summaryEl = document.getElementById("summary");
const skillsEl = document.getElementById("skills");
const progressBar = document.getElementById("progressBar");

// ================= STATUS =================
let statusEl = document.getElementById("saveStatus");

if (!statusEl) {
	statusEl = document.createElement("div");
	statusEl.id = "saveStatus";
	statusEl.style.fontSize = "12px";
	statusEl.style.color = "#666";
	statusEl.style.marginBottom = "10px";

	if (progressBar && progressBar.parentNode) {
		progressBar.parentNode.appendChild(statusEl);
	}
}

// ================= USER ID =================
let userId = localStorage.getItem("user_id");

if (!userId) {
	const bodyUserId = document.body?.getAttribute("data-user-id");
	if (bodyUserId) {
		userId = bodyUserId;
		localStorage.setItem("user_id", userId);
	}
}

// ================= CACHE =================
let lastPayload = "";

// ================= DATA =================
function collectData() {
	const skills = skillsEl?.value
		? skillsEl.value
				.split(",")
				.map((s) => s.trim())
				.filter(Boolean)
		: [];

	// ✅ FIX: collect project (future ready)
	const projects = [];

	// ✅ FIX: collect experience
	const companyEl = document.getElementById("company");
	const roleEl = document.getElementById("role");
	const durationEl = document.getElementById("duration");
	const expDescEl = document.getElementById("expDesc");

	const experiences = [];

	if (companyEl?.value || roleEl?.value || expDescEl?.value) {
		experiences.push({
			company: companyEl?.value || "",
			role: roleEl?.value || "",
			duration: durationEl?.value || "",
			description: expDescEl?.value || "",
		});
	}

	return {
		user_id: userId,
		summary: summaryEl?.value || "",
		skills,
		projects,
		experiences,
	};
}

// ================= SAVE =================
async function autoSave() {
	if (!userId) return;

	const payload = collectData();
	const payloadStr = JSON.stringify(payload);

	if (payloadStr === lastPayload) return;

	lastPayload = payloadStr;

	try {
		statusEl.innerText = "Saving...";

		const res = await fetch("/api/profile/save/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": getCookie("csrftoken"),
			},
			body: payloadStr,
		});

		if (!res.ok) {
			throw new Error("Save failed");
		}

		const data = await res.json();

		statusEl.innerText = "Saved ✓";

		if (progressBar && typeof data.completion === "number") {
			progressBar.style.width = data.completion + "%";
		}
	} catch {
		statusEl.innerText = "Error saving";
	}
}

// ================= INTERVAL =================
if (summaryEl || skillsEl) {
	setInterval(autoSave, 6000);
}

// ================= INPUT EVENTS =================
[summaryEl, skillsEl].forEach((el) => {
	if (!el) return;

	el.addEventListener("input", () => {
		statusEl.innerText = "Typing...";
	});
});
