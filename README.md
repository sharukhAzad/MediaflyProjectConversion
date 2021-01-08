# *** Mediafly QA Hiring Project ***

### Overview

The application is a distributed application that consists of 4 components that
communicate via REST apis. It serves the purposes of an asynchronous image
processing system. The user uploads an image to the system, which triggers a
job to run asynchronously on the backend. Once the job is completed the user
can view both the original image as well as the processed image. The UI is
capable of informing the user about the status of the processing job (i.e.
pending, completed, or failed).

### Setup

Dependencies that are recommended in order to work with most types of images:

- libjpeg
- libtiff
- libfreetype
- littlecms
- libwebp

If on Mac OS X, use homebrew to install some of these dependencies:

- brew install libtiff libjpeg webp little-cms2

and then 
	
	pip install Pillow

- Now, run the application with the steps outlined in the following section

If on Windows, follow these instructions:

1. Install Python 2.7.
	
	** SELECT: Add python.exe to Path **
	
	64-bit version: 
	<https://www.python.org/ftp/python/2.7.8/python-2.7.8.amd64.msi>
	
	32-bit version: 
	<https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi>
	
2. Install Pip, 
	follow instructions here: <https://pip.pypa.io/en/latest/installing.html>
	
3. Reboot
4. Open command prompt
5. Run this command:

		python -m pip install flask requests
		
6. Install PIL:

	64-bit version: <https://github.com/lightkeeper/lswindows-lib/blob/master/amd64/python/PIL-1.1.7.win-amd64-py2.7.exe?raw=true>
	
	32-bit version: <http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe>

7. Run the application, following the steps outlined in the next section.

For further instructions and information, or if on another type of machine, visit
<http://pillow.readthedocs.org/en/latest/installation.html>

If you are missing any dependent python packages, you can install them by
running:

pip install -r requirements.txt

### Running

To run, run these commands in separate terminal or cmd.exe tabs or windows in this
order, and make sure nothing is running on ports 8080 and 9090:

1. python application.py
2. python queue.py
3. python worker.py

To terminate, type CTRL+C in the terminal/cmd.exe tab or window (worker.py will terminate after stopping queue.py).

If the application does not terminate cleanly, or something else is running on either port 8080 or 9090, you may need to manually kill the processes. To do this, run the command:

	lsof -i:PORT_NUM -n -P

to find the PID for the process(es) that needs to be killed.

Then run the command

	kill <PID>

### Usage

Suggested usage --> use a browser.

###### Browser usage
Open up a browser window to 127.0.0.1:8080

###### Command line usage

To add an image to the API service:

	curl -X PUT 127.0.0.1:8080/images/<imagename>

To receive information regarding a certain image:

	curl 127.0.0.1:8080/images/<imagename>

To receive information on all images:

	curl 127.0.0.1:8080/images

To push an item to the queue:

	curl -X POST 127.0.0.1:9090/queues/<queuename>/push -	H 'Content-type:
	application/json' -d '{"id": "IMAGENAME"}'

To pop the first item from the queue:

	curl -X POST 127.0.0.1:9090/queues/<queuename>/pop

### Outstanding bug(s):

- Images added via command line must be in same working directory as application, although not a necessity for uploading an image via a browser
