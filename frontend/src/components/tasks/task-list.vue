<template>
  <div>
    <div
      :class="{ task, done: task.done }"
      @mouseover="isHovered = task.id"
      @mouseleave="isHovered = null"
      :style="{
        background: isHovered === task.id ? `${task.color}96` : `${task.color}66`,
        borderLeft: `4px solid ${task.color}`,
        boxShadow: isHovered === task.id ? ` 2px 2px 5px ${task.color}36` : `none`
      }"
    >
      <font-awesome-icon
        icon="fa-regular fa-check-square"
        class="checkbox"
        @click="updateTaskDoneStatus(store, task, props)"
        :class="{ done: task.done }"
      />
      <div>
        <div v-if="task.time" class="task-time">
          {{ `${task.time.split(':')[0]}:${task.time.split(':')[1].padStart(2, '0')}` }}
        </div>
        <p>{{ task.title }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStore } from '@/stores'
import { updateTaskDoneStatus } from '@/utils/update-task-done.js'
import { ref } from 'vue'
const props = defineProps(['fetchData', 'task'])
const store = useStore()
const isHovered = ref(null)
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
    font-size: 16px;
    position: relative;
    margin: 8px 0;
    padding: 8px;
    box-sizing: border-box;
    color: #fff;
    border-radius: 4px;
    transition: all 0.3s ease;
    cursor: pointer;
    .checkbox {
      padding: 0 10px 0 0;
    }
    p {
      overflow: hidden;
    }
    .task-time {
      font-size: 14px;
      color: #ffffffcc;
      padding-bottom: 4px;
    }
  }
  .done {
    color: #ccc;
    text-decoration: line-through;
    transition: all 0.3s;
  }
}
</style>
