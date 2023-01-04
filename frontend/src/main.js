import { ApolloClient, InMemoryCache } from "@apollo/client/core";
import { DefaultApolloClient } from "@vue/apollo-composable";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { createApp } from "vue";
import App from "./App.vue";
import "./assets/main.css";

const cache = new InMemoryCache({
  addTypename: false,
});

const _ = __APP_ENV__;
const apolloClient = new ApolloClient({
  cache,
  uri: `${_.BACKEND_PROTOCOL}://${_.BACKEND_ADDRESS}:${_.BACKEND_PORT}/${_.BACKEND_COUNTRY_ROUTE}`,
});

const app = createApp(App);
app.provide(DefaultApolloClient, apolloClient);

app.mount("#app");
