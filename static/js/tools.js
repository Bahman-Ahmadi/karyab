var domain = "http://karyab-bahman-ahmadi.vercel.app";

function makeDrawer() {
	var elems = document.querySelectorAll('.sidenav');
	var instances = M.Sidenav.init(elems);
}

function makeForm(mode) {
	if (mode == "signup") {
		document.getElementById("content").innerHTML = `
		<div class="form">
		<input type="text" id="name" class="field" required placeholder="نام و نام خانوادگی"/><br/>
		<input type="email" id="mail" class="field" required placeholder="آدرس ایمیل"/><br/>
		<input type="password" id="password" class="field" required placeholder="رمز عبور"/><br/>
		<input type="number" id="age" class="field" required placeholder="سن"/><br/>
		<textarea id="skills" class="field materialize-textarea" required placeholder="مهارت ها"></textarea><br/>
		<button id="check" onclick="signingUp(this.parentNode)">بــررســـی اطـلاعـــــات</button>
		<button id="changeMode" onclick="makeForm('login')">قبلا حساب ساختید؟ (ورود)</button>
		</div>
		`;
	} else if (mode == "login") {
		document.getElementById("content").innerHTML = `
		<div class="form">
		<input type="email" id="mail" class="field" required placeholder="آدرس ایمیل"/><br/>
		<input type="password" id="password" class="field" required placeholder="رمز عبور"/><br/>
		<button id="check" onclick="logingIn(this.parentNode)">بــررســـی اطـلاعـــــات</button>
		<button id="changeMode" onclick="makeForm('signup')">حساب ندارید؟ (ثبت‌نام)</button>
		</div>
		`;
	}
}

function goto(link) {
	document.body.innerHTML += `<a href="${link}" id="clickme"></a>`;
	document.getElementById("clickme").click();
}

function toast(text, time) {
	document.getElementById("BoxToastBox").innerHTML = `<div id='toastBox'>${text}</div>`;
	var x = document.getElementById("toastBox");
	x.className = "show";
	setTimeout(function () {
		x.className = x.className.replace("show", "");
	}, time);
}

async function sleep(ms) {
	return await new Promise(resolve => setTimeout(resolve, ms));
}
