# Crypto Trading Educational Platform

This is a full-stack educational platform for cryptocurrency trading. It includes a React frontend, a Node.js backend, and a Python engine for backtesting trading strategies.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Node.js (v18 or later)
*   pnpm
*   Python (v3.9 or later)

### Installation

1.  **Clone the repo**
    ```sh
    git clone https://github.com/your_username/your_repository.git
    ```
2.  **Set up the environment variables**

    Create a `.env` file in the root of the `crypto-trading-education-platform` directory by copying the example file:
    ```sh
    cp .env.example .env
    ```
    Then, open the `.env` file and fill in the required environment variables. At a minimum, you should set the following for the frontend to work:
    ```
    VITE_API_URL=http://localhost:3001/api
    ```
3.  **Install Frontend Dependencies**
    ```sh
    pnpm install
    ```
4.  **Install Backend Dependencies**
    ```sh
    cd backend
    npm install
    cd ..
    ```
5.  **Install Python Engine Dependencies**
    ```sh
    cd python-engine
    pip install -r requirements.txt
    cd ..
    ```

### Running the Application

1.  **Start the Backend Server**
    ```sh
    cd backend
    npm run dev
    ```
2.  **Start the Python Engine**
    ```sh
    cd python-engine
    python app.py
    ```
3.  **Start the Frontend Development Server**
    ```sh
    pnpm dev
    ```

The application should now be running at `http://localhost:5173`.

## Environment Variables

The application uses environment variables for configuration. You can find all the available variables in the `.env.example` file.

### Frontend (`VITE_` prefixed)

*   `VITE_API_URL`: The URL of the backend API.
*   `VITE_SENTRY_DSN`: The DSN for Sentry error tracking.
*   `VITE_APP_ENV`: The application environment (e.g., `development`, `production`).

### Backend

The backend has its own set of environment variables for database configuration, JWT secrets, and API keys. Please refer to the `.env.example` file for more details.
