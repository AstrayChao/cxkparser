import argparse

from cxkParser.utils import do_task, model_split, read_data


def main():
    parse_args = argparse.ArgumentParser()
    parse_args.add_argument('--path', '-p', default=None,
                            required=True, type=str, help="Please input the path where the file is located")
    parse_args.add_argument('--output', '-o', default=None,
                            required=True, type=str, help="Please input the output directory and file name of the file. e.g. / home/cxkparser/file_name. If you do not input the file name, the default file name is annotation_ < original file name > . e.g. / home/cxkparser/annotation_file_name.xlsx")
    parse_args.add_argument('--thread_nums', '-n',
                            default=1, required=False, type=int, help="Please input the number of threads, Multi-threading is not enabled by default")
    args = parse_args.parse_args()
    model_list = read_data(args.path)
    model_list_group = model_split(model_list, args.thread_nums)
    do_task(model_list_group, args.thread_nums, args.output)
    print("cxkParser end.")


if __name__ == '__main__':
    main()
