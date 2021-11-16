# -*-coding:utf-8 -*-
"""
@File    :   rosbag_filter_gui.py
@Time    :   2021/11/16
@Author  :   Yujie He
@Version :   1.0
@Contact :   yujie.he@epfl.ch
@State   :   Dev
"""


import os
import sys
import json
import rosbag
import argparse
import subprocess, yaml
from gooey import Gooey, GooeyParser

cur_path = os.path.dirname(os.path.realpath(__file__))


class RosYaml:
    def __init__(self, file, encoding="utf-8"):
        self.file = file
        self.encoding = encoding

    def get_ymal_data(self):
        with open(self.file, encoding=self.encoding) as f:
            data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return data

    def write_yaml(self, data):
        with open(self.file, "w", encoding=self.encoding) as f:
            yaml.dump(data, stream=f, allow_unicode=True)


def get_topics():
    yaml_path = os.path.join(cur_path, "bag_cached.yaml")
    if os.path.exists(yaml_path):
        test_yaml = RosYaml(yaml_path)
        data = test_yaml.get_ymal_data()
        topic_list = []
        for topic in data["topics"]:
            topic_msg = "({}) ".format(topic["messages"]) + topic["topic"]
            topic_list.append(topic_msg)
        return topic_list
    else:
        return []


def gen_bag_info(input_bag):
    info_dict = yaml.safe_load(
        subprocess.Popen(
            ["rosbag", "info", "--yaml", str(input_bag)], stdout=subprocess.PIPE
        ).communicate()[0]
    )
    bagname = input_bag.split("/")[-1]
    return info_dict


@Gooey(
    default_size=(800, 1000),  # starting size of the GUI
    dump_build_config=False,  # Dump the JSON Gooey uses to configure itself
    load_build_config=None,  # Load a JSON Gooey-generated configuration
    monospace_display=False,  # Use a mono-spaced font in the output screen
)
def main():
    parser = GooeyParser(description="Filter rosbag with GUI")
    subs = parser.add_subparsers(help="commands", dest="command")

    main_parser = subs.add_parser("Main")
    read_bag_group = main_parser.add_argument_group("I/O Options")
    read_bag_group.add_argument(
        "-i",
        "--input_bag",
        type=str,
        # help="input rosbag",
        default="./test.bag",
        widget="FileChooser",  # Gooey
    )
    read_bag_group.add_argument(
        "-o",
        "--out_dir",
        default=cur_path,
        type=str,
        # help="input rosbag folder",
        widget="DirChooser",  # Gooey
    )
    stuff = main_parser.add_mutually_exclusive_group(
        required=True,
        gooey_options={"initial_selection": 0},
    )
    stuff.add_argument(
        "--read4process",
        metavar="Extract bag info",
        action="store_true",
        help="Read rosbag for processing",
    )
    stuff.add_argument(
        "--filter2save",
        metavar="Filter bag and Export",
        help="Choose topic(s) to filter out",
        dest="filtered_topics",
        widget="Listbox",  # Dropdown Listbox
        choices=get_topics(),
        nargs="*",
        gooey_options={
            "height": 200,
            "validator": {
                "test": 'user_input != "Select Topics"',
                "message": "Choose a save file from the list",
            },
        },
    )
    filename_group = main_parser.add_argument_group(
        "Filename Options", "Customize the name of filtered rosbags"
    )
    filename_group.add_argument(
        "--suffix",
        default="_filtered",
        type=str,
    )
    filename_group.add_argument(
        "--prefix",
        default="",
        type=str,
    )

    args = parser.parse_args()

    if args.read4process:
        if not os.path.exists("bag_yaml"):
            os.makedirs("bag_yaml")
        info_dict = gen_bag_info(args.input_bag)
        with open(
            os.path.join("bag_yaml", args.input_bag.replace(".bag", ".yaml")), "w"
        ) as file:
            yaml.dump(info_dict, file)
        with open(os.path.join(cur_path, "bag_cached.yaml"), "w") as file:
            yaml.dump(info_dict, file)

        print("duration:", info_dict["duration"])
        print("start:", info_dict["start"])
        print("end:", info_dict["end"])
        print("topics:")
        for topic in info_dict["topics"]:
            topic_msg = "{} msgs: {} ({})".format(
                str(topic["messages"]), topic["topic"], topic["type"]
            )
            print("\t" + topic_msg)
    else:
        print("Filtered topics:")
        for filtered_topic in args.filtered_topics:
            print("\t" + filtered_topic.split(" ")[-1])
        remain_topics = []
        print("Remaining topics:")
        for topic_msg in get_topics():
            if topic_msg in args.filtered_topics:
                pass
            else:
                print("\t" + topic_msg.split(" ")[-1])
                remain_topics.append(topic_msg.split(" ")[-1])

        in_bagname = args.input_bag.split("/")[-1]
        # in_dir = os.path.dirname(args.input_bag)
        out_dir = args.out_dir
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        out_bagname = args.prefix + in_bagname[:-4] + args.suffix + ".bag"
        cmd = 'rosbag filter {} {} "'.format(
            str(args.input_bag), os.path.join(out_dir, out_bagname)
        )
        for topic in remain_topics:
            cmd += "topic=='"
            cmd += topic
            cmd += "' or "
        cmd = cmd[:-4]
        cmd += '"'
        print("\nCommand:\n\t{}".format(cmd))
        print("\nConverting....")
        os.system(cmd)
        print("\nFinished!!!")
        os.remove("bag_cached.yaml")


if __name__ == "__main__":
    if "gooey-seed-ui" in sys.argv:
        print(json.dumps({"--filtered_topics": get_topics()}))
    else:
        # mk_savedir()
        main()


"""
Acknowledge:
    - https://github.com/AtsushiSakai/rosbag_filter_gui
    - https://github.com/chriskiehl/Gooey
    - https://github.com/chriskiehl/GooeyExamples/blob/ac162e0b71e72beb15cf25051138d4d69bdb5f75/examples/argument_groups_tabs.py
    - http://wiki.ros.org/rosbag/Commandline#filter
"""
