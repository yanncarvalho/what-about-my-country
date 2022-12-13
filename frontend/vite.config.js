import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { config } from "./config";
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  define: {
    APPLICATION_CONFIG: config,
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
