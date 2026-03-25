const form = document.getElementById("registerForm");
const errorDiv = document.getElementById("error");
const btn = document.getElementById("registerBtn");

// ✅ FIX 1: prevent crash if form missing
if (form) {
	form.addEventListener("submit", async (e) => {
		e.preventDefault();

		const name = document.getElementById("name")?.value?.trim();
		const email = document.getElementById("email")?.value?.trim();
		const password = document.getElementById("password")?.value;
		const confirm = document.getElementById("confirm")?.value;
		const role = document.getElementById("role")?.value;

		if (errorDiv) errorDiv.innerText = "";

		if (!name || !email || !password || !confirm || !role) {
			if (errorDiv) errorDiv.innerText = "Please fill all fields";
			return;
		}

		if (password !== confirm) {
			if (errorDiv) errorDiv.innerText = "Passwords do not match";
			return;
		}

		if (btn) {
			btn.innerText = "Registering...";
			btn.disabled = true;
		}

		try {
			const res = await fetch("/api/register/", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ name, email, password, role }),
			});

			// ✅ FIX 2: safe JSON handling
			let data = {};
			try {
				data = await res.json();
			} catch {
				data = {};
			}

			if (!res.ok) {
				if (errorDiv) {
					errorDiv.innerText = data.error || "Registration failed";
				}

				if (btn) {
					btn.disabled = false;
					btn.innerText = "Register";
				}

				return;
			}

			alert("Registered successfully!");
			window.location.href = "/login/";
		} catch (err) {
			if (errorDiv) {
				errorDiv.innerText = "Something went wrong";
			}

			if (btn) {
				btn.disabled = false;
				btn.innerText = "Register";
			}
		}
	});
}
