# rosbag_filter_gui

> `rosbag filter` with Gooey-based GUI

## Test-passed

- Ubuntu 20.04
- ROS Noetic
- Python 3.8

## Installation

```shell
git clone https://github.com/hibetterheyj/rosbag_filter_gui.git
cd rosbag_filter_gui

conda create -n rosbag_filter_gui python=3.8
conda activate rosbag_filter_gui
# or `source activate rosbag_filter_gui` in ubuntu

pip3 install -U pip
pip3 install -r requirements.txt
```

## Guideline

```shell
python rosbag_filter_gui.py
```

:construction: To be continued

## Test samples downloaded

:construction:

## To-dos

- [ ] add simple video or gif for guideline
- [ ] support for `--print=PRINT-EXPRESSION` and `t` (time of message)
- [ ] add interactive script in command line
- [ ] add script for batch processing
- [ ] apply github CI/CD workflow to test for different system

## Acknowledgment

- [AtsushiSakai/**rosbag_filter_gui**](https://github.com/AtsushiSakai/rosbag_filter_gui): A PyQT4-based GUI tool for rosbag filtering (Thanks for inspiration!)
- [chriskiehl/**GooeyExamples**](https://github.com/chriskiehl/GooeyExamples): Example programs to Demonstrate the functionality of [Gooey](https://github.com/chriskiehl/Gooey)

- [`rosbag filter` in rosbag/Commandline](http://wiki.ros.org/rosbag/Commandline#filter)

