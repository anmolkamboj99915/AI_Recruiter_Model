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

document.addEventListener("DOMContentLoaded", () => {
	const form = document.getElementById("loginForm");

	if (!form) return;

	form.addEventListener("submit", async (e) => {
		e.preventDefault();

		const email = form.querySelector("input[name='email']").value;
		const password = form.querySelector("input[name='password']").value;
		const btn = document.getElementById("loginBtn");

		try {
			if (btn) {
				btn.innerText = "Logging in...";
				btn.disabled = true;
			}

			const res = await fetch("/api/login/", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": getCookie("csrftoken"),
				},
				body: JSON.stringify({ email, password }),
			});

			const data = await res.json();

			if (!res.ok) {
				alert(data.error || "Login failed");

				if (btn) {
					btn.innerText = "Login";
					btn.disabled = false;
				}
				return;
			}

			localStorage.setItem("user_id", data.user.id);

			window.location.href = "/dashboard/";
		} catch (err) {
			alert("Server error");

			if (btn) {
				btn.innerText = "Login";
				btn.disabled = false;
			}
		}
	});
});
