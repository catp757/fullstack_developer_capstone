import js from "@eslint/js";
import globals from "globals";
import pluginReact from "eslint-plugin-react";
import { defineConfig } from "eslint/config";

export default defineConfig([
  // General JS files (browser)
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    plugins: { js },
    extends: ["js/recommended"],
  },
  // Browser globals for general files
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    languageOptions: {
      globals: globals.browser,
    },
  },
  // React recommended config
  pluginReact.configs.flat.recommended,

  // Add this new override for Node files in server/database
  {
    files: ["server/database/**/*.js"],
    languageOptions: {
      globals: globals.node,       // Node.js globals like require, module, etc.
      ecmaVersion: 2021,
      sourceType: "script",        // Usually Node files use CommonJS syntax
    },
    rules: {
      // add or override rules specific to Node if you want
    },
  },
]);
