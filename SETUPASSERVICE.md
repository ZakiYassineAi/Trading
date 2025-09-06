# Setup as a systemd Service (Alternative 24/7 Method)

This guide explains how to run the agent as a persistent background service on a Linux server (like a VPS). This method ensures the agent runs 24/7 and automatically restarts if it crashes or the server reboots.

This is an alternative to the GitHub Actions method and should only be used if you require the agent to be running constantly, rather than on a 10-minute schedule.

---

## 1. Create the systemd Service File

First, you need to create a service definition file. Run the following command to create and edit the file:

```bash
sudo nano /etc/systemd/system/quantum-agent.service
```

Copy and paste the following content into the editor:

```ini
[Unit]
Description=Quantum Airdrop Agent - 24/7 Runner
After=network.target

[Service]
# Replace 'your_username' with your actual username
User=your_username

# Replace '/path/to/your/Trading' with the full, absolute path to the repository
WorkingDirectory=/path/to/your/Trading

# The command to execute. Note we use the absolute path to the script.
ExecStart=/path/to/your/Trading/start.sh

# Restart the service automatically if it fails
Restart=always
RestartSec=15

# Redirect output to the system's journal
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**IMPORTANT:**
- Replace `your_username` with the output of the `whoami` command.
- Replace `/path/to/your/Trading` with the full path to this repository on your server (use the `pwd` command inside the directory to find it).

Save the file and exit by pressing `Ctrl+X`, then `Y`, then `Enter`.

---

## 2. Enable and Start the Service

Now, run these commands one by one to enable and start your new service:

```bash
# Reload the systemd daemon to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start automatically on boot
sudo systemctl enable quantum-agent.service

# Start the service immediately
sudo systemctl start quantum-agent.service
```

Your agent is now running as a background service!

---

## 3. Managing the Service

Here are the essential commands to manage your service:

- **Check the status:** (See if it's running, view recent logs)
  ```bash
  sudo systemctl status quantum-agent.service
  ```

- **View live logs:**
  ```bash
  journalctl -u quantum-agent.service -f
  ```
  (Press `Ctrl+C` to stop viewing logs).

- **Stop the service:**
  ```bash
  sudo systemctl stop quantum-agent.service
  ```

- **Restart the service:**
  ```bash
  sudo systemctl restart quantum-agent.service
  ```

---

## 4. Troubleshooting Common Errors

- **Error: "Permission denied" when creating the service file.**
  - **Problem:** You forgot to use `sudo` when creating the file in `/etc/systemd/system/`.
  - **Solution:** Re-run the `nano` command with `sudo` at the beginning.

- **Error: Service fails to start, status shows an error related to `start.sh`.**
  - **Problem:** The `start.sh` script does not have execute permissions.
  - **Solution:** Grant execute permissions to the script with this command from inside your repository directory:
    ```bash
    chmod +x start.sh
    ```
  - Then, restart the service: `sudo systemctl restart quantum-agent.service`.

- **Error: Service complains it cannot find `start.sh` or `requirements.txt`.**
  - **Problem:** The `WorkingDirectory` in your `.service` file is incorrect.
  - **Solution:** Double-check the path you provided for `WorkingDirectory` and `ExecStart`. It must be the full, absolute path. Use `pwd` to be sure.
