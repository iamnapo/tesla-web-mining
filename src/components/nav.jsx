/* eslint-disable jsx-a11y/anchor-is-valid */
import Scrollspy from "react-scrollspy";

import Scroll from "./scroll.jsx";

const Nav = ({ sticky }) => (
	<nav id="nav" className={sticky ? "alt" : ""}>
		<Scrollspy items={["intro", "first", "second", "cta"]} currentClassName="is-active" offset={-300}>
			<li>
				<Scroll type="id" element="intro">
					<a href="#">{"Introduction"}</a>
				</Scroll>
			</li>
			<li>
				<Scroll type="id" element="first">
					<a href="#">{"Emerging Topic Detection"}</a>
				</Scroll>
			</li>
			<li>
				<Scroll type="id" element="second">
					<a href="#">{"Sentiment Analysis"}</a>
				</Scroll>
			</li>
			<li>
				<Scroll type="id" element="cta">
					<a href="#">{"Geo-location Analysis"}</a>
				</Scroll>
			</li>
		</Scrollspy>
	</nav>
);

export default Nav;
