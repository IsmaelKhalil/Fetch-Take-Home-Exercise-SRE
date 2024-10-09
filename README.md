# Fetch-Take-Home-Exercise-SRE
- [Take-Home Exercise](https://fetch-hiring.s3.us-east-1.amazonaws.com/site-reliability-engineer/health-check.pdf)

# Setting Up Git
1. Install [Git](https://git-scm.com/downloads) based on your OS.
2. Clone the repository with the following Git command, or download the ZIP file:
- `git clone https://github.com/IsmaelKhalil/Fetch-Take-Home-Exercise-SRE.git`
3. Use the command `cd Fetch-Take-Home-Exercise-SRE` to change into the project directory.

# Setting Up Python
1. Install [Python](https://www.python.org/downloads/) based on your OS.
   - During the installation, make sure to modify the installation by checking "Add Python to environment variables"
2. Open a Shell / Terminal / Command Prompt `python --version` to validate that it has successfully installed.
   - On Windows, you might receive the following message:
 	- `Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Manage App Execution Aliases.`
   - If this occurs, search for "Manage App Execution Aliases" in your Windows search menu and uncheck both `python.exe` and `python3.exe`
3. After installing Python, run the following commands:
- `pip install pyyaml`
- `pip install requests`

# Running the Project
1. In the Shell / Terminal / Command Prompt, run the command `python health_check.py`.
2. When prompted to enter the path to the configuration file, enter the path YAML file, i.e. `fetch-endpoints.yml`.
   - On certain operating systems you may need to enter the full path `Fetch-Take-Home-Exercise-SRE/fetch-endpoints.yml`
3. If successful, you will see the Endpoint statuses and availability percentages.

# Credits
- Solution by Ismael Khalil
- Problem Statement by Fetch Rewards
