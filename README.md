# CLACKS

This is a rough-and-ready command line tool to enable access to the Google Maps API for people who sit at the cross section of 1) technically-inclined enough to do stuff like parse google developer documentation and run command line tools and 2) hate their smartphone and wish there were a way to navigate this beautiful city easily without carrying paper maps or the aforementioned phone. If that's you, congrats! You'll need a few things to get started. 

## What You'll Need To Get Started:
1) A virtual environment with the appropriate dependencies installed. This tool uses `uv`, a fantastic dependency manager that's so quick and easy it frankly makes me never want to deal with `pip` ever again. You can check out the uv documentation [here](https://docs.astral.sh/uv/). That said, if you're more comfortable with pip that's fine! I included a requirements.txt file here as well, just for you. How have you been btw? We never talk any more :( 
2) A gmail account with an [app key configured](https://support.google.com/mail/answer/185833?hl=en)
3) An SMTP address corresponding to the phone where you would like your instructions sent. The format is going to be something like `yourphonenumber@some.carrier.domain`. You can google your cell carrier + "SMTP address" to find what should go after the "@". Before the "@" you should probably just know already. 
4) A [Google Maps API key](https://developers.google.com/maps/documentation/javascript/get-api-key). I'm gonna be honest here, this one is a bit of a pain. You'll need to create a project with Google Cloud, then enable the Maps API and generate a key within the project. The good news is the Google docs are great and even though there are too many steps the process is relatively straightforward.  

That's it! You're all ready to leave your smartphone at home and go out into the world secure in the knowledge that you will be able to find out what train to take home when you get lost. There's just one more step you need to take before leaving the house, and that's running the tool. 

## Running The Tool
From the root project directory, run `python main.py`. You can put all the config info you gathered above in a nice `.env` file or just supply them as inputs from the command line. The tool will handle things from there by: 
    1) polling the gmail account you provided to see if you've texted any directions requests, 2) submitting your start and end points to the maps API, and finally 3) texting you a roughly-parsed list of steps to the phone address you provided. 

*NB – The tool does not currently shut itself off, so don't forget to quit the terminal session or hit control-C to exit the tool once you've made it safely back home*

## The Code for America README Questions
**Why did you choose this specific problem to work on?**

I have a personal grudge against my smartphone and I know a lot of other people feel the same way! No one should have to drop $300-$700 on the Light Phone just to get away from being constantly online and reachable to everyone in all ways at all times. With this tool, anyone can get around town mapquest-style (RIP) with just a cheap, simple flip phone.

**Which parts of this project did you choose to polish, and which parts did you intentionally leave unpolished? Why?**

The stuff I really wanted to make sure worked was the simple process for retrieving directions. The Maps API is complex and offers a *ton* of options and parameters, and sorting out the data fetched so that they all make sense is non-trivial. This is the core functionality, so if it isn't useful or doesn't work the whole thing is pointless. 

Conversely, I didn't spend much time (yet) making this thing terribly user-friendly. In a deployed version of an app with the same functionality I can't imagine I would ever ask a user to go set up their own API credentials, that would have to be handled more smoothly. Since getting the core functionality up and running took a fair bit of work even in its current rough state, these types of quality-of-life improvements had to get cut, and the same goes for test coverage (for scope reasons there is not currently any test coverage here).

**How will you (or do you) evaluate whether or not this system is working well?**

I tested it with my personal email and cell phone. It works great! 

**Did you use AI-assisted coding tools (Copilot, ChatGPT, Claude Code, Amp, etc.) to write this? Why or why not, and how did it affect your workflow?**

I did not. This is a project I've been thinking about building for a long time, ever since I started tinkering around with the SMTP and email capabilities within python, and since there weren't any hard deadlines I didn't feel any pressure to offload code writing duties to an LLM-based tool. Whenever time allows I prefer to design and write my own programs, because I feel that deferring that decision-making to the LLM generally means I have a less robust understanding of the code I'm generating, and especially for a tool I'm submitting as part of a potential interview process it seemed like my priority should be in displaying my own work rather than my ability to curate and wrangle auto-generated code. That said, I did refer to a medium post I found on how to efficiently parse information retrieved with python's `email` tools, primarily for time purposes.  

**What would you do differently, or what would you build next given more time?**

I probably would have picked a less complex tool to build for a take-home assessment, which would have enabled me to turn this around quicker and add a bit more shine to it. There's a lot of improvements I'd like to make in future (since I do plan on using this thing myself going forward), including but not limited to:

- Adding test coverage
- Integrating a secure secret management system (e.g. AWS Parameter Store or something local like a SOPS-encrypted secrets file) to obviate the need for users to generate their own Maps API key.
- Adding the ability to send a kill signal to the tool over text
- Adding an auto-shutdown timer
- Expanding the email integration to auto-delete the command message once it's been processed so it doesn't gunk up the user's inbox
- Adding error handling and notifications over text to the user when an error has occurred
- Polishing the directions code
    - Making the parsed directions a bit more legible
    - Allowing the user to disambiguate locations when more than one result seems likely
    - Presenting options for routes (currently the first route suggested for public transit is what gets returned)
    - Retrieving an image of the proposed route for further context