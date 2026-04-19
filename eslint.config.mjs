import { defineConfig, globalIgnores } from "eslint/config";
import eslintConfigIamnapo from "eslint-config-iamnapo";

const config = defineConfig([
	{
		extends: [eslintConfigIamnapo.configs.react],
		files: [eslintConfigIamnapo.filePatterns.react],
	},
	{
		rules: {
			"react/prop-types": "off",
		},
	},
	globalIgnores(["analysis-scripts", "dataset", "public"]),
]);

export default config;
