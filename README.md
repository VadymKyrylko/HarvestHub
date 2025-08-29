# 🌱 HarvestHub

**HarvestHub** is a web-based system for planning and managing garden beds, plants, materials, tools, and maintenance tasks.  
The project is built with **Django** and uses **Bootstrap** for a responsive, consistent interface.

---

## Table of Contents
- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Database Structure](#database-structure)
- [Contributing](#contributing)
- [License](#license)

---

## About

HarvestHub helps organize gardening work — from planning beds and placing plants to managing inventory and scheduling maintenance tasks.  
It is suitable for both personal use and team collaboration with role-based access.

---

## Features

- **Garden Bed Management** — create beds, divide them into sections, track dimensions, and calculate area.
- **Plant Management** — store plant details, types, and space requirements.
- **Task Scheduling** — plan and assign maintenance tasks, track their status.
- **Resource Tracking** — manage materials and tools, including quantities, units, and usage in tasks.
- **User Roles & Access Control** — secure authentication, redirects, and role-based permissions.
- **Responsive UI** — unified Bootstrap card layouts, readable typography, and a themed background image.
- **Code Quality** — consistent code style enforced with flake8.


## Tech Stack

- **Backend:** Python 3.10+, Django
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** SQLite (default) / PostgreSQL
- **Other:** Django ORM, Django Forms, LoginRequiredMixin


## Installation

1. **Clone the repository**
    git clone https://github.com/yourusername/harvesthub.git
    cd harvesthub

2. **Create and activate a virtual environment**
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
3. **Install dependencies**
    pip install -r requirements.txt
4. **Apply migrations**
    python manage.py migrate
5. **Run the development server**
    python manage.py runserver

## Usage

Register or log in to the system.
Create garden beds, add sections, and assign plants.
Schedule tasks and assign materials and tools.
Use filters to search and sort tasks.

## Database Structure

See the attached ER diagram in the repository.
Main entities:
GardenBed ↔ BedSection ↔ Plant
MaintenanceTask ↔ M2M with Material and Tool
User with roles and access control

## Contributing

Fork the project
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request