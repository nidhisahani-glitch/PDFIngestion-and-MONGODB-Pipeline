# AI_Internship_Task

### Project Title: PDF Ingestion and MongoDB Pipeline :
My project provides a streamlined pipeline for ingesting PDFs, processing their contents, and storing relevant data in MongoDB. The pipeline ensures concurrency using Python's ThreadPoolExecutor to handle multiple PDF files efficiently, with robust error handling and logging. To simplify deployment, Docker is used to package the application, ensuring portability and ease of setup across different environments.
### RELATED STEPS 
Concurrent PDF ingestion: Utilizes ThreadPoolExecutor to process multiple PDFs in parallel.
MongoDB integration: Stores processed data into MongoDB for further analysis or querying.
Error handling: Logs any errors encountered during PDF processing, ensuring the pipeline's stability.
Dockerized setup: Easily deployable with Docker, providing a consistent environment across different systems.
### Requirements
Docker (for containerized deployment)
MongoDB (either locally installed or accessible as a cloud service)
Python 3.8+

### Python packages:
Refer to requirements.txt for a full list of dependencies.
### Project Structure
.
├── app
│   ├── PDF.py               # Main script for PDF ingestion and processing
│   ├── utils.py             # Utility functions for error handling, logging, etc.
│   ├── Dockerfile           # Docker configuration
│   ├── requirements.txt     # List of Python dependencies
│   └── README.md            # Project documentation

### Setup Instructions
1. Clone the repository :
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
2. Install dependencies:
If you are not using Docker, install the required Python packages:
pip install -r requirements.txt
3. Run the application:
To run the pipeline directly on your machine (without Docker):
python PDF.py
4. Docker Setup
Build the Docker Image:
docker build -t pdf-ingestion-app .
5. Run the Docker Container:
docker run -p 5000:5000 pdf-ingestion-app
This command runs the containerized app on port 5000. You can adjust the port mapping if needed.
6. MongoDB Setup
Ensure MongoDB is running and accessible. If you are using a local of MongoDB, make sure it’s running on port 27017. Alternatively, you can use a cloud-based MongoDB service.Configure your MongoDB connection string in the application using environment variables or directly in the script.

Optional: Use Docker Compose (For MongoDB + App)
If you'd like to set up MongoDB and the application together using Docker Compose, you can create the following docker-compose.yml file:

version: '3'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mongo
    environment:
      - MONGO_URI=mongodb://mongo:27017/mydb
  mongo:
    image: mongo
    ports:
      - "27017:27017"

docker-compose up
This will start both MongoDB and your application.

### Logging
Error logs and status messages are stored to track the ingestion process and any issues that arise during the execution. You can find logs in logs/ folder (if implemented).

### Contributing
Feel free to submit a pull request or open an issue if you encounter any bugs or have suggestions for improvement.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
