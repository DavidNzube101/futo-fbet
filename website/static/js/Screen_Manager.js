// ScreenManager.js
console.log(`[INFO]: Loaded page to screen ${current_screen}`)

const screen_definitions = {
	"1": ["home-screen", "home-tab"] ,
	"2": ["bet-screen", "bet-tab"] ,
	"3": ["account-screen", "account-tab"] ,
	"4": ["help-screen", ""]
}

function loadScreen(screen_id) {
	try {
		const screens = document.querySelectorAll(".screen")
		screens.forEach( screen => {
			screen.style.display = 'none'
		})
		const tabs = document.querySelectorAll(`.tab`)
		tabs.forEach( tab => {
			tab.className = "tab"
		})
		document.querySelector(`#${screen_definitions[screen_id][0]}`).style.display = 'block'
		try {
			document.querySelector(`#${screen_definitions[screen_id][1]}`).className = 'tab nav-tab active active-tab'
		} catch(e) {
			console.log(`Doesn't have a trigger button\n${e}`);
		}
		console.log(`[INFO]: Loaded page to screen 👇\nScreen ID: ${screen_id}\nScreen Name: ${screen_definitions[screen_id][0]}`)
	} catch(e) {
		console.log(`Invalid Screen ID\n${e}`);
	}
}

function goToScreen (element, screen_id, display_property) {
	const screens = document.querySelectorAll(".screen")
	screens.forEach( screen => {
		screen.style.display = 'none'
	})
	const tabs = document.querySelectorAll(`.${element.className}`)
	tabs.forEach( tab => {
		// tab.style.borderBottom = '0'
		tab.className = "tab"
	})
	document.querySelector(`#${screen_id}`).style.display = display_property.includes('-das') ? "block" : `${display_property}`
	// element.style.borderBottom = "2px solid #00a8f3"
	if (display_property.includes('-das')) {
		// nothing
	} else {
		element.className = "tab active-tab"
	}
}