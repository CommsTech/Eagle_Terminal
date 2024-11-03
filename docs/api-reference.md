# Eagle Terminal API Reference

## Chief Class

The `Chief` class is the core of Eagle Terminal's AI capabilities.

### Methods

#### `analyze_command_output(command: str, output: str) -> str`

Analyzes the output of a command and provides insights.

#### `suggest_next_command(command_history: List[str], device_info: Dict[str, Any]) -> str`

Suggests the next command based on command history and device information.

#### `quick_prompt(prompt: str) -> str`

Generates a quick response to a user's prompt.

#### `analyze_and_learn(prompt: str, response: str) -> str`

Analyzes the response from agents and learns from it.

#### `generate_follow_up(original_prompt: str, response: str) -> str`

Generates a follow-up question or command based on the previous interaction.

#### `start_loading_models()`

Starts loading all AI models in a separate thread.

#### `ensure_models_loaded()`

Ensures all models are loaded before proceeding with AI operations.

## CommandSuggester Class

The `CommandSuggester` class handles command suggestions for various operating systems and devices.

### Methods

#### `suggest_command(context: str, os_type: str, device_type: str) -> str`

Suggests a command based on the given context, OS type, and device type.

#### `get_command_explanation(command: str, os_type: str, device_type: str) -> str`

Provides an explanation for a given command.

#### `get_command_syntax(command: str, os_type: str, device_type: str) -> str`

Returns the syntax for a given command.

#### `suggest_multiple_commands(context: str, os_type: str, device_type: str, num_suggestions: int = 3) -> List[str]`

Suggests multiple commands based on the given context, OS type, and device type.

## ModelManager Class

The `ModelManager` class handles loading, saving, and updating of the AI model.

### Methods

#### `load_model()`

Loads the AI model.

#### `update_model(conversation_history)`

Updates the AI model with new conversation data.

#### `prune_model(amount: float = 0.3) -> None`

Prunes the model to reduce its size.

## KnowledgeManager Class

The `KnowledgeManager` class manages and retrieves relevant knowledge for AI-powered responses and learning.

### Methods

#### `get_relevant_knowledge(query: str) -> str`

Retrieves relevant knowledge based on the given query.

#### `learn(category: str, information: str) -> None`

Adds new information to the knowledge base.

## ResponseGenerator Class

The `ResponseGenerator` class generates AI responses based on input prompts and model predictions.

### Methods

#### `generate_response(prompt: str, ...) -> str`

Generates a response based on the given prompt and parameters.

#### `generate_multiple_responses(prompt: str, num_responses: int = 3, **kwargs) -> List[str]`

Generates multiple responses for the given prompt.

## ErrorHandler Class

The `ErrorHandler` class manages error handling and display in the main window of Eagle Terminal.

### Methods

#### `show_error(parent, title: str, message: str)`

Displays an error message box.

#### `show_warning(parent, title: str, message: str)`

Displays a warning message box.

#### `show_info(parent, title: str, message: str)`

Displays an information message box.

#### `log_error(title: str, message: str)`

Logs an error message without displaying a message box.

#### `log_warning(title: str, message: str)`

Logs a warning message without displaying a message box.

#### `log_info(title: str, message: str)`

Logs an information message without displaying a message box.

## SettingsActions Class

The `SettingsActions` class handles all settings-related actions in the main window of Eagle Terminal.

### Methods

#### `load_settings()`

Loads settings from the settings file.

#### `save_settings()`

Saves current settings to the settings file.

#### `open_settings_dialog()`

Opens the main settings dialog.

#### `change_theme()`

Changes the application theme.

#### `configure_ai()`

Configures AI settings.

#### `configure_plugins()`

Configures plugin settings.

#### `export_settings()`

Exports current settings to a file.

#### `import_settings()`

Imports settings from a file.

#### `reset_settings()`

Resets all settings to default values.

#### `session_options()`

Opens the session options dialog.

#### `chief_settings()`

Opens the Chief AI settings dialog.

... (other classes and methods)