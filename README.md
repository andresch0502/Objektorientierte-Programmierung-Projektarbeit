# 📚 StudyPlanner – Study Planning

UI SHOWCASE BILD EINFÜGEN

---

This project demonstrates the development of a browser-based application using **NiceGUI**, focusing on clean architecture, task organization, progress tracking, and database integration via an ORM.

It aims to:

- Cover the full process from **requirements analysis to implementation**
- Apply advanced **Python** concepts in a web-based application
- Support students in organizing subjects, tasks, and study sessions
- Provide a clear overview of deadlines, progress, and urgent priorities
- Produce clean, maintainable, and well-structured code
- Support **teamwork and professional documentation**

---

## 📝 Application Requirements

### Problem

Students often struggle to organize their academic workload efficiently. Tasks, study sessions, and deadlines are frequently scattered across different tools, which can lead to missed deadlines, poor prioritization, and limited visibility into overall learning progress.

---

### Scenario

The application allows users to:

- organize subjects
- manage tasks and assignments
- plan study times
- display deadlines clearly
- track their learning progress
- receive recommendations for urgent tasks
- view a simple study statistics overview

---
## 📖 User Stories

### 1. Login User
**As a user, I want to log in so that I can access my personal dashboard and study data.**

- **Inputs:** email (`str`), password (`str`)  
- **Outputs:** dashboard (`Dashboard`)

---

### 2. View Dashboard
**As a user, I want to see my dashboard in the browser app so that I can get an overview of my tasks, deadlines, and study progress.**

- **Inputs:** none  
- **Outputs:** open tasks (`list[Task]`), upcoming deadlines (`list[date]`), planned study sessions (`list[StudySession]`), progress overview (`dict[str, float]`)

---

### 3. Manage Subjects / Modules
**As a user, I want to create and manage subjects or modules so that I can organize my studies.**

- **Inputs:** subject name (`str`), description (`str`), color (`str`), exam date (`date`), optional lecturer (`str | None`), action (`str`) = `create | edit | delete` 
- **Outputs:** created or updated subject list (`list[Subject]`)
  
---

### 4. Manage Tasks
**As a user, I want to create and manage tasks for a subject so that I can organize assignments and deadlines.**

- **Inputs:** title (`str`), description (`str`), subject Name (`str`), deadline (`date`), priority (`int`), status (`str`) = `open | in_progress | done`, action (`str`) = `create | edit | delete`
- **Outputs:** created or updated task list (`list[Task]`)

---

### 5. View User Data / System Overview (admin)
**As an admin, I want to view user and system data so that I can monitor and manage the application.**

- **Inputs:** none or selected user (`int | None`)
- **Outputs:** user list (`list[User]`), subjects (`list[Subject]`), tasks (`list[Task]`), system overview (`dict[str, int]`)

---
## 🧩 Use Cases

<img width="1404" height="1120" alt="image" src="https://github.com/user-attachments/assets/80f09e31-75a7-4c10-b508-19302cdae488" />


### Main Use Cases
- Login (User)  
- View Dashboard (User)  
- Manage Subject / Modules (User)  
- Manage Tasks (User)  
- View User Data / System Overview (Admin)  

### Actors
- User  
- Admin  

---

### Wireframes / Mockups



---

## 🏛️ Architecture

<img width="1223" height="695" alt="image" src="https://github.com/user-attachments/assets/1da9430e-ebb2-4398-a1ca-af227dd117ce" />


## Layers
- **UI:** NiceGUI (browser-based interface)
- **Application logic:** controllers and services
- **Persistence:** SQLite + ORM + data access (DAO)

## Design Decisions
- MVC structure (Model–View–Controller)
- Clear separation of concerns
- Business logic independent of UI

## Design Patterns Used
- **Model–View–Controller / Layered MVC Variant:** NiceGUI pages and controllers handle interaction, services implement the use cases, and persistence is separated into DAO/DB components.
- **Data Access Object (DAO):** DAOs isolate database queries and persistence from business logic.
- **Facade Pattern:** a database/facade component can centralize engine creation, schema setup, and session handling.


---

## 🗄️ Database and ORM

<img width="1385" height="506" alt="image" src="https://github.com/user-attachments/assets/4dd34835-a784-4e59-a393-41990b725de7" />


The application uses **SQLModel** to map domain objects to a SQLite database.

### Entities
- `User`
- `Subject`
- `Task`

### Relationships
- One `User` → many `Subject`
- One `Subject` has many `Task`

---
