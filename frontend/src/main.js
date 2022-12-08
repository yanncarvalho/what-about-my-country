import { ApolloClient, InMemoryCache } from "@apollo/client/core";
import { DefaultApolloClient } from "@vue/apollo-composable";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { createApp } from "vue";
import App from "./App.vue";
import "./assets/main.css";
import { graphQlUrl } from "./common/helpers";

const cache = new InMemoryCache({
  addTypename: false,
});

const apolloClient = new ApolloClient({
  cache,
  uri: graphQlUrl,
});

const app = createApp(App);
app.provide(DefaultApolloClient, apolloClient);

app.mount("#app");
