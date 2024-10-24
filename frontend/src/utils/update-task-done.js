import axios from 'axios'

export const updateTaskDoneStatus = async (store, task, props) => {
  try {
    task.done = !task.done
    if (localStorage.getItem('userId')) {
      await axios.patch(`/api/users/${store.user.id}/tasks/${task.id}/`, { done: task.done })
    } else {
      const localTasks = JSON.parse(localStorage.getItem('tasks')) || []

      const updatedTaskIndex = localTasks.findIndex((t) => t.id == Number(task.id))
      if (updatedTaskIndex !== -1) {
        localTasks[updatedTaskIndex].done = task.done
        localStorage.setItem('tasks', JSON.stringify(localTasks))
      }
    }
  } catch (error) {
    console.error(error)
  }
  props.fetchData()
}
