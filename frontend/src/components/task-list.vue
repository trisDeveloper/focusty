<template>
  <div class="tasks" @click="openTaskCard($event)">
    <div
      v-for="task in day.tasks"
      :key="task.title"
      :class="{ task, done: task.done }"
      @click.stop="openTaskCard($event, task)"
    >
      <font-awesome-icon
        icon="fa-regular fa-check-square"
        class="checkbox"
        @click="updateTaskDoneStatus(task)"
        :class="{ done: task.done }"
      />
      <p>{{ task.title }}</p>
    </div>
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

      <!-- date input -->
      <VDatePicker
        v-model="store.selectedTask.date"
        mode="dateTime"
        class="date-picker"
        color="indigo"
        v-if="store.isdatepicker"
        is-dark
        hide-time-header
        @update:modelValue="handleDateSelection"
      />
      <button class="task-date" @click="store.toggledatepicker(!store.isdatepicker)">
        <font-awesome-icon icon="fa-solid fa-calendar-days" />{{ store.selectedTask.date }}
      </button>

      <input
        class="task-desc"
        v-model="store.selectedTask.description"
        @input="updateTaskDescription"
        @keyup.enter="saveTaskAndClose"
        placeholder="Description"
      />
    </div>
  </div>
</template>

<script>
import { useStore } from '@/stores'
import axios from 'axios'
export default {
  props: ['tasks', 'day', 'fetch'],

  setup(props) {
    const store = useStore()

    const updateTaskDoneStatus = async (task) => {
      try {
        task.done = !task.done
        await axios.patch(`/api/tasks/${task.id}/`, { done: task.done })
        props.fetch()
      } catch (error) {
        // Handle errors
        console.error(error)
      }
    }

    const openTaskCard = (event, task) => {
      if (event.target.closest('.task-card')) {
        // Clicked inside the task card, don't trigger opening or closing
        return
      }
      if (event.target.classList.contains('checkbox')) {
        return
      }
      if (!task && !store.isopencard) {
        // create new task
        store.setIsOpenCard(true)
        store.setSelectedTask({
          id: null,
          title: '',
          date: props.day.date,
          description: '',
          done: false
        })
      } else if (!task && store.isopencard) {
        saveTaskAndClose()
      } else if (task && !store.isopencard) {
        //update existing task
        store.setIsOpenCard(true)
        store.setSelectedTask({ ...task })
      } else {
        saveTaskAndClose()
      }
      if (!store.isopencard) {
        document.body.addEventListener('click', closeTaskCard)
      } else {
        document.body.removeEventListener('click', closeTaskCard)
      }
    }

    const closeTaskCard = () => {
      store.toggledatepicker(false)
      store.setIsOpenCard(false)

      store.setSelectedTask({
        id: null,
        title: '',
        date: null,
        description: '',
        done: false
      })
      document.body.removeEventListener('click', closeTaskCard)
    }

    const deleteTask = async (task) => {
      try {
        task.done = !task.done
        closeTaskCard()
        await axios.delete(`/api/tasks/${task.id}/`, { done: task.done })
        props.fetch()
      } catch (error) {
        // Handle errors
        console.error(error)
      }
    }

    const updateTaskTitle = (event) => {
      store.selectedTask.title = event.target.value
    }

    const handleDateSelection = (selectedDate) => {
      store.selectedTask.date = selectedDate.toISOString().split('T')[0]
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
        if (store.selectedTask.id) {
          await axios.put(`/api/tasks/${store.selectedTask.id}/`, store.selectedTask)
        } else {
          await axios.post('/api/tasks/', store.selectedTask)
        }
        props.fetch()
        closeTaskCard()
      } catch (error) {
        // Handle errors
        console.error(error)
      }
    }

    return {
      store,
      updateTaskDoneStatus,
      openTaskCard,
      closeTaskCard,
      deleteTask,
      updateTaskTitle,
      updateTaskDescription,
      saveTaskAndClose,
      handleDateSelection
    }
  },

  mounted() {},
  beforeUnmount() {
    document.body.removeEventListener('click', this.closeTaskCard)
  }
}
</script>

<style lang="scss">
@import './../styles.scss';
.tasks {
  padding: 5px;
  flex-grow: 1;
  .task {
    display: flex;
    align-items: stretch;
    font-size: 18px;
    position: relative;
    margin: 8px 0;
    padding: 8px;
    box-sizing: border-box;
    $border: 1px;
    color: #fff;
    background: $dark-back;
    background-clip: padding-box;
    border: solid $border transparent;
    border-radius: 7px;
    .checkbox {
      padding: 0 10px 0 0;
    }
    p {
      overflow: hidden;
    }
    &:hover {
      background-color: #121231;
      cursor: pointer;
    }
    &:before {
      content: '';
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      z-index: -1;
      margin: -$border;
      border-radius: inherit;
      background: $rainbow-gradient;
    }
  }
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
    background-color: #06061c;
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
      background: #06061c;
      color: white;
      margin: 10px 0;
      width: 100%;
      padding: 5px;
      font-size: 20px;
      border-bottom: 1px solid transparent;
      &:hover {
        background-color: #121231;
      }
      &:focus-visible {
        outline: none;
        border-bottom: 1px solid white;
      }
    }
    .task-title {
      position: relative;
      display: flex;
      align-items: center;
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
      padding: 10px 5px;
      svg {
        padding-right: 10px;
      }
    }
    .task-desc {
      font-size: 15px;
      color: #ffffffc4;
    }
  }
  .date-picker {
    border: 1px solid #a984ff;
    background: #121231;
    .vc-header {
      .vc-title {
        background: #06061c;
      }
      .vc-arrow {
        background: #121231;
      }
    }
    .vc-time-select-group {
      background: #06061c;
      border: none !important;
      select {
        border: none !important;
        &:hover {
          background: #121231;
        }
        &::-webkit-scrollbar {
          width: 5px;
        }
        &::-webkit-scrollbar-thumb {
          background-color: transparent;
          border-radius: 5px;
        }
        &::-webkit-scrollbar-track {
          background-color: transparent;
        }
        &::-webkit-scrollbar-thumb:hover {
          background-color: #bed5ff42;
        }
      }
    }
  }
}
</style>
