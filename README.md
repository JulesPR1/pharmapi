# PharmAPI

PharmAPI is a FastAPI-based web scraping project that extracts data from a WebMD. It provides an API to retrieve information about various medications, including their names, descriptions, and other relevant details.

## Features

- Scrapes data from WebMD to store information about various medications.
- Provides a RESTful API to access the scraped data.
- Allows users to search for medications by name or other criteria.
- Returns detailed information about each medication, including its name, description, and other relevant details.

## Installation

1. Clone the repository:

  ```bash
  git clone git@github.com:JulesPR1/pharmapi.git
  ```

2. Navigate to the project directory:

  ```bash
  cd pharmAPI
  ```

3. Install the dependencies:

  ```bash
  pip install -r requirements.txt
  ```

## Usage

1. Start the FastAPI server:

  ```bash
  uvicorn app.main:app --reload
  ```

2. Open your web browser and navigate to `http://localhost:8000/` to access the Swagger UI documentation.

3. Use the provided endpoints to interact with the API and retrieve medication data.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.

2. Create a new branch:

  ```bash
  git checkout -b feature/your-feature-name
  ```

3. Make your changes and commit them:

  ```bash
  git commit -m "commit message"
  ```

4. Push your changes to your forked repository:

  ```bash
  git push origin feature/your-feature-name
  ```

5. Open a pull request on the original repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or suggestions, feel free to reach out to the project maintainer on discord: @elphasmo