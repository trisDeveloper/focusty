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
const saveThisOrAll = ref(false)
const deleteThisOrAll = ref(false)

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
    repeatParameters: null,
    repeatId: null,
    description: '',
    done: false
  })
  store.timepic = {
    hours: 0,
    minutes: 0
  }
  document.removeEventListener('click', openTaskCard)
}

const openThisOrAll = (action) => {
  if (action == 'delete') {
    setTimeout(() => {
      deleteThisOrAll.value = true
    }, 0)
  } else if (action == 'save') {
    setTimeout(() => {
      saveThisOrAll.value = true
    }, 0)
  }
  document.addEventListener('click', closeThisOrAll)
}
const closeThisOrAll = (event) => {
  if (deleteThisOrAll.value && !event?.target.closest('.thisOrAll')) {
    setTimeout(() => {
      deleteThisOrAll.value = false
    }, 0)
    document.removeEventListener('click', closeThisOrAll)
  } else if (saveThisOrAll.value && !event?.target.closest('.thisOrAll')) {
    setTimeout(() => {
      saveThisOrAll.value = false
    }, 0)
    document.removeEventListener('click', closeThisOrAll)
  }
}

const handleSaveThisOrAll = () => {
  const tasksWithSameRepeatId = tasks.value.filter(
    (t) => t.repeatId === store.selectedTask.repeatId
  )
  if (
    tasksWithSameRepeatId.length > 1 &&
    store.selectedTask.repeatId &&
    store.selectedTask.repeatParameters &&
    JSON.stringify(tasks.value.find((task) => task.id == store.selectedTask.id)) !==
      JSON.stringify(store.selectedTask)
  ) {
    openThisOrAll('save')
  } else {
    saveTask()
  }
}

const repeatTask = (prams, start) => {
  let dates = []
  if (prams) {
    let startDate = new Date(start)
    const repeatUnits = (prams) => {
      const tempDate = new Date(startDate)
      if (prams.everyUnit == 'days') {
        //TO DO: add tasks on those dates
        dates.push(tempDate)
        startDate.setDate(startDate.getDate() + prams.everyNumber)
      } else if (prams.everyUnit === 'weeks') {
        prams.selectedDays.forEach((day) => {
          const daysToAdd = (day - tempDate.getDay() + 7) % 7
          tempDate.setDate(tempDate.getDate() + daysToAdd)
          // add tasks
          dates.push(tempDate)
        })
        startDate.setDate(startDate.getDate() + 7 * prams.everyNumber)
      } else if (prams.everyUnit == 'months') {
        //TO DO: add tasks on those dates
        dates.push(tempDate)
        startDate.setMonth(startDate.getMonth() + prams.everyNumber)
      } else if (prams.everyUnit == 'years') {
        //TO DO: add tasks on those dates
        dates.push(tempDate)
        startDate.setFullYear(startDate.getFullYear() + prams.everyNumber)
      }
    }
    if (prams.repeatEnd == 'after') {
      for (let i = 0; i < prams.occurrences; i++) {
        repeatUnits(prams)
      }
    } else if (prams.repeatEnd == 'on') {
      while (startDate <= new Date(prams.endDate)) {
        repeatUnits(prams)
      }
    } else if (prams.repeatEnd == 'never') {
      for (let i = 0; i < 730; i++) {
        repeatUnits(prams)
      }
    }
  }
  return dates
}

