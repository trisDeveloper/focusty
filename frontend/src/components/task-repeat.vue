<script setup>
import { ref } from 'vue'
import { useStore } from '@/stores'
const store = useStore()

const everyNumber = ref(1)
const everyUnit = ref('days')
const selectedDays = ref([])
const repeatEnd = ref('never')
const occurrences = ref(30)
const endDate = ref(
  new Date(new Date(store.selectedTask.date).setMonth(new Date().getMonth() + 1))
    .toISOString()
    .split('T')[0]
)
const repeatNot = ref(false)

const validateInput = () => {
  if (everyNumber.value < 1) {
    everyNumber.value = 1
  }
  if (occurrences.value < 1) {
    occurrences.value = 1
  }
}

const weekDays = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']

const toggleDay = (day) => {
  const index = selectedDays.value.indexOf(day)
  if (index === -1) {
    selectedDays.value.push(day)
  } else {
    selectedDays.value.splice(index, 1)
  }
}

const toggleRepeatNot = () => {
  repeatNot.value = !repeatNot.value
}

const save = () => {
  try {
    if (!repeatNot.value) {
      store.setSelectedTask({
        ...store.selectedTask,
        repeatParameters: {
          everyNumber: everyNumber.value,
          everyUnit: everyUnit.value,
          selectedDays: everyUnit.value == 'weeks' ? selectedDays.value : [],
          repeatEnd: repeatEnd.value,
          occurrences: repeatEnd.value == 'after' ? occurrences.value : null,
          endDate: repeatEnd.value == 'on' ? endDate.value : null
        },
        repeatId: store.selectedTask.id
      })
    }
  } catch (error) {
    console.error(error)
  }

  store.setIsRepeatOpen(false)
}
const cancel = () => {
  store.setIsRepeatOpen(false)
}
</script>

<template>
  <div class="task-repeat">
    <div class="title">Repeat</div>
    <div :class="repeatNot ? 'customization not-repeating' : 'customization'">
      <div class="repeat-every">
        <span>Every</span>
        <input
          type="number"
          min="1"
          step="1"
          v-model.number="everyNumber"
          @blur="validateInput"
          :disabled="repeatNot"
        />
        <select name="" v-model="everyUnit" :disabled="repeatNot">
          <option value="days">days</option>
          <option value="weeks">weeks</option>
          <option value="months">months</option>
          <option value="years">years</option>
        </select>
      </div>
      <div v-if="everyUnit === 'weeks' && !repeatNot" class="repeat-on">
        <span>On</span>
        <button
          v-for="(day, index) in weekDays"
          :key="index"
          :class="{ active: selectedDays.includes(day) }"
          @click="toggleDay(day)"
          class="week-days"
        >
          {{ day }}
        </button>
      </div>
      <div class="repeat-ends">
        <span>Ends</span>
        <label class="ends-option">
          <input
            type="radio"
            name="repeat-ends"
            value="never"
            v-model="repeatEnd"
            :disabled="repeatNot"
            @change="handleRepeatEndChange"
            checked
          />
          Never
        </label>
        <label class="ends-option">
          <input
            type="radio"
            name="repeat-ends"
            value="after"
            v-model="repeatEnd"
            :disabled="repeatNot"
            @change="handleRepeatEndChange"
          />
          After
          <input
            type="number"
            v-model="occurrences"
            @change="handleRepeatEndChange"
            min="1"
            @blur="validateInput"
            style="width: 50px; margin-left: 5px"
            :disabled="repeatEnd !== 'after' || repeatNot"
          />
          times
        </label>
        <label class="ends-option">
          <input
            type="radio"
            name="repeat-ends"
            value="on"
            v-model="repeatEnd"
            :disabled="repeatNot"
            @change="handleRepeatEndChange"
          />
          On
          <input
            type="date"
            v-model="endDate"
            @change="handleRepeatEndChange"
            style="margin-left: 5px"
            :disabled="repeatEnd !== 'on' || repeatNot"
          />
        </label>
      </div>
      <div class="repeat-not">
        <button @click="toggleRepeatNot" :class="{ active: repeatNot }">
          {{ repeatNot ? 'Repeat' : "Don't Repeat" }}
        </button>
      </div>
    </div>
    <div class="buttons">
      <button @click="cancel()">cancel</button>
      <button @click="save()">save</button>
    </div>
  </div>
</template>

<style lang="scss">
@import './../styles.scss';

.task-repeat {
  position: absolute;
  z-index: 10;
  display: flex;
  flex-direction: column;
  width: 90%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #111;
  border: 1px solid #88888813;
  border-radius: 8px;
  padding: 25px 20px;
  .title {
    font-weight: bold;
  }
  .customization {
    padding: 15px 0;
    font-size: 14px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    flex: 1;
    input,
    select {
      color: white;
      width: 60px;
      background: #111;
      border: 1px solid #ffffff2d;
      padding: 5px 8px;
      border-radius: 4px;
      &:focus {
        background: #222;
        border: 1px solid #222;
      }
    }
    input:disabled {
      background-color: #111;
      color: #222;
      border: 1px solid #222;
    }
    .repeat-every {
      display: flex;
      align-items: center;
      gap: 10px;
      select {
        width: 85px;
      }
    }
    .repeat-on {
      display: flex;
      align-items: center;
      gap: 5px;
      span {
        padding-right: 10px;
      }
      .week-days {
        font-size: 13px;
        line-height: 0;
        background: #111;
        color: white;
        border: 1px solid #ffffff2d;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        justify-content: center;
        align-items: center;
        &:hover {
          color: #2dff61;
          background: #79ff9a18;
          border: 1px solid #79ff9a18;
        }
      }
      .active {
        color: #2dff61;
        background: #79ff9a18;
        border: 1px solid #79ff9a18;
      }
    }
    .repeat-ends {
      display: flex;
      flex-direction: column;
      gap: 8px;
      input {
        width: fit-content;
      }
      .ends-option {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      input[type='date']::-webkit-calendar-picker-indicator {
        filter: invert(1);
      }
      input[type='date'] {
        color-scheme: dark;
      }
    }
    .repeat-not {
      button {
        padding: 5px 8px;
        cursor: pointer;
        background: #222;
        border: 1px solid #222;
        border-radius: 4px;
        color: white;
        &:hover {
          background: #161616;
          border: 1px solid #222;
        }
      }
      .active {
        background: #161616;
        border: 1px solid #222;
      }
    }
  }

  .buttons {
    display: flex;
    justify-content: end;
    gap: 10px;
    button {
      color: white;
      width: 60px;
      background: #111;
      border: 1px solid #ffffff2d;
      padding: 6px 8px;
      border-radius: 4px;
      &:hover {
        background: #333;
        cursor: pointer;
      }
      &:nth-of-type(2) {
        color: #2dff61;
        background: #79ff9a18;
        border: 1px solid #79ff9a18;
        &:hover {
          background: #79ff9b36;
        }
      }
    }
  }
}
</style>
