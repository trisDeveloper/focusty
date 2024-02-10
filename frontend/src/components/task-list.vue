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
          <div v-if="store.isOpenCard" class="task-card" ref="taskCard">
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
        </div>
      </div>
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
          time: null,
          description: '',
          done: false
        })
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
        document.body.addEventListener('click', closeTaskCard)
      } else {
        document.body.removeEventListener('click', closeTaskCard)
      }
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
    const handleTimeSelection = (modelData) => {
      store.timepic = modelData // Directly update separate model
      store.selectedTask.time = `${store.timepic.hours}:${store.timepic.minutes}` // Format and update the actual task time
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
      handleDateSelection,
      handleTimeSelection
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
        background-color: #121231;
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
        background: #121231 !important;
        position: absolute;
        button {
          background: #06061c !important;
        }
        .vc-arrow {
          background: #121231;
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
        border: 1px solid #121231;
        cursor: pointer;
        padding: 9px 5px;
        margin-right: 6px;
        border-radius: 4px;
        transition: all 0.3s ease-in-out;
        &:hover {
          background: #06061c;
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
          border: 1px solid #121231;
          &:hover {
            background: #06061c;
            border: 1px solid #aaaeb7;
          }
        }
      }
    }
    .task-desc {
      font-size: 15px;
      color: #ffffffc4;
      &:hover {
        background-color: #121231;
      }
    }
  }
}
</style>
