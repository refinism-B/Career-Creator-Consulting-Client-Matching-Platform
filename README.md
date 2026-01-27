# Career Creator Consulting Client Matching Platform

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-black)

A professional client matching platform designed for the **Career Creator** ("職游") program. This application facilitates the connection between trainee career consultants and potential clients for practice sessions. It is built with **Streamlit** for the frontend and leverages **Google Sheets** as a cloud-based database, ensuring real-time data synchronization and ease of access.

## 📖 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)

## 🚀 Introduction

The **Consulting Client Matching Platform** solves the challenge of finding suitable practice clients for career consultant trainees. It discourages trainees from consulting with close friends or family by providing a shared pool of external volunteers.

The system allows users to:
1.  **Register** potential clients (friends/acquaintances) into a shared database.
2.  **Search** for suitable clients based on specific criteria (e.g., age, region, consultation mode).
3.  **Manage** client status (e.g., mark as "Reserved" or "Pending").

> **Note**: This platform is for information exchange only. Users are responsible for contacting the referrer ("Member") to arrange the actual consultation.

## ✨ Features

-   **User-Friendly Interface**: Intuitive web interface built with pure Python using Streamlit.
-   **Real-time Synchronization**: Seamless integration with Google Sheets API for data storage.
-   **Smart Filtering**: Advanced search capabilities allowing multi-select filtering by Age, Region, Gender, and Consultation Mode.
-   **Data Validation**: Robust Pydantic models ensure data integrity before submission.
-   **Efficient Caching**: Implements local caching strategies to minimize API calls and enhance performance.
-   **Conflict Prevention**: Automatic duplicate checking based on client names.

## 🏗 System Architecture

The project follows a **Client-Server** architecture where the "Server" logic is embedded within the application but logically separated.

-   **Frontend**: Streamlit App (`app.py`) managing UI, Session State, and Faceted Search.
-   **Backend Logic**: `ClientManager` (`src/manage.py`) handling caching, filtering, and CRUD operations.
-   **Data Layer**: `GoogleSheetService` (`src/database.py`) communicating with the Google Sheets API.
-   **Data Model**: Pydantic models (`src/client.py`) for strong typing and validation.

## 📂 Project Structure

```text
/
├── app.py          # Application Entry Point (Streamlit Interface)
├── src/
│   ├── client.py   # Data Models (Pydantic)
│   ├── config.py   # Configuration & Path Management
│   ├── database.py # Google Sheets API Wrapper
│   ├── general.py  # Utility Functions
│   └── manage.py   # Business Logic & State Management
├── doc/            # Documentation
└── key/            # API Credentials (ensure you have drive.json)
```

## ⚙️ Installation

### Prerequisites

-   Python 3.9 or higher
-   A Google Cloud Service Account JSON key (for Google Sheets API access)

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/career-creator-matching-platform.git
    cd career-creator-matching-platform
    ```

2.  **Install Dependencies**
    We use `poetry` (or `pip`) for dependency management.
    ```bash
    pip install streamlit pandas pydantic gspread google-auth
    ```

3.  **Setup Credentials**
    Place your Google Service Account key file in the `key/` directory.
    -   Rename the file to `drive.json`.
    -   Ensure the Service Account has **Editor** access to the target Google Sheet (`consulting_client`).

## 🔧 Configuration

Configuration variables are managed in `src/config.py`.

-   **CREDENTIAL_PATH**: Path to your Google API key (`key/drive.json`).
-   **DATA_PATH**: Path for local development data fallback (optional).

## 🖥 Usage

Run the application using Streamlit:

```bash
streamlit run app.py
```

The application will launch in your default web browser (usually at `http://localhost:8501`).

### Workflow

1.  **Home**: Briefing and navigation.
2.  **Add Client**:
    -   Fill in details: Name, Gender, Age, Area, Location, Mode, and Referrer (Member).
    -   Submit to add to the global pool.
3.  **Search Client**:
    -   Use the sidebar or filter panel to refine results.
    -   View list of available clients.
    -   Edit status (e.g., change "Pending" to "Reserved") and save changes directly in the UI.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

**Developed for Career Creator (職游)** | *Facilitating Professional Growth through Connection*