<script setup>
import axios from 'axios'
import { useStore } from '@/stores'
import { computed, ref, onMounted } from 'vue'
import Sortable from 'sortablejs'
import tasklist from './../components/task-list.vue'
import taskCard from './../components/task-card.vue'
const store = useStore()
const props = defineProps(['filterdays'])
const today = new Date()
const tasks = ref([])

let nextTaskId = localStorage.getItem('nextTaskId') || 1

// resposive week view
const isWideScreen = ref(window.innerWidth >= 1075 || window.innerWidth <= 600)

const nextDays = computed(() => {
  const nextDays = []
  for (let i = 0; i < 7; i++) {
    const nextDay = new Date()
    nextDay.setDate(today.getDate() + i)
    nextDays.push({
      weekday: formatDatePart(nextDay, 'weekday'),
      month: formatDatePart(nextDay, 'month'),
      day: formatDatePart(nextDay, 'day'),
      date: nextDay.toISOString().split('T')[0]
    })
  }
  return nextDays
})

const displayedDays = computed(() => {
  if (props.filterdays) {
    const displayedDays = [nextDays.value[0]]
    displayedDays.forEach((day) => {
      day.tasks = getTasksForDate(day.date)
    })
    return displayedDays
  } else {
    const daysToDisplay = isWideScreen.value ? 7 : 4
    const displayedDays = nextDays.value.slice(0, daysToDisplay)
    displayedDays.forEach((day) => {
      day.tasks = getTasksForDate(day.date)
    })
    return displayedDays
  }
})
onMounted(() => {
  createSortableInstances()
  fetchData()
  moveTasksTodb()
})

const createSortableInstances = () => {
  for (let index = 0; index < displayedDays.value.length; index++) {
    const element = document.getElementById(index)
    Sortable.create(element, {
      group: 'shared',
      sort: false,
      animation: 150,
      ghostClass: 'none',
      chosenClass: 'none',
      dragClass: 'none',
      onEnd: (evt) => {
        let task = evt.item.id
        let date = displayedDays.value[evt.to.id].date
        dropTaskDate(task, date)
      }
    })
  }
}

const dropTaskDate = async (task, date) => {
  try {
    if (localStorage.getItem('userId')) {
      await axios.patch(`/api/users/${store.user.id}/tasks/${task}/`, { date: date })
    } else {
      const localTasks = JSON.parse(localStorage.getItem('tasks')) || []

      const updatedTaskIndex = localTasks.findIndex((t) => t.id == Number(task))
      if (updatedTaskIndex !== -1) {
        localTasks[updatedTaskIndex].date = date
        localStorage.setItem('tasks', JSON.stringify(localTasks))
      }
    }

    sortTasks()
  } catch (error) {
    // Handle errors
    console.error(error)
  }
  fetchData()
}
// date format    - thu feb 8 -
const formatDatePart = (date, part) => {
  const options = {
    weekday: 'short',
    month: 'short',
    day: 'numeric'
  }
  return date.toLocaleDateString('en-US', { [part]: options[part] })
}

// filter tasks per day
const getTasksForDate = (date) => {
  return tasks.value
    .filter((task) => task.date === date)
    .sort((a, b) => (a.done === b.done ? 0 : a.done ? 1 : -1))
}

// set colors per day
const getDayColor = (weekday) => {
  const colors = {
    Sun: '#ff8d84',
    Mon: '#ff9dd7',
    Tue: '#29ff7c',
    Wed: '#c4a3ff',
    Thu: '#8dc4ff',
    Fri: '#ffcf3f',
    Sat: '#ffff69'
  }
  return colors[weekday] || '#ddd'
}

const handleResize = () => {
  isWideScreen.value = window.innerWidth >= 1075 || window.innerWidth <= 600
}

// get tasks list from backend
const fetchData = () => {
  if (localStorage.getItem('userId')) {
    axios
      .get(`/api/users/${localStorage.getItem('userId')}/tasks/`)
      .then((response) => {
        tasks.value = response.data || []
        // Sort tasks after fetching
        sortTasks()
      })
      .catch((error) => {
        console.error(error)
      })
  } else {
    const localTasks = JSON.parse(localStorage.getItem('tasks')) || []
    tasks.value = localTasks
  }
}
const moveTasksTodb = async () => {
  try {
    const userId = localStorage.getItem('userId')
    if (userId) {
      const localTasks = JSON.parse(localStorage.getItem('tasks')) || []
      if (localTasks.length >= 1) {
        // Move tasks from local storage to database
        for (let i = 0; i < localTasks.length; i++) {
          localTasks[i].user = userId // Assign user ID to each task
          await axios.post(`/api/users/${userId}/tasks/`, localTasks[i])
        }
        localStorage.removeItem('tasks')
      }
    }
  } catch (error) {
    console.error('Error moving tasks to database:', error)
  }
}
const sortTasks = () => {
  tasks.value.sort((a, b) => {
    // If a task doesn't have a time, it comes first
    if (!a.time && !b.time) return 0
    if (!a.time) return -1
    if (!b.time) return 1
    // Sort based on time
    return a.time.localeCompare(b.time)
  })
}

