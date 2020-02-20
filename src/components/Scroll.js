import smoothscroll from "smoothscroll-polyfill";
import React from "react";

const Element = (props) => (props.children);

class Scroll extends React.Component {
	constructor() {
		super();
		this.handleClick = this.handleClick.bind(this);
	}

	componentDidMount() {
		smoothscroll.polyfill();
	}

	handleClick(e) {
		e.preventDefault();
		let elem = 0;
		let scroll = true;
		const { type, element, offset, timeout } = this.props;
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
			this.scrollTo(elem, offset, timeout);
		} else {
			console.log(`Element not found: ${element}`);
		}
	}

	scrollTo(element, offSet = 0, timeout = null) {
		const elemPos = element ? element.getBoundingClientRect().top + window.pageYOffset : 0;
		if (timeout) {
			setTimeout(() => { window.scroll({ top: elemPos + offSet, left: 0, behavior: "smooth" }); }, timeout);
		} else {
			window.scroll({ top: elemPos + offSet, left: 0, behavior: "smooth" });
		}
	}

	render() {
		return (
			<Element>
				{typeof (this.props.children) === "object" ? (
					React.cloneElement(this.props.children, { onClick: this.handleClick })
				) : (
					<span tabIndex={0} onKeyPress={this.handleClick} role="button" onClick={this.handleClick}>{this.props.children}</span>
				)}
			</Element>
		);
	}
}

export default Scroll;
