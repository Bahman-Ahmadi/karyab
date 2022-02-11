document.body.onload = async function(e) {
	makeDrawer();
	var loader = document.getElementById("loader");
	var account = localStorage.getItem("account");
	await sleep(1250);
	loader.style.visibility = "hidden";
	if (account == undefined) {
		toast("شما حساب کاربری ندارید", 2500);
		await sleep(1500);
		goto("/register");
	} else {
		try {
			account = JSON.parse(account.replace(/\'/g, '"'));
			document.getElementById("name").innerHTML = account.name;
			document.getElementById("email").innerHTML = account.email;

			var UUID_Box = document.getElementById("UUID");
			UUID_Box.innerHTML = account.UUID;
			UUID_Box.onclick = () => {
				var copying = navigator.clipboard.writeText(account.UUID);
				toast('شناسهٔ کاربری شما کپی شد', 2500);
			};

			var titles = document.getElementsByClassName("right");
			var checkboxes = document.getElementsByClassName("left");

			for (var checkbox = 0; checkbox < checkboxes.length; checkbox++) {
				if (account.nonAllowedSites.split(",").indexOf(titles[checkbox].innerHTML) == -1) {
					checkboxes[checkbox].checked = true;
				} else {
					checkboxes[checkbox].checked = false;
				}
			}

		} catch (e) {
			console.log(e);
		}
	}
};
function editSite(sitename) {
	var account = localStorage.getItem("account");
	account = JSON.parse(account.replace(/\'/g, '"'));

	let xhr = new XMLHttpRequest();

	xhr.onreadystatechange = async function (e) {
		if (this.readyState == 4 && this.status == 200) {
			if (this.responseText.indexOf("{") != -1) {
				localStorage.setItem("account", this.responseText);
				toast("تغییرات اعمال شدند", 1500);
			} else {
				toast("مجدداً تلاش کنید", 2500);
			}
		}
	};
	xhr.onerror = function (e) {
		document.getElementById("check").click();
	};

	xhr.open("GET", `${domain}/editSite?UUID=${account.UUID}&site=${sitename}`);
	xhr.send();

}