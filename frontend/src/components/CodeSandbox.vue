<template>
  <div class="code-sandbox">
    <div class="sandbox-header">
      <h1 class="sandbox-title">
        <span class="sandbox-icon">⚡</span>
        Code Sandbox
      </h1>
      <div class="sandbox-controls">
        <button
          @click="runCode"
          class="run-button"
          :disabled="!canRun || isExecuting"
        >
          <span class="button-icon">{{ isExecuting ? "⏳" : "▶" }}</span>
          {{ isExecuting ? "Running..." : "Run Code" }}
        </button>
        <button @click="clearOutput" class="clear-button">
          <span class="button-icon">🗑</span>
          Clear
        </button>
      </div>
    </div>

    <div class="sandbox-content">
      <div class="editor-panel">
        <div class="file-tabs">
          <button
            v-for="file in files"
            :key="file.id"
            @click="setActiveFile(file.id)"
            :class="['file-tab', { active: activeFileId === file.id }]"
          >
            <span class="file-icon">{{ getFileIcon(file.type) }}</span>
            {{ file.name }}
            <span
              v-if="files.length > 1"
              @click.stop="removeFile(file.id)"
              class="close-tab"
              >×</span
            >
          </button>
          <button @click="addNewFile" class="add-file-button">
            <span class="button-icon">+</span>
          </button>
        </div>

        <div class="editor-container">
          <div class="editor-toolbar">
            <select
              v-model="activeFile.type"
              @change="updateFileType"
              class="language-selector"
            >
              <option value="html">HTML</option>
              <option value="css">CSS</option>
              <option value="javascript">JavaScript</option>
            </select>
            <div class="editor-info">
              <span class="line-count">Lines: {{ getLineCount() }}</span>
              <span class="char-count"
                >Characters: {{ activeFile.content.length }}</span
              >
            </div>
          </div>

          <div class="code-editor-wrapper">
            <div class="line-numbers">
              <div
                v-for="line in getLineCount()"
                :key="line"
                class="line-number"
              >
                {{ line }}
              </div>
            </div>
            <textarea
              v-model="activeFile.content"
              @input="updateContent"
              @keydown="handleKeydown"
              ref="codeEditor"
              class="code-editor"
              :placeholder="getPlaceholder()"
              spellcheck="false"
            ></textarea>
          </div>
        </div>
      </div>

      <div class="output-panel">
        <div class="output-header">
          <h3>Output</h3>
          <div class="output-controls">
            <button
              @click="toggleConsole"
              :class="['console-toggle', { active: showConsole }]"
            >
              Console
            </button>
          </div>
        </div>

        <div class="output-content">
          <iframe
            v-if="!showConsole"
            ref="outputFrame"
            class="output-frame"
            sandbox="allow-scripts allow-modals"
          ></iframe>

          <div v-else class="console-output">
            <div class="console-header">JavaScript Console</div>
            <div class="console-messages">
              <div
                v-for="(message, index) in consoleMessages"
                :key="index"
                :class="['console-message', message.type]"
              >
                <span class="message-type"
                  >[{{ message.type.toUpperCase() }}]</span
                >
                <span class="message-content">{{ message.content }}</span>
                <span class="message-time">{{ message.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CodeSandbox",
  data() {
    return {
      files: [
        {
          id: 1,
          name: "index.html",
          type: "html",
          content: this.getWelcomeHTML(),
        },
      ],
      activeFileId: 1,
      nextFileId: 2,
      showConsole: false,
      consoleMessages: [],
      isExecuting: false,
    };
  },
  computed: {
    activeFile() {
      return (
        this.files.find((file) => file.id === this.activeFileId) ||
        this.files[0]
      );
    },
    canRun() {
      return this.activeFile && this.activeFile.content.trim().length > 0;
    },
  },
  methods: {
    getWelcomeHTML() {
      return [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "    <title>Code Sandbox</title>",
        "    <style>",
        "        body {",
        "            font-family: Arial, sans-serif;",
        "            margin: 20px;",
        "            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);",
        "            color: white;",
        "        }",
        "        .container {",
        "            max-width: 800px;",
        "            margin: 0 auto;",
        "            text-align: center;",
        "        }",
        "        .welcome-box {",
        "            background: rgba(255, 255, 255, 0.1);",
        "            padding: 30px;",
        "            border-radius: 15px;",
        "            backdrop-filter: blur(10px);",
        "            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);",
        "        }",
        "    </style>",
        "</head>",
        "<body>",
        '    <div class="container">',
        '        <div class="welcome-box">',
        "            <h1>🚀 Welcome to Code Sandbox!</h1>",
        "            <p>Start coding and see your results instantly!</p>",
        '            <button onclick="showMessage()">Click me!</button>',
        "        </div>",
        "    </div>",
        "",
        "    <script>",
        "        function showMessage() {",
        "            alert('Hello from Code Sandbox! 🎉');",
        "            console.log('Button was clicked!');",
        "        }",
        "    <" + "/script>",
        "</body>",
        "</html>",
      ].join("\n");
    },
    setActiveFile(fileId) {
      this.activeFileId = fileId;
    },
    addNewFile() {
      const fileName = prompt("Enter file name (e.g., script.js, style.css):");
      if (!fileName) return;

      const extension = fileName.split(".").pop().toLowerCase();
      let type = "javascript";
      if (extension === "html" || extension === "htm") type = "html";
      else if (extension === "css") type = "css";

      const newFile = {
        id: this.nextFileId++,
        name: fileName,
        type: type,
        content: this.getDefaultContent(type),
      };

      this.files.push(newFile);
      this.activeFileId = newFile.id;
    },
    removeFile(fileId) {
      if (this.files.length <= 1) return;

      const index = this.files.findIndex((file) => file.id === fileId);
      if (index !== -1) {
        this.files.splice(index, 1);
        if (this.activeFileId === fileId) {
          this.activeFileId = this.files[0].id;
        }
      }
    },
    updateFileType() {
      const file = this.activeFile;
      const extensions = { html: "html", css: "css", javascript: "js" };
      const newExt = extensions[file.type];
      const nameParts = file.name.split(".");
      if (nameParts.length > 1) {
        nameParts[nameParts.length - 1] = newExt;
        file.name = nameParts.join(".");
      } else {
        file.name += "." + newExt;
      }
    },
    getDefaultContent(type) {
      const templates = {
        html: [
          "<!DOCTYPE html>",
          '<html lang="en">',
          "<head>",
          '    <meta charset="UTF-8">',
          '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
          "    <title>New Document</title>",
          "</head>",
          "<body>",
          "    <h1>Hello World!</h1>",
          "</body>",
          "</html>",
        ].join("\n"),
        css: [
          "/* CSS Styles */",
          "body {",
          "    font-family: Arial, sans-serif;",
          "    margin: 0;",
          "    padding: 20px;",
          "}",
          "",
          ".container {",
          "    max-width: 800px;",
          "    margin: 0 auto;",
          "}",
        ].join("\n"),
        javascript: [
          "// JavaScript Code Examples",
          "console.log('Hello from JavaScript!');",
          "",
          "// Function example",
          "function greet(name) {",
          "    return `Hello, ${name}!`;",
          "}",
          "",
          "// Array and object examples",
          "const numbers = [1, 2, 3, 4, 5];",
          "const doubled = numbers.map(n => n * 2);",
          "",
          "console.log('Original:', numbers);",
          "console.log('Doubled:', doubled);",
          "console.log(greet('Code Sandbox'));",
          "",
          "// Try running this code!",
        ].join("\n"),
      };
      return templates[type] || "";
    },
    getFileIcon(type) {
      const icons = {
        html: "🌐",
        css: "🎨",
        javascript: "⚡",
      };
      return icons[type] || "📄";
    },
    getPlaceholder() {
      const placeholders = {
        html: "Write your HTML code here...",
        css: "Write your CSS styles here...",
        javascript: "Write your JavaScript code here...",
      };
      return placeholders[this.activeFile.type] || "Start coding...";
    },
    getLineCount() {
      return this.activeFile.content.split("\n").length;
    },
    updateContent() {
      // Auto-save functionality could be added here
    },
    handleKeydown(event) {
      if (event.key === "Tab") {
        event.preventDefault();
        const textarea = event.target;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;

        this.activeFile.content =
          this.activeFile.content.substring(0, start) +
          "    " +
          this.activeFile.content.substring(end);

        this.$nextTick(() => {
          textarea.selectionStart = textarea.selectionEnd = start + 4;
        });
      }
    },
    runCode() {
      if (this.isExecuting) return;

      try {
        if (!this.activeFile || !this.activeFile.content.trim()) {
          this.addConsoleMessage("warn", "No code to run");
          return;
        }

        this.isExecuting = true;

        if (this.activeFile.type === "html") {
          this.runHTMLCode();
        } else if (this.activeFile.type === "javascript") {
          this.runJavaScriptCode();
        } else if (this.activeFile.type === "css") {
          this.showCSSPreview();
        } else {
          this.addConsoleMessage(
            "error",
            `Unsupported file type: ${this.activeFile.type}`
          );
        }

        // Reset loading state after a short delay
        setTimeout(() => {
          this.isExecuting = false;
        }, 500);
      } catch (error) {
        console.error("Error in runCode:", error);
        this.addConsoleMessage("error", `Error running code: ${error.message}`);
        this.isExecuting = false;
      }
    },
    runHTMLCode() {
      // First ensure we're not in console mode
      this.showConsole = false;

      // Use nextTick to ensure the iframe is rendered
      this.$nextTick(() => {
        try {
          const iframe = this.$refs.outputFrame;

          if (!iframe) {
            console.error("Output iframe not found");
            this.addConsoleMessage("error", "Output iframe not available");
            return;
          }

          // Wait a bit for iframe to be ready
          setTimeout(() => {
            try {
              const doc =
                iframe.contentDocument || iframe.contentWindow?.document;

              if (!doc) {
                console.error("Cannot access iframe document");
                this.addConsoleMessage(
                  "error",
                  "Cannot access iframe document"
                );
                return;
              }

              // Clear and write new content
              doc.open();
              doc.write(this.activeFile.content);
              doc.close();
            } catch (docError) {
              console.error("Error writing to iframe:", docError);
              this.addConsoleMessage(
                "error",
                `Error executing HTML: ${docError.message}`
              );
            }
          }, 100);
        } catch (error) {
          console.error("Error in runHTMLCode:", error);
          this.addConsoleMessage(
            "error",
            `Error running HTML code: ${error.message}`
          );
        }
      });
    },
    runJavaScriptCode() {
      this.consoleMessages = [];
      this.showConsole = true;

      const originalLog = console.log;
      const originalError = console.error;
      const originalWarn = console.warn;

      console.log = (...args) => {
        this.addConsoleMessage("log", args.join(" "));
        originalLog.apply(console, args);
      };

      console.error = (...args) => {
        this.addConsoleMessage("error", args.join(" "));
        originalError.apply(console, args);
      };

      console.warn = (...args) => {
        this.addConsoleMessage("warn", args.join(" "));
        originalWarn.apply(console, args);
      };

      try {
        // eslint-disable-next-line no-eval
        eval(this.activeFile.content);
      } catch (error) {
        this.addConsoleMessage("error", error.message);
      }

      console.log = originalLog;
      console.error = originalError;
      console.warn = originalWarn;
    },
    showCSSPreview() {
      this.showConsole = false;

      this.$nextTick(() => {
        try {
          const cssContent = this.activeFile.content;
          const htmlContent = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            "    <title>CSS Preview</title>",
            "    <style>" + cssContent + "</style>",
            "</head>",
            "<body>",
            "    <h1>CSS Preview</h1>",
            "    <p>This is a preview of your CSS styles.</p>",
            '    <div class="example">Example content with custom styles</div>',
            "    <button>Button Element</button>",
            '    <div class="container">',
            "        <h2>Sample Content</h2>",
            '        <p class="text">Apply your CSS styles to see changes!</p>',
            "    </div>",
            "</body>",
            "</html>",
          ].join("\n");

          setTimeout(() => {
            try {
              const iframe = this.$refs.outputFrame;

              if (!iframe) {
                this.addConsoleMessage("error", "Output iframe not found");
                return;
              }

              const doc =
                iframe.contentDocument || iframe.contentWindow?.document;

              if (!doc) {
                this.addConsoleMessage(
                  "error",
                  "Cannot access iframe document"
                );
                return;
              }

              doc.open();
              doc.write(htmlContent);
              doc.close();
            } catch (docError) {
              console.error("Error writing CSS preview:", docError);
              this.addConsoleMessage(
                "error",
                `Error displaying CSS preview: ${docError.message}`
              );
            }
          }, 100);
        } catch (error) {
          console.error("Error in showCSSPreview:", error);
          this.addConsoleMessage(
            "error",
            `Error creating CSS preview: ${error.message}`
          );
        }
      });
    },
    addConsoleMessage(type, content) {
      try {
        if (!this.consoleMessages) {
          this.consoleMessages = [];
        }

        this.consoleMessages.push({
          type: type || "log",
          content: String(content || ""),
          time: new Date().toLocaleTimeString(),
        });

        // Ensure console is visible for error messages
        if (type === "error" || type === "warn") {
          this.showConsole = true;
        }
      } catch (error) {
        console.error("Error adding console message:", error);
      }
    },
    toggleConsole() {
      this.showConsole = !this.showConsole;
    },
    clearOutput() {
      try {
        if (this.showConsole) {
          this.consoleMessages = [];
          this.addConsoleMessage("info", "Console cleared");
        } else {
          this.$nextTick(() => {
            try {
              const iframe = this.$refs.outputFrame;
              if (iframe) {
                const doc =
                  iframe.contentDocument || iframe.contentWindow?.document;
                if (doc) {
                  doc.open();
                  doc.write(
                    [
                      "<html>",
                      "<head><title>Output Cleared</title></head>",
                      '<body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; color: #666;">',
                      "<h2>Output Cleared</h2>",
                      "<p>Run your code to see the output here.</p>",
                      "</body>",
                      "</html>",
                    ].join("\n")
                  );
                  doc.close();
                }
              }
            } catch (error) {
              console.error("Error clearing output:", error);
            }
          });
        }
      } catch (error) {
        console.error("Error in clearOutput:", error);
      }
    },
  },
};
</script>

