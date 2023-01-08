import * as React from "react";

import "../assets/scss/main.scss";

import Footer from "./footer.jsx";

const Layout = ({ children }) => {
	const [loading, setLoading] = React.useState("is-loading");

	React.useEffect(() => {
		const timeout = setTimeout(() => {
			setLoading("");
		}, 100);
		return () => clearTimeout(timeout);
	});

	return (
		<div className={`body ${loading}`}>
			<div id="wrapper">
				{children}
				<Footer />
			</div>
		</div>
	);
};

export default Layout;
