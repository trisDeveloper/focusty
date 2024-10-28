import axios from 'axios'

let nextTaskId = localStorage.getItem('nextTaskId') || 1
export const saveTaskLogic = async (
  thisOrAll,
  store,
  repeatTask,
  closeTaskCard,
  closeThisOrAll,
  fetchData
) => {
  try {
    if (store.selectedTask.title.trim() === '') {
      // If title is empty, do nothing
      closeTaskCard()
      return
    }
    if (localStorage.getItem('userId')) {
      // update existed task
      if (store.selectedTask.id) {
        await axios.patch(`/api/users/${store.user.id}/tasks/${store.selectedTask.id}/`, {
          ...store.selectedTask,
          thisOrAll
        })
      } else {
        // New task creation
        await axios.post(`/api/users/${store.user.id}/tasks/`, {
          ...store.selectedTask,
          thisOrAll
        })
      }
    } else {
      // update task
      if (store.selectedTask.id) {
        const localTasks = JSON.parse(localStorage.getItem('tasks')) || []
        // task is repeated
        if (store.selectedTask.repeatId) {
          // don't repeat task or remove repeating a task
          if (thisOrAll == 'all') {
            if (store.selectedTask.repeatParameters == null) {
              store.selectedTask.repeatId = null
              store.selectedTask.repeatParameters = null
              const index = localTasks.findIndex((task) => task.id === store.selectedTask.id)
              if (index !== -1) {
                localTasks[index] = { ...store.selectedTask }
              }
              const updatedTasks = localTasks.filter(
                (task) => task.repeatId == store.selectedTask.repeatId
              )
              localStorage.setItem('tasks', JSON.stringify(updatedTasks))
            }
            // repeat task
            else {
              // change repeat parameters for all repeating tasks

              let index = localTasks.findIndex((t) => t.repeatId === store.selectedTask.repeatId)

              const updatedTasks = localTasks.filter(
                (t) => t.repeatId !== String(Number(store.selectedTask.repeatId))
              )
              repeatTask(
                store,
                store.selectedTask.repeatParameters,
                localTasks[index].date,
                updatedTasks
              )
              // Save the updated tasks to localStorage
              localStorage.setItem('tasks', JSON.stringify(updatedTasks))
            }

            // change repeat parameters for this task only
          } else {
            let index = localTasks.findIndex((t) => t.id === store.selectedTask.id)
            if (
              store.selectedTask.repeatParameters !== null &&
              JSON.stringify(store.selectedTask.repeatParameters) !==
                JSON.stringify(localTasks[index].repeatParameters)
            ) {
              const updatedTasks = localTasks.filter(
                (t) => t.id !== String(Number(store.selectedTask.id))
              )
              repeatTask(
                store,
                store.selectedTask.repeatParameters,
                localTasks[index].date,
                updatedTasks
              )
            } else {
              // Update the existing task with the same repeatId
              if (JSON.stringify(localTasks[index]) !== JSON.stringify(store.selectedTask)) {
                store.selectedTask.id = String(nextTaskId)
                store.selectedTask.repeatId = null
                store.selectedTask.repeatParameters = null
                localTasks[index] = store.selectedTask
                // Save the updated task to localStorage
                localStorage.setItem('tasks', JSON.stringify(localTasks))
                localStorage.setItem('nextTaskId', nextTaskId++)
              }
            }
          }
        }
        // task is not repeated
        else {
          const existingTaskIndex = localTasks.findIndex(
            (task) => task.id === store.selectedTask.id
          )
          if (existingTaskIndex !== -1) {
            localTasks[existingTaskIndex] = store.selectedTask
          }
          localStorage.setItem('tasks', JSON.stringify(localTasks))
        }
      }

      // new task
      else {
        const localTasks = JSON.parse(localStorage.getItem('tasks')) || []
        // repeat task
        if (store.selectedTask.repeatParameters) {
          repeatTask(
            store,
            store.selectedTask.repeatParameters,
            store.selectedTask.date,
            localTasks
          )
        } else {
          store.selectedTask.id = String(nextTaskId++)
          localTasks.push(store.selectedTask)
          localStorage.setItem('tasks', JSON.stringify(localTasks))
          localStorage.setItem('nextTaskId', nextTaskId)
        }
      }
    }
    closeTaskCard()
    closeThisOrAll()
  } catch (error) {
    console.error(error)
  } finally {
    fetchData()
  }
}
