import "./styles.scss";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// font awesome icons
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faBars,
  faChartLine,
  faHome,
  faHourglass,
  faListCheck,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faCalendarCheck,
  faCheckSquare,
} from "@fortawesome/free-regular-svg-icons";
library.add(
  faBars,
  faHome,
  faCalendarCheck,
  faHourglass,
  faListCheck,
  faChartLine,
  faCheckSquare
);

const app = createApp(App);
app.use(router);
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");
