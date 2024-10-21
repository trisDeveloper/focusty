let nextTaskId = localStorage.getItem('nextTaskId') || 1
export const repeatTask = (store, prams, start, tasks) => {
  let dates = []
  let taskCount = 0
  if (prams) {
    let startDate = new Date(start)

    const repeatUnits = (prams) => {
      const tempDate = new Date(startDate)

      if (prams.everyUnit === 'days') {
        dates.push(new Date(tempDate))
        startDate.setDate(startDate.getDate() + prams.everyNumber)
        taskCount++
      } else if (prams.everyUnit === 'weeks') {
        prams.selectedDays.forEach((day) => {
          if (prams.occurrences && taskCount >= prams.occurrences) return

          const currentDate = new Date(startDate)
          const daysToAdd = (day - currentDate.getDay() + 7) % 7
          currentDate.setDate(currentDate.getDate() + daysToAdd)

          if (currentDate >= startDate) {
            dates.push(new Date(currentDate))
            taskCount++
          }
        })
        startDate.setDate(startDate.getDate() + 7 * prams.everyNumber)
      } else if (prams.everyUnit === 'months') {
        dates.push(new Date(tempDate))
        startDate.setMonth(startDate.getMonth() + prams.everyNumber)
        taskCount++
      } else if (prams.everyUnit === 'years') {
        dates.push(new Date(tempDate))
        startDate.setFullYear(startDate.getFullYear() + prams.everyNumber)
        taskCount++
      }
    }

    if (prams.repeatEnd === 'after') {
      while (taskCount < prams.occurrences) {
        repeatUnits(prams)
      }
    } else if (prams.repeatEnd === 'on') {
      while (startDate <= new Date(prams.endDate)) {
        repeatUnits(prams)
      }
    } else if (prams.repeatEnd === 'never') {
      while (taskCount <= 365) {
        repeatUnits(prams)
      }
    }
  }
  store.selectedTask.repeatId = String(nextTaskId)
  dates.forEach((date) => {
    let newTask = {
      ...store.selectedTask,
      id: String(nextTaskId),
      date: date.toISOString().split('T')[0]
    }
    tasks.push(newTask)
    nextTaskId++
  })
  // Update localStorage
  localStorage.setItem('nextTaskId', nextTaskId)
  localStorage.setItem('tasks', JSON.stringify(tasks))
}
