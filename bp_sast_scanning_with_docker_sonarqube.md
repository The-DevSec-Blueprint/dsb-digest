---
title: SAST Scanning with SonarQube and Docker
slug: sast-scanning-with-sonarqube-and-docker
subtitle: Learn how to set up and use SonarQube for Static Application Security Testing (SAST) with Docker.
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1716750474233/-LD2XXalL.png?auto=format
domain: damienjburks.hashnode.dev
tags: docker, cybersecurity, owasp, tutorial
saveAsDraft: true
enableToc: true
seriesSlug: sast-dast-docker
seriesName: SAST and DAST Scanning with Docker
---

## Introduction

As a seasoned Cloud DevSecOps Engineer with a keen interest in integrating robust security practices into the development lifecycle, I am thrilled to share insights and practical knowledge on enhancing code security. In this article, we will delve into the powerful combination of SAST (Static Application Security Testing) using SonarQube and Docker and explore how these tools can fortify your applications against vulnerabilities from the very start of the development process. This is a technical blog post or article, so get ready for some code to be shared and repositories to get cloned using Git.

## Prerequisites

Before we start talking about SonarQube or sonar scanning in general, let's talk about some of the prerequisites, right? On what it is that you actually need to have installed on your machine in order for you to be able to participate in this activity.

![Docker Logo](path/to/docker-logo.png)
![VS Code Logo](path/to/vscode-logo.png)
![Git](path/to/git-logo.png)

