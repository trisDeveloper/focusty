import "./styles.scss";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8000";

// font awesome icons
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faBars,
  faCalendarDays,
  faChartLine,
  faHome,
  faHourglass,
  faListCheck,
  faPencil,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faCalendarCheck,
  faCheckSquare,
  faTrashCan,
} from "@fortawesome/free-regular-svg-icons";
library.add(
  faBars,
  faHome,
  faCalendarCheck,
  faHourglass,
  faListCheck,
  faChartLine,
  faCheckSquare,
  faPencil,
  faCalendarDays,
  faTrashCan
);

const app = createApp(App);
app.use(router, axios, store);
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");
