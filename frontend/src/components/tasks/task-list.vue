<template>
  <div>
    <div :class="{ task, done: task.done }">
      <font-awesome-icon
        icon="fa-regular fa-check-square"
        class="checkbox"
        @click="updateTaskDoneStatus(store, task, props)"
        :class="{ done: task.done }"
      />
      <p>{{ task.title }}</p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { useStore } from '@/stores'
import { updateTaskDoneStatus } from '@/utils/update-task-done.js'
const props = defineProps(['fetchData', 'task'])
const store = useStore()
props.fetchData()
</script>
<style lang="scss">
@use '@/styles.scss' as *;
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
    background: linear-gradient(165deg, #49494973, #181818);
    background-clip: padding-box;
    border: solid $border #333;
    border-radius: 7px;
    .checkbox {
      padding: 0 10px 0 0;
    }
    p {
      overflow: hidden;
    }
    &:hover {
      background-color: #131518;
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
}
</style>
