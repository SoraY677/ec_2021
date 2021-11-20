import subprocess
import time

from src import submit
from src.solution_search import create

# def run_multisleep():
#     """ 複数の子プロセスでrun_sleep.pyを実行する """
#     def run_sleep():
#         proc = subprocess.Popen([
#             "python",
#             "test/windows/syn_pop.py",
#             str("family_type_id == [0,3,4,60,70,80] and role_household_type_id == [0,1,21,30,31] and industry_type_id == [-1,10,20,30,50,60,80,90,100,160,170,200] and employment_type_id == [-1,20,30] and company_size_id == [-1,5,10]"),
#             str(9) ,
#             str("[2]"), 
#             str("hakodate"),
#             str("[123,42,256]")
#              ],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         return proc

#     start = time.time()
#     procs = []
#     for _ in range(1):
#         procs.append(run_sleep())

#     for proc in procs:
#         res,err = proc.communicate()
#         print(res)
#         print(type(res))
#         print(res[0])

#     end = time.time()
#     print("Finished in {} seconds.".format(end-start))

# if __name__ == "__main__":
#     run_multisleep()

sol = create.create_init_sol(function_id="[1,2]",city="hakodate",seeds="[123,42,256]")
submit.regist(sol, ["python","test/windows/syn_pop.py"] )
# print(submit.regist(sol, ["python","test/windows/synpop.py"] ))
print(submit.run())
# command = [ "python",
#             "test/windows/syn_pop.py",]
# command.extend(submit._sol_encode(sol))
# print(command)
# proc = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# # print(proc.communicate())




