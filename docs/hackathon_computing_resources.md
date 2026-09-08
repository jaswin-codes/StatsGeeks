# Hackathon Computing Resources Orientation

## Metadata
- Duration: ~13 minutes 29 seconds
- Source: Video transcript (data science regional hackathon orientation talk)
- Main Topics: JupyterLab server access, login details, folder structure, Python environment, memory management, package installation, virtual environments, data upload/download, support channels

## Introduction

Hello everybody, my name is Tim Glitter. I'm a system administrator at IDIA, and today I'll be speaking to you about the computing resources that you'll be using for this hackathon.

There are a few topics I want to cover, starting with the computing resources that will be allocated to each team, and the login details you'll require to gain access to these resources. You'll be using JupyterLab, and for this hackathon specifically, memory management will be important, so we'll be touching on that. I'll also cover how to install packages, create virtual environments, and upload and download data from the server, since you'll probably want to download some of the data after the hackathon is done.

## Computing Resources

For each hackathon, there are multiple teams, with three people per team, up to a maximum of eight teams. Each team of three people will have access to their own JupyterLab server.

Each JupyterLab server has:
- 16 CPUs
- 128 GB of RAM
- 200 GB of hard drive space

For this hackathon, the 128 GB of RAM will probably be the main bottleneck, so monitoring techniques will be covered shortly.

To gain access to the server, each team will be given a URL along with a username and password so that each team member can log in to their server.

## Login Details

The format of the URL will be shown on the screen; you'll just have to replace "region" with your specific hackathon region.

For example, using Chile as the region for the first team, the URL would follow the pattern:

```
chile-dsr-2025-1
```

(DSR stands for Data Science Regional hackathon.)

Along with the URL, you'll have username and password pairs. Even though there are only three team members, an extra login has been created just in case it's needed, and you'll use this username and password to log in.

> **[Visual reference omitted from transcript]** — login dialogue screenshot

Once you've entered the URL into the browser, you'll see the login dialogue. Usernames follow a similar format:
- Team one usernames start with "1" followed by the user's index/number.
- Team two usernames start with "2" followed by the user's number.

After logging in, you'll be loaded into a JupyterLab session.

## JupyterLab

> **[Visual reference omitted from transcript]** — screenshot of the JupyterLab launcher

After logging in, you'll see the JupyterLab launcher. From here you are able to open:
- Notebooks
- Scripts
- Text files
- The browser file structure
- A Linux terminal

If you lose the launcher window, you can use the menus to open these components individually, or open a new launcher window.

## Folder Structure

After logging in, each user will have a separate copy of the hackathon repository, which is already cloned. In addition, there is a **shared folder**, where files and folders are shared across team members. If you want to share your work, this is the place to save the files.

## Default Python Environment

For this hackathon, all packages required by the provided notebooks have already been pre-installed. You don't need to install any packages to run through the provided notebooks.

> **[Visual reference omitted from transcript]** — screenshot of the repository showing Python notebooks and data folders

## Jupyter Notebook Memory Display

The provided notebooks have a memory extension added at the bottom, which shows how much data has been loaded into memory for that specific notebook.

## Jupyter Memory Management Overview

Memory is likely to be the main bottleneck for this hackathon, so it will be important to monitor it. To reiterate:
- Each server has 128 GB of RAM.
- Jupyter itself will have access to about 120 GB of that.

It will be important for the team to manage these resources and coordinate. If the team exceeds these resources (uses more than 128 GB of RAM), a memory monitoring program will look for the largest open notebook and accompanying kernel and terminate it. This is unfortunately necessary — otherwise Jupyter service stability cannot be guaranteed.

> **Note:** If you want to run a large notebook, it is important to let the other team members know and monitor memory usage together. If one of your kernels does get killed, a dialog box will be shown to indicate this.

The easiest way to monitor these resources is to open a new terminal (File → New Terminal) and use the `htop` command-line utility.

## htop — Server CPU & Memory Usage

`htop` shows:
- The percentage usage of every CPU
- The total memory used by the server

Example: 36.9 GB used out of a total of 123 GB.

