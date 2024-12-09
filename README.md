# Ice Cream Parlor Application

This is a Python-based application for managing the operations of a fictional ice cream parlor. It uses SQLite to manage seasonal flavor offerings, ingredient inventory, customer flavor suggestions, and allergy concerns. The application also allows users to maintain a cart of their favorite products and manage allergens.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ice-cream-parlor.git
    cd ice-cream-parlor
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. (Optional) To run using Docker, ensure you have Docker Desktop installed and running.

## Running the Application
To run the application, you can either use Python or Docker:

### Using Python:
1. Ensure you have Python 3.x installed.
2. Run the application:
    ```bash
    python app.py
    ```
3. Visit `http://localhost:5000` in your browser.

### Using Docker:
1. Build the Docker image:
    ```bash
    docker build -t ice_cream_parlor .
    ```

2. Run the Docker container:
    ```bash
    docker run -p 5000:5000 ice_cream_parlor
    ```

3. Access the application at `http://localhost:5000`.

## Testing the Application
To test the application:
- Add seasonal flavors and ensure they appear in the offerings.
- Add ingredients to the inventory and ensure they are listed.
- Submit flavor suggestions and manage allergens.
- Test the cart functionality by adding and removing items.
- Verify the search and filter options work correctly.

## Docker Usage
Ensure Docker is running on your system before proceeding with the Docker commands. Docker will handle setting up the application with all dependencies and environment configurations.



