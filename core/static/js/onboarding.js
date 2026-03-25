// ================= ONBOARDING SCRIPT =================

// ================= ELEMENTS =================
const roleEl = document.getElementById("role");
const skillsSection = document.getElementById("skillsSection");
const companySection = document.getElementById("companySection");
const startBtn = document.getElementById("startBtn");
const statusEl = document.getElementById("status");
const errorEl = document.getElementById("errorMsg");

// ================= INIT ROLE STATE =================
function updateRoleUI() {
	if (!roleEl) return;

	if (roleEl.value === "recruiter") {
		if (skillsSection) skillsSection.style.display = "none";
		if (companySection) companySection.style.display = "block";
	} else {
		if (skillsSection) skillsSection.style.display = "block";
		if (companySection) companySection.style.display = "none";
	}
}

// ✅ FIX 1: null safety for roleEl
if (roleEl) {
	roleEl.addEventListener("change", updateRoleUI);
	updateRoleUI();
}

// ================= SUBMIT =================
if (startBtn) {
	startBtn.addEventListener("click", async () => {
		const name = document.getElementById("name")?.value?.trim();
		const email = document.getElementById("email")?.value?.trim();
		const role = roleEl?.value;

		// RESET
		if (errorEl) errorEl.innerText = "";

		if (!name || !email) {
			if (errorEl) errorEl.innerText = "Please fill all required fields";
			return;
		}

		startBtn.disabled = true;
		startBtn.innerText = "Saving...";
		if (statusEl) statusEl.innerText = "";

		let payload = {
			name,
			email,
			role,
		};

		// Candidate
		if (role === "candidate") {
			const skillsInput = document.getElementById("skills");
			payload.skills = skillsInput?.value
				? skillsInput.value
						.split(",")
						.map((s) => s.trim())
						.filter(Boolean)
				: [];
		}

		// Recruiter
		if (role === "recruiter") {
			const companyInput = document.getElementById("company");
			payload.company = companyInput?.value?.trim() || "";
		}

		try {
			const res = await fetch("/api/onboarding/", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(payload),
			});

			// ✅ FIX 2: response validation
			if (!res.ok) {
				throw new Error("Onboarding failed");
			}

			const data = await res.json();

			// ✅ FIX 3: safe storage
			if (data?.user_id) {
				localStorage.setItem("user_id", data.user_id);
			}

			if (statusEl) statusEl.innerText = "Saved ✓ Redirecting...";

			setTimeout(() => {
				window.location.href = "/dashboard/";
			}, 1000);
		} catch (err) {
			if (statusEl) statusEl.innerText = "Error saving data";

			startBtn.disabled = false;
			startBtn.innerText = "Continue →";
		}
	});
}
