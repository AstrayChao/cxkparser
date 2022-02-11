import argparse

from cxkParser.utils import doTask, model_split, read_data


def main():
    parse_args = argparse.ArgumentParser()
    parse_args.add_argument('--path', '-p', default=None,
                            required=True, type=str, help="请输入文件根目录")
    parse_args.add_argument('--output', '-o', default=None,
                            required=True, type=str, help="请输入文件的输出目录和文件名, 若不输入文件名，将自动生成8位的token作为文件名")
    parse_args.add_argument('--thread_nums', '-n',
                            default=1, required=False, type=int, help="请输入线程数量，默认不开启")
    args = parse_args.parse_args()
    model_list = read_data(args.path)
    model_list_group = model_split(model_list, args.thread_nums)
    doTask(model_list_group, args.thread_nums, args.output)
    print("cxk程序结束")


if __name__ == '__main__':
    main()
