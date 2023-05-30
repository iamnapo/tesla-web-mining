export const onCreateWebpackConfig = ({ stage, loaders, actions }) => {
	if (stage === "build-html") {
		actions.setWebpackConfig({
			module: {
				rules: [
					{
						test: /plotly|mapbox/,
						use: loaders.null(),
					},
				],
			},
		});
	}
};
