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


			var jobs = document.getElementsByClassName("job");
			if (jobs.length === 0) {
				document.getElementById("nojob").style.visibility = "visible";
				goto(domain+"/loadDashboard?UUID="+account.UUID);
			}
		} catch (e) {
			console.log(e);
		}
	}
};

function share(title, description, link) {
	var data = `${title}\n${description}\n\nلینک استخدامی : ${link}\nلینک ثبت‌نام در کاریاب : ${domain}`;
	navigator.share({
		text: data
	});
}