
# Reddit Video Maker Bot 🎥


# My Fork of the below.
This fork is not going to be merged with the original. 
Original readme is kept for credits to original author.


* improvements
* removed playright and just text box
* added edgetts engine for voice
  released in v1
* v2 work is coming along refer to [TODO](TODO.md)
    * use subtitle as main video track, instead of textbox(this option is still available)
    * title credits creation with text box and emoji support in title
    * Different voices in edgetts and gender identification of post creator to change voice gender. 

More coming, listed in [TODO](TODO.md)

To see progress in dev and actual videos visit https://www.facebook.com/people/A-Few-Stories-from-r/100069823481590/

All done WITHOUT video editing or asset compiling. Just pure ✨programming magic✨.

Created by Lewis Menelaws & [TMRRW](https://tmrrwinc.ca)

<a target="_blank" href="https://tmrrwinc.ca">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/6053155/170528535-e274dc0b-7972-4b27-af22-637f8c370133.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/6053155/170528582-cb6671e7-5a2f-4bd4-a048-0e6cfa54f0f7.png">
  <img src="https://user-images.githubusercontent.com/6053155/170528582-cb6671e7-5a2f-4bd4-a048-0e6cfa54f0f7.png" width="350">
</picture>

## Video Explainer

[![lewisthumbnail](https://user-images.githubusercontent.com/6053155/173631669-1d1b14ad-c478-4010-b57d-d79592a789f2.png)
](https://www.youtube.com/watch?v=3gjcY_00U1w)

## Motivation 🤔

These videos on TikTok, YouTube and Instagram get MILLIONS of views across all platforms and require very little effort.
The only original thing being done is the editing and gathering of all materials...

... but what if we can automate that process? 🤔

## Disclaimers 🚨

- **At the moment**, this repository won't attempt to upload this content through this bot. It will give you a file that
  you will then have to upload manually. This is for the sake of avoiding any sort of community guideline issues.

## Requirements

- Python 3.10
- Playwright (this should install automatically in installation)

## Installation 👩‍💻

1. Clone this repository
2. Run `pip install -r requirements.txt`
3. Run `python -m playwright install` and `python -m playwright install-deps`
4. For mac open fonts and copy Apple Color Emoji.ttc into fonts, other platform can download Apple Color Emoji.ttc from 
https://drive.usercontent.google.com/download?id=1aGzSjSPUlYtCpH-Yn6ggWCWXNfIKdu6Z&export=download&authuser=0 and rename it to Apple Color Emoji.ttc and move under fonts folder

**EXPERIMENTAL!!!!**

On macOS and Linux (debian, arch, fedora and centos, and based on those), you can run an install script that will automatically install steps 1 to 3. (requires bash)

`bash <(curl -sL https://raw.githubusercontent.com/sayok88/RedditVideoMakerBot/master/install.sh)`

This can also be used to update the installation

4. Run `python main.py`
5. Visit [the Reddit Apps page.](https://www.reddit.com/prefs/apps), and set up an app that is a "script". Paste any URL in redirect URL. Ex:google.com
6. The bot will ask you to fill in your details to connect to the Reddit API, and configure the bot to your liking
7. Enjoy 😎
8. If you need to reconfigure the bot, simply open the `config.toml` file and delete the lines that need to be changed. On the next run of the bot, it will help you reconfigure those options.

(Note if you got an error installing or running the bot try first rerunning the command with a three after the name e.g. python3 or pip3)

If you want to read more detailed guide about the bot, please refer to the [documentation](https://reddit-video-maker-bot.netlify.app/)

## Video



https://github.com/sayok88/RedditVideoMakerBot/assets/25224679/3d78c325-3560-4bf2-b0d6-5d1f58c18eff



## Contributing & Ways to improve 📈

In its current state, this bot does exactly what it needs to do. However, improvements can always be made!

I have tried to simplify the code so anyone can read it and start contributing at any skill level. Don't be shy :) contribute!

- [ ]  Creating better documentation and adding a command line interface.
- [X]  Allowing the user to choose background music for their videos.
- [X]  Allowing users to choose a reddit thread instead of being randomized.
- [X]  Allowing users to choose a background that is picked instead of the Minecraft one.
- [X]  Allowing users to choose between any subreddit.
- [X]  Allowing users to change voice.
- [X]  Checks if a video has already been created
- [X]  Light and Dark modes
- [X]  NSFW post filter

Please read our [contributing guidelines](CONTRIBUTING.md) for more detailed information.

### For any questions or support join the [Discord](https://discord.gg/WBQT52RrHV) server

## Developers and maintainers. (From Original Repo, dont bug them for this one)

Elebumm (Lewis#6305) - https://github.com/elebumm (Founder)

Jason (personality.json) - https://github.com/JasonLovesDoggo (Maintainer)

Simon (OpenSourceSimon) - https://github.com/OpenSourceSimon

CallumIO (c.#6837) - https://github.com/CallumIO

Verq (Verq#2338) - https://github.com/CordlessCoder

LukaHietala (Pix.#0001) - https://github.com/LukaHietala

Freebiell (Freebie#3263) - https://github.com/FreebieII

Aman Raza (electro199#8130) - https://github.com/electro199

## LICENSE

[Roboto Fonts](https://fonts.google.com/specimen/Roboto/about) are licensed under [Apache License V2](https://www.apache.org/licenses/LICENSE-2.0)
