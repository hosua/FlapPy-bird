#!/usr/bin/bash

unset FIRST_RUN
PATH_TO_VENV="flappy-venv"

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
	echo "Note: In order for the virtual environment to work, you need source this script."
	echo
	echo "In other words, either run this script with:"
	echo ". init-venv.sh"
	echo
	echo "or with the command:"
	echo "source init-venv.sh"
	echo
	echo "You should not be running it with ./init-venv.sh"

	exit 1
fi


if [ ! -d "$PATH_TO_VENV" ] ; then 
	echo "Creating a new venv named: $PATH_TO_VENV"
	python3 -m venv "$PATH_TO_VENV"
	FIRST_RUN=1
fi

source "$PATH_TO_VENV/bin/activate"
echo "Started the virtual environment"

if [ ! -z "$FIRST_RUN" ]; then
	echo "Installing the necessary packages to the venv..."
	echo
	"$PATH_TO_VENV"/bin/pip3 install --upgrade pip
	"$PATH_TO_VENV"/bin/pip3 install -r requirements.txt
	if [ $? -ne 0 ]; then
		echo
		echo "Warning: Failed to install some packages. You may need to install system dependencies."
		echo "For pygame, you may need to install SDL2 development libraries:"
		echo "  sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev"
		echo
		echo "Alternatively, try installing pygame from a pre-built wheel:"
		echo "  \"$PATH_TO_VENV\"/bin/pip3 install --only-binary :all: pygame==2.5.2"
		echo
	fi
fi

echo
echo "To leave the venv without closing your shell, use the deactivate command"
echo