<style scoped>
.code-sandbox {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: "Monaco", "Menlo", "Ubuntu Mono", monospace;
  background: #1e1e1e;
  color: #ffffff;
}

.sandbox-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #2d2d30;
  border-bottom: 1px solid #3c3c3c;
}

.sandbox-title {
  margin: 0;
  font-size: 1.5rem;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 10px;
}

.sandbox-icon {
  font-size: 1.8rem;
}

.sandbox-controls {
  display: flex;
  gap: 10px;
}

.run-button,
.clear-button {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s;
}

.run-button {
  background: #4caf50;
  color: white;
}

.run-button:hover:not(:disabled) {
  background: #45a049;
}

.run-button:disabled {
  background: #666;
  cursor: not-allowed;
}

.clear-button {
  background: #f44336;
  color: white;
}

.clear-button:hover {
  background: #da190b;
}

.button-icon {
  font-size: 0.9rem;
}

.sandbox-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.editor-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #3c3c3c;
}

.file-tabs {
  display: flex;
  background: #2d2d30;
  border-bottom: 1px solid #3c3c3c;
  overflow-x: auto;
}

.file-tab {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 10px 15px;
  border: none;
  background: transparent;
  color: #cccccc;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  white-space: nowrap;
}

.file-tab:hover {
  background: #3c3c3c;
}