const saveTask = async (thisOrAll = 'this') => {
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
        // repeat update all
        if (store.selectedTask.repeatId) {
          // Check if repeatParameters have changed
          if (store.selectedTask.repeatParameters == null) {
            // Don't repeat Task
            const updatedTasks = localTasks.filter(
              (task) =>
                task.repeatId !== store.selectedTask.repeatId || task.id === store.selectedTask.id
            )
            store.selectedTask.repeatId = null
            const index = updatedTasks.findIndex((task) => task.id === store.selectedTask.id)
            if (index !== -1) {
              localTasks[index] = store.selectedTask
            }
            localStorage.setItem('tasks', JSON.stringify(updatedTasks))
          } else {
            if (thisOrAll == 'all') {
              let index = localTasks.findIndex((t) => t.repeatId === store.selectedTask.repeatId)
              if (
                JSON.stringify(store.selectedTask.repeatParameters) !==
                JSON.stringify(localTasks[index].repeatParameters)
              ) {
                const updatedTasks = localTasks.filter(
                  (t) => t.repeatId !== String(Number(store.selectedTask.repeatId))
                )
                let dates = repeatTask(store.selectedTask.repeatParameters, localTasks[index].date)
                store.selectedTask.repeatId = String(nextTaskId)
                for (let i = 0; i < dates.length; i++) {
                  // Create a new task object for each iteration
                  let newTask = {
                    ...store.selectedTask,
                    id: String(nextTaskId),
                    date: new Date(dates[i]).toISOString().split('T')[0]
                  }
                  updatedTasks.push(newTask)
                  localStorage.setItem('nextTaskId', nextTaskId++)
                }
                localStorage.setItem('tasks', JSON.stringify(updatedTasks))
              } else {
                // Update the existing tasks with the same repeatId
                const updatedTasks = localTasks.map((task) => {
                  if (task.repeatId === store.selectedTask.repeatId) {
                    task.title = store.selectedTask.title
                    task.time = store.selectedTask.time
                    task.description = store.selectedTask.description
                  }
                  return task
                })

                // Save the updated tasks to localStorage
                localStorage.setItem('tasks', JSON.stringify(updatedTasks))
              }
            } else {
              let index = localTasks.findIndex((t) => t.id === store.selectedTask.id)
              if (
                JSON.stringify(store.selectedTask.repeatParameters) !==
                JSON.stringify(localTasks[index].repeatParameters)
              ) {
                const updatedTasks = localTasks.filter(
                  (t) => t.id !== String(Number(store.selectedTask.id))
                )
                let dates = repeatTask(store.selectedTask.repeatParameters, localTasks[index].date)
                store.selectedTask.repeatId = String(nextTaskId)
                for (let i = 0; i < dates.length; i++) {
                  // Create a new task object for each iteration
                  let newTask = {
                    ...store.selectedTask,
                    id: String(nextTaskId),
                    date: new Date(dates[i]).toISOString().split('T')[0]
                  }
                  updatedTasks.push(newTask)
                  localStorage.setItem('nextTaskId', nextTaskId++)
                }
                localStorage.setItem('tasks', JSON.stringify(updatedTasks))
              } else {
                // Update the existing task with the same repeatId
                if (JSON.stringify(localTasks[index]) !== JSON.stringify(store.selectedTask)) {
                  store.selectedTask.id = String(nextTaskId)
                  store.selectedTask.repeatId = null
                  store.selectedTask.repeatParameters = null
                  localTasks[index] = store.selectedTask
                  // Save the updated task to localStorage
                  localStorage.setItem('tasks', JSON.stringify(localTasks))
                  localStorage.setItem('nextTaskId', nextTaskId++)
                }
              }
            }
          }
        } else {
          const existingTaskIndex = localTasks.findIndex(
            (task) => task.id === store.selectedTask.id
          )
          if (existingTaskIndex !== -1) {
            // Task found, update its properties
            localTasks[existingTaskIndex] = store.selectedTask
          }
          localStorage.setItem('tasks', JSON.stringify(localTasks))
        }
      } else {
        const localTasks = JSON.parse(localStorage.getItem('tasks')) || []
        // repeat new task
        if (store.selectedTask.repeatParameters) {
          let dates = repeatTask(store.selectedTask.repeatParameters, store.selectedTask.date)
          store.selectedTask.repeatId = String(nextTaskId)
          for (let i = 0; i < dates.length; i++) {
            // Create a new task object for each iteration
            let newTask = {
              ...store.selectedTask,
              id: String(nextTaskId),
              date: new Date(dates[i]).toISOString().split('T')[0]
            }
            localTasks.push(newTask)
            localStorage.setItem('nextTaskId', nextTaskId++)
          }
          localStorage.setItem('tasks', JSON.stringify(localTasks))
        } else {
          store.selectedTask.id = String(nextTaskId++)
          localTasks.push(store.selectedTask)
          localStorage.setItem('tasks', JSON.stringify(localTasks))
          localStorage.setItem('nextTaskId', nextTaskId)
        }
      }
    }
    closeTaskCard()
    closeThisOrAll()
  } catch (error) {
    // Handle errors
    console.error(error)
  }
  fetchData()
}

const openTaskCard = (event, task, day) => {
  if (
    event.target.closest('.task-card') ||
    event.target.closest('.task-repeat') ||
    store.isRepeatOpen ||
    deleteThisOrAll.value
  ) {
    // Clicked inside the task card, don't trigger opening or closing

    return
  }
  if (event.target.classList.contains('checkbox')) {
    return
  }
  if (!task && !store.isopencard) {
    // create new task

    setTimeout(() => {
      store.setIsOpenCard(true)
      store.setSelectedTask({
        id: null,
        title: '',
        date: day.date,
        time: null,
        description: '',
        repeatParameters: null,
        repeatId: null,
        done: false,
        user: localStorage.getItem('userId') || null
      })
    }, 0)

    document.addEventListener('click', openTaskCard)
  } else if (!task && store.isopencard) {
    handleSaveThisOrAll()
  } else if (task && !store.isopencard) {
    //update existing task

    setTimeout(() => {
      store.setIsOpenCard(true)
    }, 0)
    store.setSelectedTask({ ...task })
    if (store.selectedTask.time) {
      store.timepic = {
        hours: store.selectedTask.time.split(':')[0],
        minutes: store.selectedTask.time.split(':')[1]
      }
    }

    document.addEventListener('click', openTaskCard)
  } else {
    saveTask()
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
          <div class="weekday" :style="{ color: 'white' }">
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
        </div>
      </div>
      <taskCard
        :fetchData="fetchData"
        :handleSaveThisOrAll="handleSaveThisOrAll"
        :openThisOrAll="openThisOrAll"
        :closeThisOrAll="closeThisOrAll"
        :deleteThisOrAll="deleteThisOrAll"
      />
      <div v-if="saveThisOrAll" class="thisOrAll">
        <div @click="saveTask('this')">This Task</div>
        <div @click="saveTask('all')">All Tasks</div>
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
.thisOrAll {
  position: absolute;
  display: flex;
  flex-direction: column;
  top: 50%;
  left: 50%;
  width: 150px;
  padding: 4px;
  transform: translate(-50%, -50%);
  border-radius: 6px;
  background: linear-gradient(165deg, rgb(32, 32, 32), #181818);
  border: 1px solid #303030;
  z-index: 10;
  div {
    cursor: pointer;
    padding: 6px 8px;
    &:hover {
      background: #292929;
      border-radius: 4px;
    }
  }
}
</style>
