import eslintConfigIamnapo from "eslint-config-iamnapo";

/** @type {import('eslint').Linter.Config} */
const config = [
	...eslintConfigIamnapo.configs.react.map((cfg) => ({
		...cfg,
		files: [eslintConfigIamnapo.filePatterns.react],
	})),
	{
		rules: {
			"react/prop-types": "off",
		},
	},
	{ ignores: ["analysis-scripts", "dataset", "public"] },
];

export default config;
