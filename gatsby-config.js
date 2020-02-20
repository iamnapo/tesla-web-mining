module.exports = {
	siteMetadata: {
		title: "Twitter Project of Web Data Mining course",
		author: "Maria Kouvela, Napoleon-Christos Oikonomou",
		description: "Demonstration of our Twitter Project of Web Data Mining course",
	},
	plugins: [
		"gatsby-plugin-react-helmet",
		{
			resolve: "gatsby-plugin-manifest",
			options: {
				name: "Twitter Project of Web Data Mining course",
				short_name: "Web Data Minging",
				start_url: "/",
				background_color: "#663399",
				theme_color: "#663399",
				display: "minimal-ui",
				icon: "src/assets/images/website-icon.png",
			},
		},
		"gatsby-plugin-sass",
		"gatsby-plugin-offline",
	],
};
