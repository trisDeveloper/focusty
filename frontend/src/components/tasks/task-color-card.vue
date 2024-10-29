<script setup>
import { useStore } from '@/stores'
const store = useStore()
const colors = [
  '#82FF87', // Light Mint Green
  '#00FFE6', // Electric Cyan
  '#93C5FD', // Light Sky Blue
  '#3B82F6', // Bright Blue
  '#D8B4FE', // Lavender Purple
  '#A78BFA', // Soft Violet Purple
  '#FCA5A5', // Light Red
  '#F9A8D4', // Soft Pink
  '#FDBA74', // Peachy Orange
  '#FFF26E', // Sunny Yellow
  '#232323' // gray
]
const saveColor = (color) => {
  store.setSelectedTask({ ...store.selectedTask, color })
  store.setIsColorOpen(false)
}
</script>

<template>
  <div class="color-palette">
    <h4 :style="{ fontWeight: 'bold' }">Change Task Color:</h4>
    <div class="colors">
      <div
        v-for="color in colors"
        :key="color"
        :title="color"
        class="color"
        :style="{ background: color }"
        @click.stop="saveColor(color)"
      ></div>
    </div>
  </div>
</template>

<style lang="scss">
@use '@/styles.scss' as *;

.color-palette {
  position: absolute;
  z-index: 10;
  width: 60%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -100%);
  background: #1a1c1d;
  border: 1px solid #88888823;
  box-shadow: 1px 1px 10px #00000080;
  border-radius: 4px;
  padding: 12px;
  .colors {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    padding-top: 15px;
  }
  .color {
    width: 19px;
    height: 19px;
    margin: 2px 4px 2px 0;
    border: 1px solid transparent;
    cursor: pointer;
    border-radius: 50%;
    &:hover {
      border: 1px solid #ccc;
      box-shadow: 1px 1px 10px #000000bd;
    }
  }
}
</style>
