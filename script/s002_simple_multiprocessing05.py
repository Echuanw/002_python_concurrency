from multiprocessing import Process, current_process, Pool , cpu_count
import time

""" 
    The sixth use script of Process : s002_simple_multiprocessing05.py
    1 进程池
"""


def process_task(item):           # core business
    if item == 2:
        raise NotImplemented('业务步骤出错，执行中断')
    time.sleep(1)
    return f"【{current_process().name}】进程，正在处理业务 {item}"

def process_task_callback(rst):
    """进程处理的回调操作"""
    print('【业务回调】%s' % (rst))

def process_task_error(err):
    """error process"""
    print('【业务错误】%s' % (err))


def main():
    p_pool = Pool(
        processes=cpu_count()     # cpu 核心数
    )
    for item in range(5):
        rst = p_pool.apply_async(        # 异步方式执行
            func=process_task,
            args=(item,),
            callback=process_task_callback,  # 处理完成后进行回调处理
            error_callback=process_task_error
        ) 
        print(rst.get())     # 进行执行完成，触发callback() 并返回
    p_pool.close()   # 关闭进程池

if __name__ == '__main__':
    main()