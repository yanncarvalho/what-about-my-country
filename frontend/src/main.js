import { ApolloClient, InMemoryCache } from "@apollo/client/core";
import { DefaultApolloClient } from "@vue/apollo-composable";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { createApp } from "vue";
import App from "./App.vue";
import "./assets/main.css";

// eslint-disable-next-line no-undef
const config = APPLICATION_CONFIG;

const cache = new InMemoryCache({
  addTypename: false,
});
const apolloClient = new ApolloClient({
  cache,
  uri: config.BACKEND.COUNTRY_URL,
});
const app = createApp(App);
app.provide(DefaultApolloClient, apolloClient);
app.provide("application_config", config);

app.mount("#app");
