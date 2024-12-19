FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
  && sudo apt-get -y install \
  git dnsutils usbutils \
  clang python3-venv \
  udev

## Set up udev rules for PlatformIO
RUN curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/assets/system/99-platformio-udev.rules | tee /etc/udev/rules.d/99-platformio-udev.rules
RUN usermod -a -G dialout vscode \
  && usermod -a -G plugdev vscode

# Install PlatformIO CLI
RUN curl -fsSL -o /tmp/get-platformio.py https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py
RUN python3 /tmp/get-platformio.py \
  && python3 /tmp/get-platformio.py check core --dump-state ~/pioinstaller-state.json

RUN echo 'export PATH="$PATH:$HOME/.platformio/penv/bin"' | tee -a /home/vscode/.bashrc /home/vscode/.zshrc 
RUN echo 'export PATH="$PATH:$HOME/.platformio/penv/bin"' | sudo tee -a /root/.bashrc /root/.zshrc