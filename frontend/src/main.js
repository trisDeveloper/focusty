import './styles.scss'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import VCalendar from 'v-calendar'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import 'v-calendar/style.css'

axios.defaults.baseURL = 'https://trisdev.pythonanywhere.com'

// font awesome icons
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faBars,
  faCalendarDays,
  faChartLine,
  faForwardStep,
  faGear,
  faHome,
  faHourglass,
  faListCheck,
  faPause,
  faPencil
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faCalendarCheck,
  faCheckSquare,
  faClock,
  faTrashCan
} from '@fortawesome/free-regular-svg-icons'
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
  faTrashCan,
  faClock,
  faGear,
  faPause,
  faForwardStep
)

const app = createApp(App)

app.use(createPinia())
app.use(router, axios)
app.use(VCalendar, {})
app.component('font-awesome-icon', FontAwesomeIcon)
app.component('VueDatePicker', VueDatePicker)
app.mount('#app')
