# Structural flow

![AWS web app structural flow](https://github.com/user-attachments/assets/82f72445-78f3-4cfb-bb67-b1354df29467)

### Workflow Overview

1. **Client Authentication**:
   - **Action**: The user logs in through the React application.
   - **Process**:
     - The React app sends user credentials to the AuthService via  Kong.
     - AuthService verifies the credentials and returns an authentication token, which will tthen be process by Kong to ensure authentication through all trafic.
     - The token is stored in the browser’s local storage for subsequent requests.

2. **Client Interaction**:
   - **Action**: The user sets search filters (e.g., price range, mileage) for car listings.
   - **Process**:
     - The React app sends the search criteria and the stored authentication token to the Scraper Task Producer via the Kong API Gateway.

3. **Scraper Task Producer**:
   - **Action**: The Scraper Task Producer generates a Facebook Marketplace search link based on the user’s filters.
   - **Process**:
     - The Scraper Task Producer scrapes the listing page, collecting all relevant car listing links.
     - It uses `concurrent.futures` to manage background tasks that run Selenium in parallel for scraping.
     - Once all links are collected, the task producer sends them to Kong API Gateway for further processing.

4. **Kong (API Gateway & Load Balancer)**:
   - **Action**: Kong handles routing and load balancing.
   - **Process**:
     - Kong verifies the authentication token provided by the Scraper Task Producer.
     - Kong distributes the scraping tasks to various instances in the NLP Services EC2 cluster based on load and availability.
     - It routes the requests to the appropriate NLP services.

5. **NLP Services**:
   - **Action**: The NLP services process car listing links.
   - **Process**:
     - Each instance in the NLP Services cluster processes the provided car listing links, extracting detailed attributes and filtering out undesired listings (e.g., scams, down payments).
     - NLP Services use `concurrent.futures` to manage background tasks that run Selenium for scraping and spaCy for NLP processing.
     - The processed data is then sent to the Scraped Content Service via Kong.

6. **Scraped Content Service**:
   - **Action**: The Scraped Content Service stores the processed car listings.
   - **Process**:
     - Kong verifies the authentication token provided by NLP Services.
     - The Scraped Content Service stores detailed car listings in its database using Django ORM.
     - It ensures data persistence and makes it accessible for future queries.

7. **SSE Service**:
   - **Action**: The SSE Service handles real-time updates.
   - **Process**:
     - The SSE Service monitors the Scraped Content Service for new car listings.
     - It uses Redis for pub/sub messaging to push updates to clients.
     - The React app subscribes to SSE events and updates the UI in real-time when new car listings are posted.

### Tech Stack and Deployment

#### 1. **Client Application (React)**
- **Tech Stack**:
  - **Frontend**: React
  - **UI Components**: Material-UI (MUI)
- **Deployment**:
  - **Hosting**: AWS S3
  - **Details**: The React application is built as static files and deployed on S3 for static website hosting.

#### 2. **AuthService**
- **Tech Stack**:
  - **Backend Framework**: Django
  - **Authentication**: Django REST Framework
- **Deployment**:
  - **Hosting**: AWS EC2
  - **Details**: The Django application is deployed on EC2 instances. AuthService is registered in Kong API Gateway for handling authentication requests.

#### 3. **Scraper Task Producer**
- **Tech Stack**:
  - **Backend Framework**: FastAPI
  - **Background Task Execution**: Python `concurrent.futures` (for managing background tasks)
  - **Web Scraping**: Selenium with Chrome
- **Deployment**:
  - **Hosting**: AWS EC2
  - **Details**: The FastAPI application is deployed on EC2. `concurrent.futures` manages background tasks for scraping using Selenium. The service is registered in Kong API Gateway with routes for scraping tasks.

#### 4. **NLP Services**
- **Tech Stack**:
  - **Backend Framework**: FastAPI
  - **NLP Library**: spaCy
  - **Background Task Execution**: Python `concurrent.futures` (for managing background tasks)
  - **Web Scraping**: Selenium with Chrome
- **Deployment**:
  - **Hosting**: AWS EC2 (Cluster of instances)
  - **Details**: FastAPI applications run on multiple EC2 instances. `concurrent.futures` manages background tasks for Selenium and spaCy. Each service instance is registered in Kong API Gateway with routes for NLP processing.

#### 5. **Scraped Content Service**
- **Tech Stack**:
  - **Backend Framework**: Django
  - **ORM**: Django ORM
- **Deployment**:
  - **Hosting**: AWS EC2
  - **Details**: The Django application is deployed on EC2. It uses Django ORM to store data in a database. The service is registered in Kong API Gateway for content management.

#### 6. **SSE Service**
- **Tech Stack**:
  - **Backend Framework**: FastAPI
  - **Pub/Sub Broker**: Redis
- **Deployment**:
  - **Hosting**: AWS EC2
  - **Details**: The FastAPI application is deployed on EC2. Redis handles pub/sub messaging for real-time updates. The service is registered in Kong API Gateway for SSE endpoints.

#### 7. **Kong (API Gateway & Load Balancer)**
- **Tech Stack**:
  - **API Gateway**: Kong
  - **Load Balancing**: Kong
- **Deployment**:
  - **Hosting**: AWS EC2
  - **Details**: Kong is deployed on EC2 and configured for API management and load balancing. It routes requests to microservices and manages load distribution for NLP services.
