import './styles.scss'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Cookies from 'js-cookie'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import VCalendar from 'v-calendar'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import 'v-calendar/style.css'

//axios
axios.defaults.baseURL = import.meta.env.VITE_BASE_URL
axios.defaults.headers['Content-Type'] = 'application/json'
axios.interceptors.request.use(
  (config) => {
    const token = Cookies.get('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

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
  faPencil,
  faRepeat,
  faChevronRight,
  faChevronLeft
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
  faForwardStep,
  faRepeat,
  faChevronRight,
  faChevronLeft
)
const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router, axios)
app.use(VCalendar, {})
app.component('font-awesome-icon', FontAwesomeIcon)
app.component('VueDatePicker', VueDatePicker)
app.mount('#app')

export { pinia }
