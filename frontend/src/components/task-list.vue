<template>
  <div>
    <div :class="{ task, done: task.done }">
      <font-awesome-icon
        icon="fa-regular fa-check-square"
        class="checkbox"
        @click="updateTaskDoneStatus(task)"
        :class="{ done: task.done }"
      />
      <p>{{ task.title }}</p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { useStore } from '@/stores'
const props = defineProps(['fetchData', 'task'])
const store = useStore()

const updateTaskDoneStatus = async (task) => {
  try {
    task.done = !task.done
    await axios.patch(`/api/users/${store.user.id}/tasks/${task.id}/`, { done: task.done })
    props.fetchData()
  } catch (error) {
    // Handle errors
    console.error(error)
  }
}
props.fetchData()
</script>
<style lang="scss">
@import './../styles.scss';
.tasks {
  padding: 5px;
  flex-grow: 1;
  min-height: 100px;
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