1. **[Docker](https://www.docker.com/products/docker-desktop)** - We're going to be launching the application from Docker and also running the scans using Docker as well.

1. **[VS Code](https://code.visualstudio.com/)** - This is not a hard requirement but highly recommended for viewing and editing files like the Markdown file and Docker Compose YAML file.

1. **[Git](https://git.com)** - We're going to need this to clone and checkout the repositories.

## Understanding SonarQube

### What is SonarQube?

SonarQube is a self-managed automatic code review tool that systematically helps you deliver clean code. I've used SonarQube several times within the past to help me out with DevSecOps related work or really to scan my code.

![SonarQube](path/to/sonarqube-image.png)

The application can be integrated with various different IDEs and pipelines to build, test, and deploy your code, and to be able to scan your code for all kinds of issues—not just security issues. It could be refactoring issues that your code has and many other things. Here are some key features of SonarQube:

1. **Quality Gates**: A score that defines how well-maintained and secure your entire application code base is.
2. **Supports 30+ Languages**: Including popular languages and frameworks.
3. **Integration with DevOps & CI Platforms**: GitHub, GitLab, BitBucket, Azure, etc.
4. **Fast Analysis and Unified Configurations**
5. **SonarLint IDE Integration**

For our SAST scanning purposes, we are going to focus on leveraging SonarQube and the Sonar Scanner to identify security vulnerabilities within our code.

No need to worry about paying though. SonarQube is free and open-source (unless you opt for the enterprise or data center editions). We will use the Community Edition, which still covers many features that help us scan our code for various issues.

## Understanding Docker Compose

Docker Compose is a powerful tool designed to define and manage multi-container Docker applications with ease. By using a single YAML file, Docker Compose allows developers to configure the various services, networks, and volumes that comprise their application stack, streamlining the deployment and management processes.

### Key Features and Benefits

#### Simplified Configuration

Docker Compose uses a YAML file, commonly named `docker-compose.yml`, to define the entire application stack in a human-readable format. This file outlines each service in your application, the Docker images they use, and any dependencies between them. This simplifies the setup process, making it easy to replicate the environment across different machines or teams.

#### Multi-Container Applications

With Docker Compose, you can define multiple services that work together, such as a web server, a database, and a cache service. Each service runs in its own container, ensuring isolation and consistency. This modular approach allows you to scale individual components independently and manage complex applications with ease.

#### Network Management

Docker Compose automatically handles the creation and management of networks for your containers. It allows different services to communicate with each other seamlessly, using service names as hostnames. This built-in networking capability eliminates the need for manual network configuration and simplifies inter-service communication.

#### Volume Management

Persisting data is crucial for many applications. Docker Compose allows you to define volumes in your configuration file, ensuring that data is not lost when containers are stopped or recreated. Volumes can be shared between services, enabling data persistence and easy access across different components of your application.

#### Environment Configuration

Docker Compose supports environment variables, making it easy to manage different configurations for various environments (development, testing, production). By defining environment variables in the YAML file or in an `.env` file, you can customize service behavior without modifying the application code.

## Scanning and Inspecting Sonar Results

Let's get into the technical activity and cloning and setting up the vulnerable web application and SonarQube using Docker Compose and Git.

### Cloning Vulnerable Web Application (TIWAPP)

First, you’ll need to clone the **TWAPP** web application repository. I've specified the URL in the command below:

```bash
git clone <repository-URL>
cd <cloned-repo-directory>
```

#### Spinning Up the Environment

We will use Docker Compose to set up the necessary environment:

```bash
docker-compose up -d
```

>**NOTE**: The `-d` flag runs the container in detached mode, but if you want to see real-time logs, you can run:

```bash
docker-compose up
```

### Verifying the Setup

To ensure the environment is up and running, navigate to `http://localhost:8000` in your web browser.

### Setting Up SonarQube with Docker Compose

1. **Clear your terminal**:

    ```bash
    clear
    ```

1. **Docker Compose YAML File**

Here’s the `docker-compose.yml` file we will use:

```yaml
version: "1"

services:
  sonarqube:
    image: sonarqube:lts-community
    depends_on:
      - sonar_db
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://sonar_db:5432/sonar
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: sonar
    ports:
      - "9001:9000"
    volumes:
      - sonarqube_conf:/opt/sonarqube/conf
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_extensions:/opt/sonarqube/extensions
      - sonarqube_logs:/opt/sonarqube/logs
      - sonarqube_temp:/opt/sonarqube/temp

  sonar_db:
    image: postgres:13
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
      POSTGRES_DB: sonar
    volumes:
      - sonar_db:/var/lib/postgresql
      - sonar_db_data:/var/lib/postgresql/data

volumes:
  sonarqube_conf:
  sonarqube_data:
  sonarqube_extensions:
  sonarqube_logs:
  sonarqube_temp:
  sonar_db:
  sonar_db_data:
```

1. **Deploy SonarQube using Docker Compose:**

    ```bash
    docker-compose up -d
    ```

Give it about 5-10 minutes to download and set up the necessary Docker container images for SonarQube and its database.

### Logging into SonarQube

Once SonarQube is fully operational, navigate to `http://localhost:9000` in your web browser.

1. **Login Credentials**:
    - **Username**: `admin`
    - **Password**: `admin`

2. **Change the default password** when prompted.

![SonarQube Login](path/to/sonarqube-login.png)

### Creating a Project in SonarQube

Create a new project in SonarQube to scan. For this example, we'll use a **vulnerable web application from GitHub**.

- **Project Key**: `test-vulnerable-app`
- **Project Name**: `Test Vulnerable App`

You'll want to generate a token for Sonar Scanner and keep it safe as you'll need it for the scanning process.

### Running Sonar Scanner using Docker

Navigate to your project directory in the terminal where you have cloned the vulnerable web application repository.

```bash
cd /path/to/your/project-directory
```

Run the following command to scan your project with SonarQube:

```bash
docker run --rm --network=host -e SONAR_HOST_URL="http://localhost:9000" -e SONAR_LOGIN="your-generated-token" -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli
```

The scan will take some time. Once completed, results will be published to your SonarQube project:

![SonarQube Scan Results](path/to/scan-results.png)

### Reviewing Results in SonarQube

Log into the SonarQube console and navigate to your project to review the results. The scan results will be categorized into different sections like Bugs, Vulnerabilities, Code Smells, etc.

**Security Vulnerabilities**:

Security vulnerabilities are critical issues within your code that can be exploited by malicious actors to compromise the integrity, confidentiality, or availability of your application. Identifying and addressing these vulnerabilities is paramount to maintaining a secure codebase. SonarQube's SAST (Static Application Security Testing) capabilities help detect these issues early in the development lifecycle, enabling you to fix them before they become significant problems.

- **Example: Enable SSL Certification Validation**:
  
  One common security vulnerability is having SSL certification validation disabled in your application. SSL (Secure Sockets Layer) certificates are essential for establishing encrypted connections between clients and servers, ensuring that data transferred over the network is secure and cannot be intercepted by unauthorized parties. If SSL certification validation is set to false, your application is vulnerable to man-in-the-middle (MITM) attacks, where attackers can intercept and manipulate the data being exchanged.

  **Solution**:
  Ensure that SSL certification validation is enabled in all your connections. This can usually be done by configuring the appropriate settings in your application's connection properties or environment variables. For example, in a Python application using the `requests` library, you should ensure SSL verification is enabled:

  ```python
  import requests

  # Correct way with SSL verification enabled
  response = requests.get('https://example.com', verify=True)
  ```

  By enabling SSL certification validation, you can protect your application from potential security breaches and ensure that your data remains secure.

  ![Security Vulnerabilities](path/to/security-vulnerabilities.png)

**Code Smells**:

Code smells are indicators of potential problems in your code that, while not necessarily bugs, can lead to maintainability issues and increased technical debt. SonarQube identifies code smells and provides recommendations to improve the quality, readability, and maintainability of your code. Addressing code smells helps ensure that your codebase remains clean and efficient, making it easier to manage and extend over time.

- **Example: Avoid Duplicating Strings or Literals**:
  
  A common code smell is the duplication of strings or literals multiple times throughout your code. This practice can lead to inconsistencies and make your code harder to maintain. For instance, if a string value changes, you will need to update it in multiple places, increasing the risk of errors and inconsistencies.

  **Solution**:
  Use constants or configuration files to store commonly used strings or literals. This approach centralizes the values, making your code more manageable and reducing the risk of errors. For example, in a Python application, you might define constants in a separate module:

  ```python
  # constants.py
  WELCOME_MESSAGE = "Welcome to our application!"
  ERROR_MESSAGE = "An error has occurred."
  ```

  Then, you can use these constants throughout your code instead of duplicating the string values:

  ```python
  # main.py
  from constants import WELCOME_MESSAGE, ERROR_MESSAGE

  def greet_user():
      print(WELCOME_MESSAGE)

  def handle_error():
      print(ERROR_MESSAGE)

  greet_user()
  handle_error()
  ```

  By avoiding the duplication of strings or literals, you can improve the maintainability and readability of your code, making it easier to update and extend in the future.

  ![Code Smells](path/to/code-smells.png)

By addressing both security vulnerabilities and code smells, you can ensure that your codebase is not only secure but also clean and maintainable, leading to more robust and reliable software development practices.

## Conclusion

SonarQube is a powerful tool for static application security testing (SAST). It allows you to identify vulnerabilities and code smells efficiently, ensuring that your application codebase is both secure and maintainable.

Thank you so much for reading! I hope you were able to take away valuable insights about setting up and using SonarQube and the Sonar Scanner. Please make sure you like, subscribe, and drop a comment down below letting me know what you think about this guide and the blog overall.