.file-tab.active {
  background: #1e1e1e;
  color: #ffffff;
  border-bottom-color: #007acc;
}

.file-icon {
  font-size: 0.9rem;
}

.close-tab {
  margin-left: 5px;
  padding: 2px 5px;
  border-radius: 3px;
  transition: background 0.2s;
}

.close-tab:hover {
  background: #ff4444;
}

.add-file-button {
  padding: 10px 15px;
  border: none;
  background: transparent;
  color: #cccccc;
  cursor: pointer;
  transition: all 0.2s;
}

.add-file-button:hover {
  background: #3c3c3c;
  color: #ffffff;
}

.editor-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: #2d2d30;
  border-bottom: 1px solid #3c3c3c;
}

.language-selector {
  background: #3c3c3c;
  color: #ffffff;
  border: 1px solid #555;
  padding: 5px 10px;
  border-radius: 3px;
}

.editor-info {
  display: flex;
  gap: 15px;
  font-size: 0.8rem;
  color: #cccccc;
}

.code-editor-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.line-numbers {
  position: absolute;
  left: 0;
  top: 0;
  width: 50px;
  height: 100%;
  background: #2d2d30;
  border-right: 1px solid #3c3c3c;
  padding: 15px 5px;
  font-size: 0.9rem;
  color: #858585;
  overflow: hidden;
  z-index: 2;
}

