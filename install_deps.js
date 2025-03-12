const { exec } = require('child_process');
const path = require('path');

// Function to install Python packages
function installPythonPackages() {
  const requirements = path.join(__dirname, 'requirements.txt');
  
  // Use python3 -m pip to ensure we're using the correct pip
  const command = `python3 -m pip install -r ${requirements}`;
  
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error installing packages: ${error}`);
      return;
    }
    if (stderr) {
      console.error(`Warnings during installation: ${stderr}`);
    }
    console.log(`Package installation complete: ${stdout}`);
  });
}

installPythonPackages();