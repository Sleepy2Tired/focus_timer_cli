# Focus Timer CLI
A command-line Pomodoro timer to enhance productivity and track your sessions.

## Features
- Start and stop Pomodoro sessions
- Check current timer status
- Log sessions in CSV format for easy tracking
- Simple and intuitive command-line interface

## Quickstart
To get started with Focus Timer CLI, follow these simple steps:

1. **Install the tool**:
   ```bash
   npm install -g focus-timer-cli
   ```

2. **Run the timer**:
   ```bash
   focus-timer start
   ```

## Usage Examples
- **Start a Pomodoro session**:
  ```bash
  focus-timer start
  ```

- **Stop the current session**:
  ```bash
  focus-timer stop
  ```

- **Check the current status**:
  ```bash
  focus-timer status
  ```

- **View session logs**:
  ```bash
  focus-timer logs
  ```

## Configuration
Focus Timer CLI comes with default settings. You can customize the following parameters:
- **Pomodoro Duration**: Set your desired session length (default: 25 minutes).
- **Break Duration**: Set your break length (default: 5 minutes).
- **CSV Log Path**: Specify where to save session logs.

Edit the configuration file located at `~/.config/focus-timer/config.json` to adjust these settings.

## Roadmap
- [ ] Add notification features for session completion
- [ ] Implement customizable session lengths
- [ ] Introduce a GUI version of the timer
- [ ] Enhance logging with analytics features

## FAQ
**Q: Can I change the timer durations?**  
A: Yes, you can modify the Pomodoro and break durations in the configuration file.

**Q: How do I view my session logs?**  
A: Use the command `focus-timer logs` to access your CSV logs.

**Q: Is this tool cross-platform?**  
A: Yes, Focus Timer CLI works on Windows, macOS, and Linux.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.