.line-number {
  text-align: right;
  line-height: 1.5;
  padding-right: 10px;
}

.code-editor {
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
  background: transparent;
  color: #ffffff;
  font-family: "Monaco", "Menlo", "Ubuntu Mono", monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 15px 15px 15px 65px;
  resize: none;
  z-index: 3;
  position: relative;
}

.output-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #ffffff;
}

.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.output-header h3 {
  margin: 0;
  color: #333;
}

.output-controls {
  display: flex;
  gap: 10px;
}

.console-toggle {
  padding: 6px 12px;
  border: 1px solid #007acc;
  background: transparent;
  color: #007acc;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s;
}

.console-toggle:hover,
.console-toggle.active {
  background: #007acc;
  color: white;
}

.output-content {
  flex: 1;
  position: relative;
}

.output-frame {
  width: 100%;
  height: 100%;
  border: none;
  background: white;
}

.console-output {
  height: 100%;
  background: #1e1e1e;
  color: #ffffff;
  display: flex;
  flex-direction: column;
}

.console-header {
  padding: 10px 15px;
  background: #2d2d30;
  border-bottom: 1px solid #3c3c3c;
  font-weight: bold;
}

.console-messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}

.console-message {
  display: flex;
  gap: 10px;
  padding: 5px 0;
  border-bottom: 1px solid #3c3c3c;
  font-family: "Monaco", "Menlo", "Ubuntu Mono", monospace;
  font-size: 0.9rem;
}

.console-message.error {
  color: #ff6b6b;
}

.console-message.warn {
  color: #ffd93d;
}

.console-message.log {
  color: #ffffff;
}

.message-type {
  font-weight: bold;
  min-width: 60px;
}

.message-content {
  flex: 1;
}

.message-time {
  font-size: 0.8rem;
  color: #858585;
  min-width: 80px;
  text-align: right;
}

/* Responsive design */
@media (max-width: 768px) {
  .sandbox-content {
    flex-direction: column;
  }

  .editor-panel {
    height: 60vh;
    border-right: none;
    border-bottom: 1px solid #3c3c3c;
  }

  .output-panel {
    height: 40vh;
  }

  .sandbox-header {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }

  .sandbox-controls {
    justify-content: center;
  }
}
</style>
