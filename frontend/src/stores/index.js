import { defineStore } from 'pinia'

export const useStore = defineStore('storeId', {
  state: () => ({
    weekStart: new Date(),
    user: {
      id: null,
      username: null,
      email: null,
      pic: null,
      birthday: null,
      country: null,
      join: null
    },
    isopencard: false,
    isRepeatOpen: false,
    isColorOpen: false,
    selectedTask: {
      id: null,
      title: '',
      date: null,
      time: '00:00',
      description: '',
      repeatParameters: null,
      repeatId: null,
      done: false,
      color: '#555555',
      user: null
    },
    timepic: {
      hours: 0,
      minutes: 0
    }
  }),
  actions: {
    setWeekStart(value) {
      this.weekStart = value
    },
    setIsOpenCard(value) {
      this.isopencard = value
    },
    setIsRepeatOpen(value) {
      this.isRepeatOpen = value
    },
    setIsColorOpen(value) {
      this.isColorOpen = value
    },
    setSelectedTask(task) {
      this.selectedTask = task
    },
    setUser(user) {
      this.user = user
    }
  }
})
