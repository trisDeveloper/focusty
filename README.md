# Focusty 🚀

> [!TIP]
> This application is actively in development. While additional security measures have been added, Focusty is still not intended for handling sensitive data in production.

Focusty is a full-stack productivity app built with Vue, Vite, Python, and Django, integrating Pomodoro techniques, advanced task management, and insightful analytics for anyone aiming for peak productivity.

## Distinctiveness and Complexity

The app stands out by integrating multiple productivity features into one cohesive platform, offering a seamless experience tailored for focused time management.
The application uses Django for the backend and Vue.js for the frontend, along with JWT authentication for security and user data management. Building Focusty involved complex state management, asynchronous task updates, and interactive, real-time UI elements that enhance usability, making it both distinctive and technically challenging.

## Features 🛠️

- **Pomodoro Timer**: Boost your productivity with a fully customizable Pomodoro timer, meticulously engineered for focus and efficiency.
- **Task Management**: Effortlessly organize your tasks with intuitive **drag-and-drop** functionality, precise date and time pickers, and automatic sorting algorithms.
-  ![](https://img.shields.io/badge/New!-steelblue) **Recurring Tasks**: Now supports repeating tasks with customizable intervals and easy management, ensuring you never miss a deadline.
- **Calendar View**: Visualize your schedule with a sleek weekly calendar view, empowering dynamic task creation and seamless manipulation.
- **Task Color Customization**: Personalize your tasks by changing colors!
- **User Authentication**: Securely authenticate and manage profiles with JWT and password hashing.
- **Statistics and Analytics**: Gain profound insights into your productivity journey with dynamic line charts, meticulously tracking task completion and Pomodoro focus time.
- **Accessibility**: Now optimized to be 100% accessible, ensuring an inclusive user experience.

## Demo

link: https://trisdeveloper.github.io/focusty/

![Focusty](https://raw.githubusercontent.com/trisDeveloper/focusty/refs/heads/main/focusty%20homepage.png)

[![Focusty youtube video](https://img.youtube.com/vi/wrSbkanFiS0/0.jpg)](https://youtu.be/wrSbkanFiS0)

## Development Tools 🛠️

### Frontend

[![Vue.js](https://img.shields.io/badge/Vue.js-3.4.15-brightgreen)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0.11-blueviolet)](https://vitejs.dev/)
[![Axios](https://img.shields.io/badge/Axios-1.6.7-blue)](https://axios-http.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-3.9.1-orange)](https://www.chartjs.org/)
[![Pinia](https://img.shields.io/badge/Pinia-2.1.7-yellowgreen)](https://pinia.esm.dev/)
[![Vue Router](https://img.shields.io/badge/Vue%20Router-4.2.5-orange)](https://router.vuejs.org/)
[![Sortable.js](https://img.shields.io/badge/Sortable.js-1.15.2-yellow)](https://sortablejs.github.io/Vue.Draggable/)

### Backend

[![Django](https://img.shields.io/badge/Django-3.2-brightgreen)](https://www.djangoproject.com/)
[![Django CORS Headers](https://img.shields.io/badge/Django%20CORS%20Headers-4.3.1-blueviolet)](https://github.com/adamchainz/django-cors-headers)
[![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-3.14.0-blue)](https://www.django-rest-framework.org/)
[![Django Rest Framework Simple JWT](https://img.shields.io/badge/Django%20Rest%20Framework%20Simple%20JWT-5.3.1-orange)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
[![Djoser](https://img.shields.io/badge/Djoser-2.2.2-yellowgreen)](https://djoser.readthedocs.io/en/latest/)
[![Social Auth App Django](https://img.shields.io/badge/Social%20Auth%20App%20Django-5.4.0-yellow)](https://github.com/python-social-auth/social-app-django)

## Usage 📝

### Task Management 📅

- **Adding Tasks**: Effortlessly add new tasks by clicking on the today tasks section and providing essential details such as title, description, date, and time.
- **Editing Tasks**: Seamlessly modify task details, mark tasks as completed, change colors or remove tasks directly from the calendar view.
- **Recurring Tasks**: Easily create and manage repeating tasks to keep your productivity on track.
- **Drag-and-Drop**: Streamline your workflow by effortlessly rearranging tasks through intuitive drag-and-drop gestures.

### Pomodoro Timer ⏲️

- **Focus Sessions**: Personalize your focus sessions with customizable focus and break durations, complemented by a sleek Pomodoro timer.
- **Notifications**: Stay on track with timely notifications and audible alerts at the end of each focus session.

### Analytics 📊

- **Journey Page**: Visualize your productivity journey with sophisticated line charts, meticulously charting task completion and Pomodoro focus time over the past week.

## Running Focusty
The application is live and accessible at this [link](https://trisdeveloper.github.io/focusty/), ready for immediate use. If you'd like to run Focusty locally:

- **Clone the Repository**: Use ` git clone https://github.com/trisDeveloper/focusty ` to get the project files.
- **Run Backend**: `cd focusty/backend/ `
    - Set up a virtual environment `python3 -m venv venv && source venv/bin/activate` (optional but recommended)
    - Install dependencies `pip install -r requirements.txt`
    - Apply Django migrations `cd focusty/ && python manage.py makemigrations focusty_app && python manage.py migrate`
    - Run the Django development server `python manage.py runserver`
      
  The backend should now be accessible at `http://127.0.0.1:8000`.
- **Run Frontend**: `cd focusty/frontend/ `
    - Install dependencies `npm install`
    - Run the Vue development server `npm run dev`
      
  The frontend should now be accessible at the provided local server link, typically `http://localhost:5173/focusty#/`.

## Files Structure
### Backend
- **settings.py**: Configuration settings for the Django project, including database setup and installed apps.
- **urls.py**: URL routing for the application, mapping URL patterns to views.
- **views.py**: Contains the logic for handling requests and returning responses for the API.
- **models.py**: Defines the data models for the application (e.g., User, Task).
- **serializers.py**: Serializers for converting complex data types, such as querysets, into JSON format.
- **requirements.txt**: Lists the Python packages required to run the backend.
### Frontend
- **main.js**: The entry point for the Vue.js application, setting up the Vue instance.
- **App.vue**: The root component of the application, containing the main layout and structure.
- **components/**: Directory containing reusable Vue components (e.g., TaskList, TaskCard, NavMenu).
- **views/**: Directory containing the different views for the application (e.g., HomeView, CalendarView, PomodoroView).
- **router.js**: Defines the routing for the Vue application, mapping URLs to components.
- **store.js**: Pinia store setup for state management across components.
- **package.json**: Contains metadata about the project and lists npm dependencies.

## Development Process 🤔

### Ideation 💡

The journey of Focusty commenced on February 1st, 2024. Struggling to find an accessible time management app, I decided to develop my own. While it's currently in its early stages and may not match established platforms, it's a work in progress, continuously evolving based on user feedback and technological advancements. Passionate about empowering users to optimize productivity, I'm committed to its ongoing improvement.

### Implementation 🚀

Leveraging a comprehensive tech stack comprising Vue, Vite, Axios, Chart.js... for frontend and Python, Django, RestFramework... for backend and a myriad of other cutting-edge technologies, development commenced with meticulous attention to detail and relentless pursuit of perfection. From user authentication to task management and analytics, each feature was meticulously crafted to deliver a seamless user experience. Although the app is still in its early stages and may not yet meet industry standards, it's continuously evolving with a plethora of new features and improvements on the horizon.

### Refinement 🛠️

Throughout the development process, feedback loops were integral to refining and enhancing Focusty's functionality and usability. Iterative improvements, bug fixes, and performance optimizations were rigorously implemented to ensure that Focusty exceeded user expectations.

## Roadmap 🗺️

- **Enhanced Task Features**: Implement sub tasks, and categories to elevate task management capabilities.
- **Integration with External Tools**: Seamlessly integrate with popular productivity tools such as Google Calendar and Trello to streamline workflows and maximize efficiency.
- **Security Enhancements**: Regular security audits and data encryption, **OAuth** Integration to simplify login while maintaining security.


## Contributing 🤝

Contributions are invaluable to the continued evolution of Focusty. Whether you have ideas for new features, enhancements, or bug fixes, we welcome your contributions with open arms. Please feel free to open an issue or submit a pull request to join us on this exciting journey of productivity innovation.

## License 📄

This project is licensed under the MIT License.

