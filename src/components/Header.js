import React from "react";

const Header = () => (
	<header id="header" className="alt">
		<h1>#Tesla Twitter Content Analysis</h1>
		<p>
			{"Part 2 of the Web Data Mining course, by "}
			<a href="mailto:onapoleon@csd.auth.gr">Napoleon-Christos Oikonomou</a>
			{" & "}
			<a href="mailto:mvkouvela@csd.auth.gr">Maria Kouvela</a>
			{"."}
		</p>
		<br />
		<strong><em style={{ fontSize: "1.5rem" }}>Hint: Plots are interactive!</em></strong>
	</header>
);

export default Header;