If everybody starts running multiple notebooks, usage can become much higher — for example, 107 GB used out of 123 GB, with most CPUs almost fully occupied.

```bash
htop
```

## Notebook Memory Usage

Another way to monitor memory usage is to look at the bottom of a specific notebook, which shows how much memory that notebook is using.

Example: a "reading data" notebook using 36 GB. Clicking on a different notebook (e.g., "introduction") refreshes the display at the bottom of the screen to show that notebook's memory usage.

Using both `htop` (whole-server view) and the per-notebook memory display, you should get a good overview of how much resources the team is using, and can cut back if you're getting close to the limit, to avoid large notebooks being killed.

## Closing Jupyter Kernels

You can view the Jupyter kernels that are loaded by clicking a specific button and expanding the list of kernels.

> **Note:** Sometimes a Jupyter kernel can detach from its notebook and continue running in the background, using memory. In that case, you can expand the kernel list, find the kernel with no corresponding notebook, and shut it down.

## Package Installation

It is possible to install packages into the default Python environment, which is accessible to the whole team. The command for this is shown on-screen (a standard `pip install` with the package name). The virtual environment is stored in the shared folder mentioned earlier.

```bash
pip install <package_name>
```

You can also install packages for yourself only using:

```bash
pip install --user <package_name>
```

These commands are also documented in the README in the repository.

**Example:** Opening a new terminal (File → New Terminal), running the install command for the `scipy` package, and seeing "successfully installed" — after this, the package is accessible in the default Python environment provided for the hackathon.

## Creating a New Virtual Environment

In some cases you might want to create your own virtual environment — for instance, if you want to install a package that might have dependency conflicts with existing installed packages, and you just want to test something out.

The steps (all performed in the terminal) are:

1. Use the `venv` module to create a virtual environment.
2. Source/activate it.
3. Install `ipykernel`.
4. Create a new Jupyter kernel so that Jupyter can find it.
5. Install the packages that you require.

```bash
python -m venv myenv
source myenv/bin/activate
pip install ipykernel
python -m ipykernel install --user --name=myenv
pip install <required_packages>
```

After doing these steps, a new Jupyter kernel will show up that you'll be able to launch. These commands are also shown in the GitHub README, so you don't have to remember them.

## Uploading and Downloading Data

This is built into the Jupyter interface:
- **Upload:** use the upload button.
- **Download:** right-click on any file.

> **Note:** You can't download whole directories at once. In that case, use the terminal and the `tar` command-line utility to bundle multiple files together, then download the single resulting file.

```bash
tar -cvf archive_name.tar folder_to_download/
```

## Getting Support

For common problems (login issues, package installation problems, etc.), most of these are covered in this presentation. First, check:
- The README
- The GitHub README

These resources answer a lot of common queries.

Most regional hackathons will have tutors available for consultation as well.

For more serious problems, these should be raised with the regional team or the lead organizer — most likely needed if multiple people are having a similar problem that isn't easy to resolve. In that case, it's important to provide:
- A short description of what happened
- A screenshot or copy of the actual error message
- Information about the user login and team number

The regional team has contact details and will raise a support ticket, following up as soon as possible throughout the hackathon.

## Summary

- Each team has its own JupyterLab server with 16 CPUs and 128 GB of RAM.
- It's important to carefully manage RAM resources between team members and coordinate usage.
  - While exploring the system independently at first, try to keep to about a third of the RAM per user.
  - Coordinate with the team once you want to start running larger notebooks.
- **Monitoring:**
  - Use `htop` to get an overview of the whole server.
  - Use the memory display at the bottom of a Jupyter notebook to see exactly which notebook is using a lot of memory.
  - Monitor open kernels and close any that are using memory unnecessarily.
- **Sharing:** Use the shared folder to create folders/files to share with the team; you can also install new packages for the whole team in the default Python environment.
- **Support:** Check the documentation first; for serious queries, raise them with the regional organizing team.
- **Important:** Remember to download your data on the last day of the hackathon — the service will be shut down at the end of the final day.

Thanks a lot, and good luck with the hackathon — hope you all enjoy it!
