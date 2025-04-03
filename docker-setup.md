
# Docker and Docker Compose Setup Guide

Ensure your system meets the requirements and follow the steps below to install and verify Docker and Docker Compose.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
   - [Windows (with WSL 2)](#windows-with-wsl-2)
   - [macOS](#macos)
   - [Linux](#linux)
3. [Verification](#verification)
4. [Troubleshooting](#troubleshooting)
5. [Additional Tips](#additional-tips)
6. [Summary](#summary)

---

## Prerequisites

### System Requirements

- **Windows**
  - Windows 10 64-bit: Pro, Enterprise, or Education (Build 15063 or later)
  - WSL 2 enabled
- **macOS**
  - macOS 10.14 or newer
- **Linux**
  - Most modern distributions (Ubuntu, Debian, Fedora, CentOS, etc.)
  - 64-bit processor
  - Minimum 4 GB RAM (8 GB recommended)
  - Virtualization enabled in BIOS/UEFI

---

## Installation

### Windows (with WSL 2)

#### 1. Install WSL 2

1. **Open PowerShell as Administrator**:

   ```powershell
   wsl --install
   ```

   This command installs WSL 2 along with the default Linux distribution (usually Ubuntu).

2. **Restart Your Computer** when prompted.

3. **Set WSL 2 as Default**:

   ```powershell
   wsl --set-default-version 2
   ```

#### 2. Install Docker Desktop

1. **Download Docker Desktop for Windows**:
   - Visit the [Docker Desktop for Windows download page](https://www.docker.com/products/docker-desktop).
   - Click on **"Download for Windows"**.

2. **Install Docker Desktop**:
   - Run the downloaded installer (`Docker Desktop Installer.exe`).
   - Follow the installation wizard.
   - **Enable WSL 2 Integration** during installation.

3. **Start Docker Desktop**:
   - Launch Docker Desktop from the Start menu.
   - Ensure the Docker icon appears in the system tray.

#### 3. Configure Docker to Use WSL 2

1. **Open Docker Desktop Settings**:
   - Right-click the Docker icon in the system tray.
   - Select **"Settings"**.

2. **Enable WSL Integration**:
   - Go to **"Resources"** > **"WSL Integration"**.
   - Enable integration with your preferred Linux distributions.

#### 4. (Optional) Install Docker Compose Separately

*Note: Docker Compose is included with Docker Desktop. If you need a standalone version, follow these steps.*

1. **Download Docker Compose**:

   ```powershell
   curl -SL https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-windows-x86_64.exe -o docker-compose.exe
   ```

2. **Move to a Directory in PATH**:

   ```powershell
   Move-Item -Path docker-compose.exe -Destination "C:\Program Files\Docker\Docker\resources\bin\docker-compose.exe"
   ```

3. **Verify Installation**:

   ```powershell
   docker-compose --version
   ```

---

### macOS

#### 1. Install Docker Desktop for Mac

1. **Download Docker Desktop for Mac**:
   - Visit the [Docker Desktop for Mac download page](https://www.docker.com/products/docker-desktop).
   - Click on **"Download for Mac"**.

2. **Install Docker Desktop**:
   - Open the downloaded `.dmg` file.
   - Drag the **Docker.app** icon to the **Applications** folder.

3. **Start Docker Desktop**:
   - Launch **Docker** from the **Applications** folder.
   - You may be prompted to enter your password to grant permissions.
   - Wait for Docker to initialize (you'll see a Docker whale icon in the menu bar).

#### 2. Verify Docker Installation

Open **Terminal** and run:

```bash
docker --version
```

**Expected Output:**

```
Docker version XX.XX.X, build XXXXXXX
```

#### 3. Verify Docker Compose Installation

Docker Compose is included with Docker Desktop for Mac.

```bash
docker compose version
```

**Expected Output:**

```
Docker Compose version v2.20.2
```

#### 4. Run a Test Container

```bash
docker run hello-world
```

**Expected Output:**

A message confirming that Docker is working correctly.

---

### Linux

#### 1. Uninstall Old Versions

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

#### 2. Install Docker Engine

**a. Update Package Index:**

```bash
sudo apt-get update
```

**b. Install Prerequisites:**

```bash
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

**c. Add Docker’s Official GPG Key:**

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

**d. Set Up the Repository:**

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**e. Install Docker Engine and Docker Compose Plugin:**

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### 3. Manage Docker as a Non-Root User

**a. Create Docker Group:**

```bash
sudo groupadd docker
```

**b. Add Your User to the Docker Group:**

```bash
sudo usermod -aG docker $USER
```

**c. Apply Changes:**

Log out and log back in, or run:

```bash
newgrp docker
```

---

## Verification

### 1. Check Docker Installation

```bash
docker --version
```

**Expected Output:**

```
Docker version 24.0.5, build 1234567
```

### 2. Check Docker Compose Installation

- **Docker Compose as a Plugin:**

  ```bash
  docker compose version
  ```

- **Standalone Docker Compose:**

  ```bash
  docker-compose --version
  ```

**Expected Output:**

```
Docker Compose version v2.20.2
```

### 3. Run a Test Container

```bash
docker run hello-world
```

**Expected Output:**

A message confirming that Docker is working correctly.

### 4. Test Docker Compose

**a. Create a Test `docker-compose.yml` File:**

```yaml
version: '3.8'

services:
  test:
    image: hello-world
```

**b. Run Docker Compose:**

- **Using Docker Compose Plugin:**

  ```bash
  docker compose up
  ```

- **Using Standalone Docker Compose:**

  ```bash
  docker-compose up
  ```

**c. Expected Output:**

The `hello-world` container runs, displays a success message, and exits.

**d. Clean Up:**

- **Using Docker Compose Plugin:**

  ```bash
  docker compose down
  ```

- **Using Standalone Docker Compose:**

  ```bash
  docker-compose down
  ```

---

## Troubleshooting

### 1. Docker Commands Not Found

- **Cause**: Docker not installed or not in system PATH.
- **Solution**: Reinstall Docker and ensure the installation path is in your system’s PATH variable.

### 2. Permission Denied Errors (Linux)

- **Cause**: User not in `docker` group.
- **Solution**: Add your user to the `docker` group and restart your session.

  ```bash
  sudo usermod -aG docker $USER
  newgrp docker
  ```

### 3. Docker Daemon Not Running

- **Windows/macOS**: Ensure Docker Desktop is running.
  - **Windows**: Check the system tray for the Docker icon.
  - **macOS**: Look for the Docker whale icon in the menu bar. If not visible, launch Docker Desktop from the **Applications** folder.

- **Linux**:

  ```bash
  sudo systemctl status docker
  ```

  **Start Docker Daemon if Not Running:**

  ```bash
  sudo systemctl start docker
  ```

### 4. Outdated Docker or Docker Compose

- **Solution**: Update Docker and Docker Compose to the latest versions.
  - **Windows/macOS**: Use Docker Desktop’s update feature.
  - **Linux**:

    ```bash
    sudo apt-get update
    sudo apt-get upgrade docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

---

## Additional Tips

- **Use `.env` Files**: Store environment variables in `.env` files and reference them in your `docker-compose.yml` for better security and flexibility.
- **Backup Docker Data**: Regularly backup Docker volumes to prevent data loss.
- **Monitor Resources**:
  - **Windows/macOS**:
    - Use Docker Desktop's settings to monitor and adjust CPU, memory, and disk usage.
      - **Windows**: Right-click the Docker icon in the system tray and select **"Settings"**.
      - **macOS**: Click the Docker whale icon in the menu bar and select **"Preferences"**.
- **Leverage Docker Compose Version Control**: Specify a compatible version in your `docker-compose.yml` to ensure compatibility.

---

## Summary

By following this guide, you can:

1. **Install Docker and Docker Compose** on Windows (with WSL 2), **macOS**, and Linux.
2. **Verify** the installations by running test containers and checking versions.
3. **Troubleshoot** common issues to ensure smooth operation.
4. **Maintain** your Docker environment with regular updates and best practices.
5. **Docker concepts** https://docs.docker.com/get-started/
