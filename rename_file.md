```markdown
---
title: "SAST Scanning With SonarQube and Docker"
slug: "sast-scanning-with-sonarqube-and-docker"
subtitles: "Learn how to set up and use SonarQube for Static Application Security Testing (SAST) with Docker."
tags: ["SAST", "SonarQube", "Docker", "Security", "DevSecOps"]
cover: "path/to/cover/image.jpg"
domain: "damienjburks.hashnode.dev"
saveAsDraft: true
enableToc: true
---

# SAST Scanning With SonarQube and Docker

What's going on y'all? It's Damien with the DevSecBlueprint once again with another technical video. And in today's video, we're going to be performing SAST scans against code repositories using SonarQube. If you haven't taken a look at my video about SAST and DAST concepts, I highly recommend you look at it before we get started, since it'll give you a pretty decent overview of what SAST scanning is.

And with that being stated, let's get right into it.

## Prerequisites

Before we start talking about SonarQube or sonar scanning in general, let's talk about some of the prerequisites, right? On what it is that you actually need to have installed on your machine in order for you to be able to participate in this activity.

1. **[Docker](https://www.docker.com/products/docker-desktop)**
    - We're going to be launching the application from Docker and also running the scans using Docker as well.
    
2. **[VS Code](https://code.visualstudio.com/)**
    - This is not a hard requirement but highly recommended for viewing and editing files like the Markdown file and Docker Compose YAML file.

> Note: Links to all the prerequisites, including the YouTube video about SAST and DAST scanning concepts, are located in the description.

![Docker Logo](path/to/docker-logo.png)
![VS Code Logo](path/to/vscode-logo.png)

## Understanding SonarQube

### What is SonarQube?

SonarQube is a self-managed automatic code review tool that systematically helps you deliver clean code. I've used SonarQube several times within the past to help me out with DevSecOps related work or really to scan my code.

![SonarQube](path/to/sonarqube-image.png)

The application can be integrated with various different IDEs and pipelines to build, test, and deploy your code, and to be able to scan your code for all kinds of issues—not just security issues. It could be refactoring issues that your code has and many other things.

Key features include:

1. **Quality Gates**: A score that defines how well-maintained and secure your entire application code base is.
2. **Supports 30+ Languages**: Including popular languages and frameworks.
3. **Integration with DevOps Platforms**: GitHub, GitLab, BitBucket, Azure, etc.
4. **Fast Analysis and Unified Configurations**
5. **SonarLint IDE Integration**

For our SAST scanning purposes, we are going to focus on leveraging SonarQube and the Sonar Scanner to identify security vulnerabilities within our code.

### Community Edition

SonarQube is free and open-source (unless you opt for the enterprise or data center editions). We will use the Community Edition, which still covers many features that help us scan our code for various issues.

## Understanding Docker Compose

Docker Compose is a tool for defining and running a multi-container Docker application. It simplifies the control of your entire application stack, making it easy to manage services, networks, and volumes in a single YAML file configuration.

### Key Benefits

![Docker Compose](path/to/docker-compose-image.png)

1. **Efficient Development and Deployment**: One command to start all services from a configuration file.
2. **Environment Friendly**: Works in various environments like production, staging, development, and testing.
3. **CI Workflows**: Can be integrated into your continuous integration workflows.

## Technical Activity

### Setting Up SonarQube with Docker Compose

Let's get into the technical activity and start setting up SonarQube with Docker Compose.

1. **Clear your terminal**:
    ```bash
    clear
    ```

2. **Docker Compose YAML File**

Here’s the `docker-compose.yml` file we will use:

```yaml
version: '3.8'

services:
  sonarqube:
    image: sonarqube:community
    ports:
      - "9000:9000"
    environment:
      - SONAR_JDBC_URL=jdbc:postgresql://db:5432/sonar
      - SONAR_JDBC_USERNAME=sonar
      - SONAR_JDBC_PASSWORD=sonar
    depends_on:
      - db

  db:
    image: postgres:latest
    environment:
      - POSTGRES_USER=sonar
      - POSTGRES_PASSWORD=sonar
      - POSTGRES_DB=sonar

volumes:
  sonarqube_data:
  sonarqube_extensions:
  sonarqube_logs:
```

3. **Deploy SonarQube using Docker Compose:**

    ```bash
    docker-compose up -d
    ```

Give it about 4-5 minutes to download and set up the necessary Docker container images for SonarQube and its database.

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

Generate a token for Sonar Scanner and keep it safe as you'll need it for the scanning process.

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

- Example: Enable SSL certification validation on connections where it’s set to false.

![Security Vulnerabilities](path/to/security-vulnerabilities.png)

**Code Smells**:

SonarQube also identifies code smells and provides recommendations to improve the code quality.

- Example: Avoid duplicating strings or literals multiple times.

![Code Smells](path/to/code-smells.png)

## Conclusion

SonarQube is a powerful tool for static application security testing (SAST). It allows you to identify vulnerabilities and code smells efficiently, ensuring that your application codebase is both secure and maintainable.

Thank you so much for reading! I hope you were able to take away valuable insights about setting up and using SonarQube and the Sonar Scanner. Please make sure you like, subscribe, and drop a comment down below letting me know what you think about this guide and the blog overall.

![Thank You](path/to/thank-you.png)

---

*Go to the top of the page to view the Table of Contents.*
```