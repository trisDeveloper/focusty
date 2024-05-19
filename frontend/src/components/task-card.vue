<template>
  <div v-if="store.isopencard" class="task-card" ref="taskCard">
    <div class="task-actions">
      <!-- delete icon -->
      <font-awesome-icon
        icon="fa-regular fa-trash-can"
        class="trash"
        @click="deleteTask(store.selectedTask)"
      />
      <font-awesome-icon
        icon="fa-regular fa-check-square"
        class="checkbox"
        @click="updateTaskDoneStatus(store.selectedTask)"
        :class="{ done: store.selectedTask.done }"
      />
      <font-awesome-icon
        icon="fa-solid fa-repeat"
        class="repeat"
        @click="openRepeatCard(store.selectedTask)"
      />
    </div>
    <!-- title -->
    <div class="task-title">
      <input
        class="task-title"
        v-model="store.selectedTask.title"
        @input="updateTaskTitle"
        @keyup.enter="saveTaskAndClose"
        placeholder="Title"
      />
      <font-awesome-icon icon="fa-solid fa-pencil" />
    </div>
    <div class="task-date">
      <VDatePicker
        v-model="store.selectedTask.date"
        @update:modelValue="handleDateSelection"
        is-dark
        class="date-picker"
        color="indigo"
        :popover="false"
      >
        <template #default="{ togglePopover }">
          <div>
            <button class="date-btn" @click="() => togglePopover()">
              <span
                ><font-awesome-icon icon="fa-solid fa-calendar-days" />{{
                  store.selectedTask.date
                }}</span
              >
            </button>
          </div>
        </template>
      </VDatePicker>
      <VueDatePicker
        v-model="store.timepic"
        class="time-picker"
        dark
        time-picker
        @update:modelValue="handleTimeSelection"
      />
    </div>
    <input
      class="task-desc"
      v-model="store.selectedTask.description"
      @input="updateTaskDescription"
      @keyup.enter="saveTaskAndClose"
      placeholder="Description"
    />
  </div>
</template>

<script setup>
import axios from 'axios'
import { useStore } from '@/stores'
const props = defineProps(['fetchData', 'task'])
const store = useStore()
let nextTaskId = localStorage.getItem('nextTaskId') || 1
const deleteTask = async (task) => {
  try {
    closeTaskCard()
    if (localStorage.getItem('userId')) {
      await axios.delete(`/api/users/${store.user.id}/tasks/${task.id}/`, { done: task.done })
    } else {
      const localTasks = JSON.parse(localStorage.getItem('tasks')) || []
      const updatedTasks = localTasks.filter((t) => t.id !== task.id)
      localStorage.setItem('tasks', JSON.stringify(updatedTasks))
    }
  } catch (error) {
    // Handle errors
    console.error(error)
  }
  props.fetchData()
}
const updateTaskDoneStatus = async (task) => {
  try {
    task.done = !task.done
    if (localStorage.getItem('userId')) {
      await axios.patch(`/api/users/${store.user.id}/tasks/${task.id}/`, { done: task.done })
    } else {
      const localTasks = JSON.parse(localStorage.getItem('tasks')) || []

      const updatedTaskIndex = localTasks.findIndex((t) => t.id == Number(task.id))
      if (updatedTaskIndex !== -1) {
        localTasks[updatedTaskIndex].done = task.done
        localStorage.setItem('tasks', JSON.stringify(localTasks))
      }
    }
  } catch (error) {
    // Handle errors
    console.error(error)
  }
  props.fetchData()
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
  document.body.removeEventListener('click', closeTaskCard)
}

const updateTaskTitle = (event) => {
  store.selectedTask.title = event.target.value
}

const handleDateSelection = (selectedDate) => {
  store.selectedTask.date = selectedDate.toISOString().split('T')[0]
}

const handleTimeSelection = (modelData) => {
  store.timepic = modelData
  store.selectedTask.time = `${store.timepic.hours}:${store.timepic.minutes}`
}

const updateTaskDescription = (event) => {
  store.selectedTask.description = event.target.value
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
  props.fetchData()
}
props.fetchData()
</script>
<style lang="scss">
@import './../styles.scss';
.tasks {
  padding: 5px;
  flex-grow: 1;
  .done {
    color: #393949;
    text-decoration: line-through;
    transition: all 0.3s;
  }
  .task-card {
    position: fixed;
    display: flex;
    flex-direction: column;
    top: 50%;
    left: 50%;
    width: 400px;
    max-width: calc(100% - 10px);
    transform: translate(-50%, -50%);
    border-radius: 10px;
    padding: 20px;
    background-color: #0b0c0d;
    border: 1px solid #8269ac;
    box-shadow: 0px 2px 10px 2px #03030e41;
    z-index: 10;
    .task-actions {
      display: flex;
      flex-direction: row-reverse;
      margin-bottom: 10px;
      color: #ddd;
      font-size: 18px;
      .trash,
      .checkbox {
        padding-left: 10px;
        &:hover {
          color: #c4a3ff;
        }
      }
    }
    .task-title input,
    .task-desc,
    .task-date {
      border: none;
      background: #0b0c0d;
      color: white;
      margin: 10px 0;
      width: 100%;
      padding: 5px;
      font-size: 20px;
      border-bottom: 1px solid transparent;
      &:focus-visible {
        outline: none;
        border-bottom: 1px solid white;
      }
    }
    .task-title {
      position: relative;
      display: flex;
      align-items: center;
      & input:hover {
        background-color: #131518;
      }
      input {
        border-bottom: 1px solid #ddd;
      }
      svg {
        position: absolute;
        right: 5px;
        color: #ccc;
      }
    }
    .task-date {
      margin: 5px 0;
      font-size: 16px;
      text-align: left;
      border: none;
      display: flex;
      align-items: center;
      .date-picker {
        border: 1px solid #a984ff;
        background: #131518 !important;
        position: absolute;
        button {
          background: #0b0c0d !important;
        }
        .vc-arrow {
          background: #131518;
        }
      }
      .vc-popover-content-wrapper .vc-popover-content button {
        background: #06061b !important;
        color: #fff;
      }
      .date-btn {
        background: inherit;
        border: none;
        color: inherit;
        font-size: inherit;
        border: 1px solid #131518;
        cursor: pointer;
        padding: 9px 5px;
        margin-right: 6px;
        border-radius: 4px;
        transition: all 0.3s ease-in-out;
        &:hover {
          background: #0b0c0d;
          border: 1px solid #aaaeb7;
        }
        svg {
          padding-right: 7px;
          color: #959595;
          &:hover {
            color: inherit;
          }
        }
      }
      .time-picker {
        width: 120px;
        .dp__pointer {
          background: inherit !important;
          border: 1px solid #131518;
          &:hover {
            background: #0b0c0d;
            border: 1px solid #aaaeb7;
          }
        }
      }
    }
    .task-desc {
      font-size: 15px;
      color: #ffffffc4;
      &:hover {
        background-color: #131518;
      }
    }
  }
}
</style>