const closeTaskCard = () => {
  store.setIsOpenCard(false)

  store.setSelectedTask({
    id: null,
    title: '',
    date: null,
    time: null,
    description: '',
    done: false
  })
  store.timepic = {
    hours: 0,
    minutes: 0
  }
  window.removeEventListener('click', closeTaskCard)
}

const saveTaskAndClose = async () => {
  try {
    if (store.selectedTask.title.trim() === '') {
      // If title is empty, do nothing
      closeTaskCard()
      return
    }
    if (localStorage.getItem('userId')) {
      if (store.selectedTask.id) {
        await axios.patch(
          `/api/users/${store.user.id}/tasks/${store.selectedTask.id}/`,
          store.selectedTask
        )
      } else {
        await axios.post(`/api/users/${store.user.id}/tasks/`, store.selectedTask)
      }
    } else {
      if (store.selectedTask.id) {
        const localTasks = JSON.parse(localStorage.getItem('tasks')) || []
        const existingTaskIndex = localTasks.findIndex((task) => task.id === store.selectedTask.id)
        if (existingTaskIndex !== -1) {
          // Task found, update its properties
          localTasks[existingTaskIndex] = store.selectedTask
        }
        localStorage.setItem('tasks', JSON.stringify(localTasks))
      } else {
        const localTasks = JSON.parse(localStorage.getItem('tasks')) || []
        store.selectedTask.id = String(nextTaskId++)
        localTasks.push(store.selectedTask)
        localStorage.setItem('tasks', JSON.stringify(localTasks))
        localStorage.setItem('nextTaskId', nextTaskId)
      }
    }

    closeTaskCard()
  } catch (error) {
    // Handle errors
    console.error(error)
  }
  fetchData()
}

const openTaskCard = (event, task, day) => {
  if (event.target.closest('.task-card')) {
    // Clicked inside the task card, don't trigger opening or closing
    return
  }
  if (event.target.classList.contains('checkbox')) {
    return
  }
  if (!task && !store.isopencard) {
    // create new task

    store.setSelectedTask({
      id: null,
      title: '',
      date: day.date,
      time: null,
      description: '',
      done: false,
      user: localStorage.getItem('userId') || null
    })
    store.setIsOpenCard(true)
  } else if (!task && store.isopencard) {
    saveTaskAndClose()
  } else if (task && !store.isopencard) {
    //update existing task
    store.setIsOpenCard(true)
    store.setSelectedTask({ ...task })
    if (store.selectedTask.time) {
      store.timepic = {
        hours: store.selectedTask.time.split(':')[0],
        minutes: store.selectedTask.time.split(':')[1]
      }
    }
  } else {
    saveTaskAndClose()
  }
  if (!store.isopencard) {
    window.addEventListener('click', closeTaskCard)
  } else {
    window.removeEventListener('click', closeTaskCard)
  }
}

window.addEventListener('resize', handleResize)
handleResize()
fetchData()
</script>

<template>
  <div class="container">
    <div class="calendar">
      <div v-for="(day, index) in displayedDays" :key="index" class="day">
        <div class="dayname">
          <div class="weekday" :style="{ color: getDayColor(day.weekday) }">
            {{ day.weekday }}
          </div>
          <div class="daynum">{{ day.month }} {{ day.day }}</div>
        </div>
        <div class="tasks" @click="openTaskCard($event, null, day)" :id="index">
          <tasklist
            v-for="task in day.tasks"
            :key="task.id"
            :id="task.id"
            :task="task"
            :fetchData="fetchData"
            @click.stop="openTaskCard($event, task, day)"
          >
          </tasklist>
          <taskCard :fetchData="fetchData" />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
@import './../styles.scss';
.none::before {
  display: none;
}
.container {
  max-width: 1500px;
  margin: 0 auto;
}

.calendar {
  display: flex;
  justify-content: center;
  flex-wrap: nowrap;
  flex-direction: row;
  min-height: calc(100vh - 65px);

  .day {
    width: calc(100% / 7);
    padding: 5px;
    border: 1px solid #ffffff0f;
    display: flex;
    flex-direction: column;

    .dayname {
      height: fit-content;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-direction: row;

      .weekday {
        padding: 5px;
        font-size: 19px;
      }

      .daynum {
        padding: 5px;
        font-size: 23px;
        color: #fff;
      }
    }
  }

  @media (max-width: 1075px) {
    .day {
      width: calc(100% / 4);
    }
  }
}

@media (max-width: 600px) {
  .calendar {
    flex-wrap: nowrap;
    flex-direction: column;
    justify-content: flex-start;

    .day {
      width: calc(100%);
      border-bottom: 1px solid #ffffff0f;
    }
  }
}
.tasks {
  padding: 5px;
  flex-grow: 1;
}
</style>
