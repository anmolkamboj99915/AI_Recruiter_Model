// ================= RECRUITER SCRIPT =================

// ================= CSRF HELPER =================
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

// ================= USER =================
// ✅ FIX 1: safe access
const recruiterId = localStorage.getItem("user_id") || document.body?.getAttribute("data-user-id");

// ================= LOAD =================
async function loadCandidates() {
	try {
		const res = await fetch("/api/candidates/");

		// ✅ FIX 2: response validation
		if (!res.ok) throw new Error("API error");

		const data = await res.json();

		renderCandidates(data.candidates || [], data.shortlisted || []);
	} catch (err) {
		console.error("Error loading candidates");
	}
}

// ================= RENDER =================
function renderCandidates(candidates, shortlistedIds) {
	const container = document.getElementById("candidateList");

	// prevent crash
	if (!container) return;

	container.innerHTML = `<h2 class="title">All Candidates</h2>`;

	candidates.forEach((c) => {
		const isShortlisted = shortlistedIds.includes(c.id);

		const card = document.createElement("div");
		card.className = "card";

		card.innerHTML = `
			<h3>${c.name || "Unnamed"}</h3>
	
			<p class="summary">
				${c.summary || "<em>No summary available</em>"}
			</p>
	
			<div class="skills">
				<strong>Skills:</strong><br />
				${(c.skills || []).map((s) => `<span>${s}</span>`).join("")}
			</div>
	
			<div style="margin-top: 15px">
				<a href="/candidate/${c.id}/" class="btn btn-secondary">
					View Profile
				</a>
	
				<button 
					class="btn btn-primary shortlist-btn"
					data-id="${c.id}"
					data-shortlisted="${isShortlisted}"
				>
					${isShortlisted ? "Remove" : "Shortlist"}
				</button>
			</div>
		`;

		container.appendChild(card);
	});

	attachEvents();
}

// ================= SHORTLIST =================
async function shortlistCandidate(button, candidateId) {
	try {
		button.innerText = "Shortlisting...";
		button.disabled = true;

		const res = await fetch("/api/shortlist/", {
			// ✅ FIXED
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": getCookie("csrftoken"),
			},
			body: JSON.stringify({
				candidate_id: candidateId,
			}),
		});

		if (!res.ok) throw new Error("API error");

		button.innerText = "Remove from Shortlist";
		button.dataset.shortlisted = "true";
		button.disabled = false;
	} catch {
		button.innerText = "Add to Shortlist";
		button.disabled = false;
		alert("Error shortlisting");
	}
}

// ================= REMOVE =================
async function removeShortlist(button, candidateId) {
	try {
		button.innerText = "Removing...";
		button.disabled = true;

		const res = await fetch("/api/shortlist/remove/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": getCookie("csrftoken"),
			},
			body: JSON.stringify({
				candidate_id: candidateId,
			}),
		});

		if (!res.ok) throw new Error("API error");

		button.innerText = "Add to Shortlist";
		button.dataset.shortlisted = "false";
		button.disabled = false;
	} catch {
		button.innerText = "Remove from Shortlist";
		button.disabled = false;
		alert("Error removing shortlist");
	}
}

// ================= EVENTS =================
function attachEvents() {
	const buttons = document.querySelectorAll(".shortlist-btn");

	buttons.forEach((btn) => {
		const candidateId = parseInt(btn.getAttribute("data-id"));

		if (!candidateId) return;

		btn.addEventListener("click", () => {
			const isShortlisted = btn.dataset.shortlisted === "true";

			if (isShortlisted) {
				removeShortlist(btn, candidateId);
			} else {
				shortlistCandidate(btn, candidateId);
			}
		});
	});
}

// ================= INIT =================
document.addEventListener("DOMContentLoaded", loadCandidates);
