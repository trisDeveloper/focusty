<script setup>
import axios from 'axios'
import taskRepeat from './task-repeat.vue'
import { updateTaskDoneStatus } from '@/utils/update-task-done.js'
import { useStore } from '@/stores'
const props = defineProps([
  'fetchData',
  'task',
  'handleSaveThisOrAll',
  'closeThisOrAll',
  'closeTaskCard',
  'openThisOrAll',
  'deleteThisOrAll'
])
const store = useStore()

const deleteTask = async (task, deleteThisOrAll) => {
  try {
    closeTaskCard()
    props.closeThisOrAll()
    if (localStorage.getItem('userId')) {
      await axios.delete(`/api/users/${store.user.id}/tasks/${task.id}/`, {
        data: { deleteThisOrAll: deleteThisOrAll }
      })
    } else {
      const localTasks = JSON.parse(localStorage.getItem('tasks')) || []
      if (task.repeatId && deleteThisOrAll == 'all') {
        const updatedTasks = localTasks.filter((t) => t.repeatId !== task.repeatId)
        localStorage.setItem('tasks', JSON.stringify(updatedTasks))
      } else {
        const updatedTasks = localTasks.filter((t) => t.id !== task.id)
        localStorage.setItem('tasks', JSON.stringify(updatedTasks))
      }
    }
  } catch (error) {
    // Handle errors
    console.error(error)
  }
  props.fetchData()
}
const handleClickOutside = (event) => {
  if (store.isRepeatOpen && !event.target.closest('.task-repeat')) {
    store.setIsRepeatOpen(false)
    document.removeEventListener('click', handleClickOutside)
  }
}
const openRepeatCard = () => {
  setTimeout(() => {
    store.setIsRepeatOpen(true)
  }, 0)
  document.addEventListener('click', handleClickOutside)
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

props.fetchData()
</script>

<template>
  <div v-if="store.isopencard" class="task-card" ref="taskCard">
    <div class="task-actions">
      <!-- delete icon -->
      <font-awesome-icon
        title="Delete Task"
        icon="fa-regular fa-trash-can"
        class="trash"
        @click="
          store.selectedTask.repeatId
            ? props.openThisOrAll('delete')
            : deleteTask(store.selectedTask, 'this')
        "
      />
      <!-- done icon -->
      <font-awesome-icon
        title="Mark As Done"
        icon="fa-regular fa-check-square"
        class="checkbox"
        @click="updateTaskDoneStatus(store, store.selectedTask, props)"
        :class="{ done: store.selectedTask.done }"
      />
      <!-- repeat icon -->
      <font-awesome-icon
        title="Repeat Task"
        icon="fa-solid fa-repeat"
        class="repeat"
        :style="store.selectedTask.repeatParameters ? { color: '#3eff78e0' } : ''"
        @click="openRepeatCard()"
      />
    </div>
    <!-- title -->
    <div class="task-title">
      <input
        class="task-title"
        v-model="store.selectedTask.title"
        @input="updateTaskTitle"
        @keyup.enter="props.handleSaveThisOrAll"
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
      @keyup.enter="props.handleSaveThisOrAll"
      placeholder="Description"
    />
    <div v-if="props.deleteThisOrAll" class="thisOrAll">
      <div @click="deleteTask(store.selectedTask, 'this')">This Task</div>
      <div @click="deleteTask(store.selectedTask, 'all')">All Tasks</div>
    </div>
    <taskRepeat v-if="store.isRepeatOpen"></taskRepeat>
  </div>
</template>

<style lang="scss">
@use '@/styles.scss' as *;
.tasks {
  padding: 5px;
  flex-grow: 1;
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
  border: 1px solid #303030;
  box-shadow: 0px 2px 10px 2px #03030e41;
  z-index: 10;
  .task-actions {
    display: flex;
    flex-direction: row-reverse;
    margin-bottom: 10px;
    color: #ddd;
    font-size: 18px;
    .trash,
    .checkbox,
    .repeat {
      padding-left: 10px;
      &:hover {
        color: #818181;
      }
    }
    .done {
      color: #818181 !important;
      text-decoration: line-through;
      transition: all 0.3s;
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
      border: 1px solid #303030;
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
      background: #2b2b2b !important;
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
</style>
