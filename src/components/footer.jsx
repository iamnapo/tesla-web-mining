import report from "../assets/report.pdf";

const Footer = () => (
	<footer id="footer">
		<section>
			<h2>{"Source code &amp; other relevant files!"}</h2>
			<dl className="alt">
				<dt>{"Website:"}</dt>
				<dd><a href="https://github.com/iamnapo/tesla-web-mining">{"https://github.com/iamnapo/tesla-web-mining"}</a></dd>
				<dt>{"Dataset:"}</dt>
				<dd><a href="https://github.com/iamnapo/tesla-web-mining/tree/main/dataset">{"https://github.com/iamnapo/tesla-web-mining/tree/main/dataset"}</a></dd>
				<dt>{"Scripts:"}</dt>
				<dd><a href="https://github.com/iamnapo/tesla-web-mining/tree/main/analysis-scripts">{"https://github.com/iamnapo/tesla-web-mining/tree/main/analysis-scripts"}</a></dd>
				<dt>{"Report:"}</dt>
				<dd><a href={report} download="report.pdf">{"report.pdf"}</a></dd>
			</dl>
		</section>
		<p className="copyright">
			{"Made with ❤️ by Napoleon & Mary using "}
			<a href="https://github.com/codebushi/gatsby-starter-stellar">{"Gatsby.js"}</a>
		</p>
	</footer>
);

export default Footer;
