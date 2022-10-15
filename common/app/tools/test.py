from configparser import ConfigParser

config = ConfigParser()
config.read('ini.ini')

print(config.has_section('CONFIG'))





# import asyncio
#
#
# async def fun1(x):
#     print(x**2)
#     await asyncio.sleep(3)
#     print("Fun1 done!")
#
#
# async def fun2(x):
#     print(x ** 2)
#     await asyncio.sleep(3)
#     print("Fun2 done!")
#
#
# async def main():
#     task1 = asyncio.create_task(fun1(4))
#     task2 = asyncio.create_task(fun2(4))
#
#     await task1
#     await task2
#
# asyncio.run(main())
