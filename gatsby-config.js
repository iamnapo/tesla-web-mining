module.exports = {
	siteMetadata: {
		siteUrl: "https://www.tesla.iamnapo.me",
		title: "Twitter Project of Web Data Mining course",
		author: "Maria Kouvela, Napoleon-Christos Oikonomou",
		description: "Demonstration of our Twitter Project of Web Data Mining course",
	},
	plugins: [
		"gatsby-plugin-sass",
		"gatsby-plugin-react-helmet",
		"gatsby-plugin-sitemap",
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
		"gatsby-plugin-offline",
		"gatsby-plugin-netlify",
	],
};
