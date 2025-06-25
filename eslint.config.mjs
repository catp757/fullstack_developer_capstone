import js from "@eslint/js";
import globals from "globals";
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
  // Node-specific config for backend/server files
  {
    files: ["server/database/**/*.js"],
    languageOptions: {
      globals: globals.node,
      ecmaVersion: 2021,
      sourceType: "script",
    },
    rules: {
      // Node-specific rules can go here
    },
  },
]);

