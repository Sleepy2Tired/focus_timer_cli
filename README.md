# Focus Timer CLI
A command-line tool to boost your productivity with Pomodoro sessions.

## Features
- Start and stop Pomodoro sessions
- Check current session status
- Log sessions to CSV for easy tracking
- Simple and intuitive command-line interface

## Quickstart
To install Focus Timer CLI, clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/focus-timer-cli.git
cd focus-timer-cli
pip install -r requirements.txt
```

## Usage Examples
Start a new Pomodoro session:

```bash
focus-timer start
```

Stop the current session:

```bash
focus-timer stop
```

Check the status of the current session:

```bash
focus-timer status
```

View your session logs in CSV format:

```bash
focus-timer logs
```

## Configuration
Focus Timer CLI allows you to customize session durations. Edit the configuration file located at `config.json`:

```json
{
  "work_duration": 25,
  "break_duration": 5
}
```

## Roadmap
- [ ] Add notifications for session start and end
- [ ] Implement user-defined session lengths
- [ ] Enhance CSV logging with additional metrics
- [ ] Create a desktop version of the timer

## FAQ
**Q: Can I customize session lengths?**  
A: Yes, you can modify the `config.json` file to set your desired durations.

**Q: How do I view my session logs?**  
A: Use the command `focus-timer logs` to display your session logs in CSV format.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.