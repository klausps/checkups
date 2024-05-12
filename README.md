# Server Shutdown Based on UPS Status and Battery Level

This repository contains a simple Python script that automates server shutdown based on the UPS (Uninterruptible Power Supply) status (`OL` - On-Line) and battery level.

## Contents

The repository includes three primary files:

- `checkstatus.py`: A simple script that utilizes a basic class implementing the NUT (Network UPS Tools) protocol in cleartext.
- `NUTClient.py`: The class file which contains the implementation of the NUT protocol interactions.
- `config.py`: Contains basic configuration variables such as the server address, username, password, and battery threshold.

## Collaboration

Feel free to fork this repository and contribute to its improvement. Pull requests and suggestions are welcome!

## Setup and Usage

1. **Clone the repository:**
git clone https://github.com/klausps/checkups.git


2. **Configure your settings in `config.py`**:
- Set the server address, username, and password as per your UPS setup.
- Adjust the battery threshold according to your needs.

3. **Run the script:**

python checkstatus.py
## License

This project is licensed under the MIT License - see the `LICENSE` file for details (to be added if not already present).
