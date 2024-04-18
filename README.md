# The DSB Digest

<p align="center"><img src="./assets/readme_diagrams/Default%20Banner.svg" /></p>

## Overview

This repository will contain a list of all blog posts that are uploaded/committed to Hashnode, Medium, and Dev.TO. This is the parent repository for the DevSec Blueprint and all of Damien's blog posts that he's written over the course of his career.

>**PSA:** Make sure you read your own damn docs for your own good, because you and I both know you tend to _"forget"_!

## Architecture Diagram

![Default Architecture Diagram](./assets/readme_diagrams/architecture_diagram.drawio.svg)

### Architecture Diagram Summary

1. A blogger, referred to as "ME", uses a "DSB Blogging Assistant" to create a blog post in Markdown format. The blogger checks in the blog post (MD) to a "Source Repo" (a source repository, likely on GitHub).
1. Once the blog post (MD) has been checked into the source repository, Hashnode grabs the latest blog post and publishes it as a "draft" unless specified otherwise in the blog.
1. GitHub Actions, which are automated tasks, are then triggered to sync, process, and process the markdown file from the repository.
1. The GitHub Actions are part of a workflow that includes an automated process to replicate the post from Hashnode to Dev.TO and Medium. There is some comparative analysis that takes place here.
1. The blog posts are published to Medium and Dev.TO, with the canonical URL set to the Hashnode Blog (the original blogging site).

## Installation Instructions

1. Install the dependencies listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

1. Format the code using Black:

    ```bash
    black .
    ```

1. Lint the code using Pylint:

    ```bash
    pylint .
    ```

1. Execute Python Application:

    ```bash
    python src/main.py
    ```

    > **NOTE**: Make sure you have all of our environment variables configured before doing this. If you aren't sure, check out the GitHub Actions.

## Things to Remember - Seriously....

1. Medium sucks, and it doesn't support Markdown images (at least all of them). Don't do embedded markdown images.
1. Medium sucks. Only PNGs or JPGs.
1. Medium sucks. Make sure you pay attention to the APIs. They aren't supported anymore (EOL).