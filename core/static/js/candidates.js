// // ================= CANDIDATES SCRIPT =================

// // ================= CSRF =================
// function getCookie(name) {
// 	let cookieValue = null;
// 	if (document.cookie && document.cookie !== "") {
// 		const cookies = document.cookie.split(";");
// 		for (let cookie of cookies) {
// 			cookie = cookie.trim();
// 			if (cookie.startsWith(name + "=")) {
// 				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
// 				break;
// 			}
// 		}
// 	}
// 	return cookieValue;
// }

// // ================= SHORTLIST =================

// // Add / Remove toggle
// async function toggleShortlist(candidateId, btn) {
// 	try {
// 		const isShortlisted = btn.classList.contains("shortlisted");

// 		const url = isShortlisted ? "/api/shortlist/remove/" : "/api/shortlist/add/";

// 		const res = await fetch(url, {
// 			method: "POST",
// 			headers: {
// 				"Content-Type": "application/json",
// 				"X-CSRFToken": getCookie("csrftoken"),
// 			},
// 			body: JSON.stringify({ candidate_id: candidateId }),
// 		});

// 		// ✅ FIX: API validation
// 		if (!res.ok) {
// 			throw new Error("API error");
// 		}

// 		// Update UI
// 		if (isShortlisted) {
// 			btn.classList.remove("shortlisted");
// 			btn.innerText = "Add to Shortlist";
// 			btn.style.background = "#4caf50";
// 		} else {
// 			btn.classList.add("shortlisted");
// 			btn.innerText = "Remove from Shortlist";
// 			btn.style.background = "#e53935";
// 		}
// 	} catch (err) {
// 		alert("Something went wrong");
// 	}
// }

// // ================= BIND BUTTONS =================

// document.addEventListener("DOMContentLoaded", () => {
// 	const buttons = document.querySelectorAll(".shortlist-btn");

// 	buttons.forEach((btn) => {
// 		const candidateId = btn.getAttribute("data-id");

// 		if (!candidateId) return;

// 		btn.addEventListener("click", () => {
// 			toggleShortlist(candidateId, btn);
// 		});
// 	});
// });
