import { ApolloClient, InMemoryCache } from "@apollo/client/core";
import { DefaultApolloClient } from "@vue/apollo-composable";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { createApp } from "vue";
import App from "./App.vue";
import "./assets/main.css";

const cache = new InMemoryCache();
const apolloClient = new ApolloClient({
  cache,
  uri: "http://127.0.0.1:8000/api/v1/country",
});

const app = createApp(App);
let headers = new Headers({ "Access-Control-Allow-Origin": "*" });
app.provide(DefaultApolloClient, apolloClient, headers);

app.mount("#app");
