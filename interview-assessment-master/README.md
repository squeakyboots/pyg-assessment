# Setup Instructions
Build and start the docker container, via Windows:
1. Open Developer Powershell for VS from Visual Studio or the start menu (Visual Studio must be installed)
2. Navigate to the solution directory and run `nmake init`

Running `make init` from the solution directory should work for Unix-based systems but hasn't been tested.

Once the docker container is running open the CLI for "interview-assessment" and run `python app.py` from the `/app` 
directory (which is the default directory you'll enter when launching the docker CLI with most methods).
- Note: If you initially get a DB connection error verify the DB has loaded up completely before trying again (sometimes it can
take a few minutes).

The application will run at the interval set in `app.py` (default once an hour). It will check the top three coins by market cap and
purchase a coin if its price is below the 10-day average.

Purchases and portfolio details will be logged to `/app/storage/logs/app.log` and output to the console.

[5m34s video overview](https://drive.google.com/file/d/1lgHkBNaz2__Q-BPsPHr9gpaMJs3s-2UL/view?usp=drivesdk). You may need to download the video or manually set the video quality in the embedded player if the quality 
of the stream is poor.
