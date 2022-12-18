/* eslint-disable no-undef */
import { fileURLToPath, URL } from "node:url";
import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return defineConfig({
    plugins: [vue()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    define: {
      __APP_ENV__: env,
    },
    server: {
      port: env.FRONTEND_PORT,
      host: env.FRONTEND_ADRESS,
      https: env.FRONTEND_PROTOCOL === "https",
    },
    test: {
      environment: "happy-dom",
    },
  });
});
