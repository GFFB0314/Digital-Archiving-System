# Project Title: **xSAVE** 🚀

Welcome to **xSAVE** – a feature-rich, cross-platform solution designed to simplify your workflow and boost productivity! This project is built using cutting-edge technologies and robust libraries, ensuring a smooth user experience and high performance across different operating systems. Below, you'll find a comprehensive guide detailing what our project is about, the tools and frameworks we used, and a step-by-step walkthrough on how to set up, run, and even compile your own executable version of the application.

---

## Table of Contents
- [Project Title: **xSAVE** 🚀](#project-title-xsave-)
  - [Table of Contents](#table-of-contents)
  - [About the Project 📖](#about-the-project-)
  - [Technologies \& Libraries Used 🛠️](#technologies--libraries-used-️)
  - [Getting Started 🚀](#getting-started-)
  - [Usage Guide 📝](#usage-guide-)
  - [Building an Executable 🔧](#building-an-executable-)
  - [Contributing 🤝](#contributing-)
  - [Contact 📬](#contact-)

---

## About the Project 📖

**xSAVE** is designed to serve as a comprehensive toolkit for managing everyday tasks efficiently. Whether you are a developer, a data analyst, or simply looking for a more organized way to handle daily challenges, this project aims to offer intuitive interfaces and powerful functionality. By combining a modern graphical interface with back-end support through SQLite databases and various utilities, the application is a perfect blend of practicality and innovation.

The application leverages the robust features of [Kivy](https://kivy.org/), a Python framework for developing multitouch applications, in tandem with [KivyMD](https://github.com/kivymd/KivyMD) for Material Design components, ensuring that both aesthetics and usability are at the forefront. In addition, the integration of [pygame](https://www.pygame.org/news) facilitates multimedia and game-like elements, making the application versatile and engaging.

---

## Technologies & Libraries Used 🛠️

The project is built with the following key libraries, modules, and frameworks:

- **Kivy**: A modern framework for developing multitouch applications that run on multiple platforms.
- **KivyMD**: Material Design components for Kivy, installed via:
```bash
pip install https://github.com/kivymd/KivyMD/archive/master.zip
```
- **pygame**: A set of Python modules designed for writing video games, offering robust multimedia capabilities.

- **fpdf2**: A lightweight library for generating PDFs, ideal for creating reports or exporting data.

- **sqlite3**: A built-in Python module that provides a simple and efficient SQL database engine.

- **sys, os, subprocess**: Built-in Python modules for system-level operations, environment management, and process handling.

- **black**: A powerful code formatter that enforces a consistent style throughout the codebase.

- **mypy**: A static type checker to improve code quality and catch potential bugs.

- **pylint**: A linter that ensures your code adheres to Python’s coding standards and best practices.

- **pytest**: A testing framework that makes it easy to write simple as well as scalable test cases for your code.
Use the following command to install the dependencies:
```bash
pip install kivy pygame fpdf2 black mypy pylint pytest
```

## Getting Started 🚀
**Prerequisites** 📌
Before you start, ensure you have the following installed on your system:

- Python 3.6 or higher

- pip (Python package installer)

Additionally, you will need to have a Git client installed to clone the repository.

**Installation Steps** 🛠️
1. **Clone the Repository**
   Open your terminal or command prompt and run:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   ```
   This command will create a local copy of the project on your machine.

2. **Navigate to the Project Directory**
   Change to the project directory:
   ```bash
   cd your-repo
   ```

3. **Install the Required Libraries**
   Install the dependencies using `pip`:
   ```bash
   pip install https://github.com/kivymd/KivyMD/archive master.zip
   pip install kivy pygame fpdf2 black mypy pylint pytest
   ```
   **Note**: sqlite3, sys, os, and subprocess are built-in modules in Python and do not require installation

4. **Verify Installation**
   Ensure that all packages are correctly installed by running:
   ```bash
   pip list 
   ```
   This should display a list of installed packages, including all the dependencies mentioned.

## Usage Guide 📝
Once the installation is complete, you can start using **xSAVE**. Here’s how:
1. **Run the Application**
   To run the application, simply execute your main Python script:
   ```bash
   python main.py 
   ```
   This command will launch the application window with its intuitive GUI, and you can start interacting with it immediately. The default admin credentials are uername: `root` and password: `root`. 
   You can see the other users of the applications by running the program `display_users.py` found in the `data` directory.
   To do so, run the command below:
   ```bash
   cd data
   python display_users.py
   ```
2. **Updating the Application**
    You can edit the app as you want to ensure that it matches your needs and expectations.

## Building an Executable 🔧
If you want to distribute **xSAVE** as a standalone executable, follow these steps:
1. **Edit the Spec File**
   Locate the spec file (e.g., xSAVE.spec) in the repository. Modify it if necessary to adjust settings such as the application name, icon, or additional data files.
2. **Generate the Executable**
    Run the following command to build the executable:
    ```bash
    pyinstaller xSAVE.spec
    ```
    This command uses PyInstaller to package the application into an executable file, making it easy to distribute and run on machines without Python pre-installed.
    **Note**: Ensure `pyinstaller` is correctly installed in your computer. 
    Run the following command to install `pyinstaller`
    ```bash
    pip install pyinstaller
    ```
3. **Locate the Executable**
   After the build process completes, you will find the executable in the dist folder within your project directory. You can now share this executable with your users! The executable may not work when located inside the `dist` folder, cut and paste it in the `root` directory containing your `python` and `kivy` files.

## Contributing 🤝
We welcome contributions from the community! If you'd like to improve xSAVE, please fork the repository and submit a pull request. Before making significant changes, feel free to open an issue to discuss your ideas. All contributions, whether code, documentation, or bug reports, are greatly appreciated!

## Contact 📬
For any questions, issues, or suggestions, please feel free to contact us at:
- Email: gbetnkom.bechir@gmail.com
- GitHub Issues: Project Issues

Thank you for exploring **xSAVE!** We hope you find it as exciting and useful as we intended it to be. Happy coding! 😊
