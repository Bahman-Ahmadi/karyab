document.body.onload = async function(e) {
	makeDrawer();
	var loader = document.getElementById("loader");
	await sleep(1250);
	loader.style.visibility = "hidden";

	var account = localStorage.getItem("account");
	switch (account) {
		case null:
			makeForm("signup");
			break;

		default:
			goto("/dashboard");
			break;
	}
};

function signingUp(parent) {
	var children = [];
	for (var i of parent.childNodes) {
		i.required?children.push(i): null;
	}
	for (var j of parent.childNodes) {
		if (j.required) {
			var index = children.indexOf(j);
			if (j.value == "") {
				toast("لطفا اطلاعات را تکمیل کنید", 2500);
				return null;
			}
			if (index == 0 && !(j.value.split(" ").length > 1)) {
				toast("لطفا نام و نام خانوادگی را وارد کنید", 2500);
				return null;
			} if (index == 2 && !(j.value.replace(/\d/g, "") != i.value)) {
				toast("لطفا رمزعبور قوی (همراه با اعداد) وارد کنید", 2500);
				return null;
			} if (index == 3 && !(j.value.length == 2)) {
				toast("لطفا سن حقیقی خود را وارد کنید", 2500);
				return null;
			} if (index == 4 && !(j.value.split(",").length > 1)) {
				toast("لطفا مهارت های خود را با ',' از هم جدا کنید", 2500);
				return null;
			}
		}
	}
	loader.style.visibility = "visible";
	toast("لطفا اندکی صبر کنید...", 2500);

	let xhr = new XMLHttpRequest();

	xhr.onreadystatechange = async function (e) {
		if (this.readyState == 4 && this.status == 200) {
			toast(this.responseText, 2500);
			await sleep(2500);
			loader.style.visibility = "hidden";
			goto("/");
			return;
		}
	};
	xhr.onerror = function (e) {
		document.getElementById("check").click();
	};

	xhr.open("GET", `${domain}/register?mode=signup&name=${children[0].value}&email=${children[1].value}&password=${children[2].value}&age=${children[3].value}&skills=${children[4].value}`);
	xhr.send();
}

function logingIn(parent) {
	var children = [];
	for (var i of parent.childNodes) {
		i.required?children.push(i): null;
	}
	loader.style.visibility = "visible";
	toast("لطفا اندکی صبر کنید...", 2500);

	let xhr = new XMLHttpRequest();

	xhr.onreadystatechange = async function (e) {
		if (this.readyState == 4 && this.status == 200) {
			if (this.responseText.indexOf("{") != -1) {
				var myHeaders = new Headers();
				myHeaders.set("UUID", JSON.parse(this.responseText.replace(/\'/g, '"')).UUID);
				localStorage.setItem("account", this.responseText);
				toast("با موفقیت به حسابتان وارد شدید", 2500);
			} else {
				toast(this.responseText, 2500);
			}
			await sleep(2500);
			loader.style.visibility = "hidden";
			goto("/dashboard");
			return;
		}
	};
	xhr.onerror = function (e) {
		console.log(e);
		document.getElementById("check").click();
	};

	xhr.open("GET", `${domain}/register?mode=login&email=${children[0].value}&password=${children[1].value}`);
	xhr.send();
}