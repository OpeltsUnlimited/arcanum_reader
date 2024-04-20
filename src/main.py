from argparse import ArgumentParser, RawDescriptionHelpFormatter
from git_helper import MyRepo
import json
from arcanum_root import Arcanum_root
from to_html import ToHtml
from os import path
from my_html_file import My_html_file

example_text='''
Example:
  main.py -p local    <- pull both
  main.py -pc local   <- pull both and check what to recrearte for local
  main.py -c markup   <- check if markup has to be recreated
  main.py -pa local   <- pull arcanum, and recreate the static page
  main.py -t markup   <- recreate the aecanumtesting markup, no pulling from git
'''

if __name__ == "__main__":
    parser  = ArgumentParser(
        prog='Arcanum-Reader',
        description='Reads data from a arcanum Repo, and builds a wiki-like page',
        epilog=example_text,
        usage="main.py [-p][-c][-a][-t] {local,markup} [-o out][-r root]",
        formatter_class=RawDescriptionHelpFormatter)
    
    parser.add_argument('-p', '--pull', action='store_true', help="pull specified version -a/-t,")
    parser.add_argument('-c', '--check', action='store_true', help="check if something to rebuild, needs -p, ignores -a/-t")
    parser.add_argument('-a', '--arcanum', action='store_true', help="generate for arcanum")
    parser.add_argument('-t', '--testing', action='store_true', help="generate for arcanumtesting")
    parser.add_argument('--RESET', action='store_true', help="forget which versions were used to be build bevore")
    sub=parser.add_subparsers(title="operation", dest='operation', help="choose what to create")

    sub_local = sub.add_parser("local", help="generate local/static webpage")
    sub_local.add_argument("-o", "--output", nargs=1, help="output directory", default="./public")
    sub_local.add_argument("-r", "--root", nargs=1, help="prepended to generated links/paths, usefull for nested-routes", default="")
    
    sub_markup = sub.add_parser("markup", help="generate wiki/markup into a specified folder")
    sub_markup.add_argument("-o", "--output", nargs=1, help="output directory", default="")
    sub_markup.add_argument("-r", "--root", nargs=1, help="prepended to generated links/paths, usefull for nested-routes", default="")

    args = parser.parse_args()

    # pull first
    arcanum_repo = MyRepo("arcanum","https://gitlab.com/mathiashjelm/arcanum/")
    arcanumtesting_repo = MyRepo("arcanumtesting","https://gitlab.com/arcanumtesting/arcanum/")
    if args.pull:
        pull_arcanum = args.arcanum or (not args.arcanum and not args.testing)
        pull_testing = args.testing or (not args.arcanum and not args.testing)

        if pull_arcanum:
            arcanum_repo.pull()
        else:
            pass
        if pull_testing:    
            arcanumtesting_repo.pull()
        else: #args.testing
            pass
    else: # nothing was pulled
        pass

    # load used for check, and make sure minimum data structure exsists
    last_run = None
    try:
        with open('last_run.json', 'r') as file:
            last_run = json.load(file)
    except FileNotFoundError:
        pass # during first run the data might not exsist
    if  not last_run:
        last_run = {}
    if not "local" in last_run:
        last_run["local"] = {}
    last_local = last_run["local"]
    if not "arcanum" in last_local:
        last_local["arcanum"] = ""
    if not "testing" in last_local:
        last_local["testing"] = ""
    if not "markup" in last_run:
        last_run["markup"] = {}
    last_markup = last_run["markup"]
    if not "arcanum" in last_markup:
        last_markup["arcanum"] = ""
    if not "testing" in last_markup:
        last_markup["testing"] = ""

    # check if a operation was specified:
    if not args.operation:
        exit(0)

    # check for lokal:
    if 'local' in args.operation:
        if args.check:
            print(arcanum_repo.getCurrentCommit())
            if arcanum_repo.getCurrentCommit() != last_local["arcanum"]:
                args.arcanum=True
            if arcanumtesting_repo.getCurrentCommit() != last_local["testing"]:
                args.testing=True

        arcanum_output = path.join(args.output,"arcanum")
        arcanum_root = f"{args.root}/arcanum"
        testing_output = path.join(args.output,"testing")
        testing_root = f"{args.root}/testing"

        if args.arcanum:
            print("Do Arcanum, local")
            try:
                arcanum_data = Arcanum_root()
                arcanum_data.read("arcanum/data")

                convert = ToHtml(arcanum_output,arcanum_root)
                convert.toHtml(arcanum_data)

                last_local["arcanum"] = arcanum_repo.getCurrentCommit()
            except Exception as exp: # i only want to skip the set-last part in case of a exeption, but a catch/exept is mandatory  
                raise exp # so i just re-trow it (altough bad practice, you schouldent catch if not used)

        if args.testing:
            print("Do Testing, local")
            last_local["testing"] = arcanumtesting_repo.getCurrentCommit()

        # root index page
        arcanum_exsists = path.isdir(arcanum_output)
        testing_exsists = path.isdir(testing_output)

        index_file = My_html_file("index", args.output)
        list = index_file.content.add("ul")

        if arcanum_exsists:
            list_element = list.add("li")
            link = list_element.add("a")
            link.attrib["href"]=arcanum_root
            link.text = "Arcanum"
        if testing_exsists:
            list_element = list.add("li")
            link = list_element.add("a")
            link.attrib["href"]=f"{args.root}/testing"
            link.text = "Testing"

        if arcanum_exsists and testing_exsists:
            pass
        elif arcanum_exsists: # only arcanum exsists -> Redirect
            meta = index_file.addMeta()
            meta.attrib["http-equiv"]="refresh"
            meta.attrib["content"]=f"0 url={arcanum_root}"
        else:
            meta = index_file.addMeta()
            meta.attrib["http-equiv"]="refresh"
            meta.attrib["content"]=f"0 url={testing_root}"
        
        index_file.write()
        
    # check for markup
    if 'markup' in args.operation:
        if args.check:
            if arcanum_repo.getCurrentCommit() != last_markup["arcanum"]:
                args.arcanum=True
            if arcanumtesting_repo.getCurrentCommit() != last_markup["testing"]:
                args.testing=True

        if args.arcanum:
            print("Do Arcanum, local")
            last_markup["arcanum"] = arcanum_repo.getCurrentCommit()
        if args.testing:
            print("Do Testing, local")
            last_markup["testing"] = arcanumtesting_repo.getCurrentCommit()

    with open('last_run.json', 'w') as file:
        json.dump(last_run, file)


    