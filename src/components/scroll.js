import * as React from "react";

const Element = (props) => (props.children);

const Scroll = ({ type, element, offset = 0, timeout, children }) => {
	const handleClick = (e) => {
		e.preventDefault();
		let elem = 0;
		let scroll = true;
		if (type && element) {
			switch (type) {
				case "class":
					elem = document.querySelectorAll(`.${element}`)[0];
					scroll = !!elem;
					break;
				case "id":
					elem = document.querySelector(`#${element}`);
					scroll = !!elem;
					break;
				default:
			}
		}

		if (scroll) {
			const elemPos = elem ? elem.getBoundingClientRect().top + window.pageYOffset : 0;
			if (timeout) {
				setTimeout(() => { window.scroll({ top: elemPos + offset, left: 0, behavior: "smooth" }); }, timeout);
			} else {
				window.scroll({ top: elemPos + offset, left: 0, behavior: "smooth" });
			}
		} else {
			console.log(`Element not found: ${element}`);
		}
	};

	return (
		<Element>
			{typeof (children) === "object" ? (
				React.cloneElement(children, { onClick: handleClick })
			) : (
				<span tabIndex={0} role="button" onKeyPress={handleClick} onClick={handleClick}>{children}</span>
			)}
		</Element>
	);
};

export default Scroll;
