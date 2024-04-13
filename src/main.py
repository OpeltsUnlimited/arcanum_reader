from argparse import ArgumentParser, RawDescriptionHelpFormatter
from git_helper import MyRepo

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
    sub_local.add_argument("-r", "--root", nargs=1, help="prepended to generated links/paths, usefull for nested-routes")
    
    sub_markup = sub.add_parser("markup", help="generate wiki/markup into a specified folder")
    sub_markup.add_argument("-o", "--output", nargs=1, help="output directory", default="")
    sub_markup.add_argument("-r", "--root", nargs=1, help="prepended to generated links/paths, usefull for nested-routes")

    args = parser.parse_args()

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