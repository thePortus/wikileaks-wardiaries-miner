# wikileaks-wardiaries-miner
A Python script to extract data from a local mirror of the WikiLeaks War Diaries daya

In  the summer of 2010, an unknown source within the Defense Department provided WikiLeaks with a highly classified database containing over 492,000 files somewhat misleadingly called the ‘War Diaries.’ Each record in the files pertains to a single ‘kinetic event,’ jargon meaning any time a situation involves potential lethality or physical harm. All together, the database appears to contain every single event from both Iraq and Afghanistan, as known to U.S. Central Command, from 2004–2009.

Each event contains full metadata with date, time, location, and more. This allows us to see the reports coming into U.S. command as they happened. Of course, while extremely detailed we should be as careful with this as any source. Fog of war, concern for the narrative of events (better known as CYA) all effect how records are produced and submitted. Subsequent investigation has in fact shown that some events recorded appear counterfactual events as journalists as uncovered them. Above all, what this allows us to reconstruct is the picture as it appeared to U.S. decision makers.

To get a copy of the site, I used the wGet tool to download a local mirror. Check out [ProgrammingHistorian’s wGet tutorial](https://programminghistorian.org/en/lessons/automated-downloading-with-wget#:~:text=to%20follow%20along.-,Wget%20is%20a%20useful%20program%2C%20run%20through%20your%20computer's,line%2C%20for%20retrieving%20online%20material.&text=It%20can%20be%20useful%20in,copy%20of%20an%20entire%20website.) here for a great guide of how to use the tool beyond this demonstration.

To install wGet…

Windows: Go here and download and run the installer, then launch your Command Prompt and follow directions below.

OSX/Linux: We need to install wGet via Homebrew on the command line. We will install Homebrew if you haven’t already. Open up your Terminal program in your Utilities folder and enter the following commands to install Homebrew and then wGet.

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install wget
```

All Systems: Once wGet is installed, run the following two commands to download the both sites to local mirrors. Note: this method limits the rate of download to be server-friendly.

```shell
wget https://WikiLeaks.org/irq/ -r -w 2 --limit-rate=150k
wget https://WikiLeaks.org/afg/ -r -w 2 --limit-rate=150k
```

Now you can run the script on the local mirrors!
