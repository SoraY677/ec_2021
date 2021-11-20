from src import submit
from src.solution_search import create


sol = create.create_init_sol(function_id="[1,2]",city="hakodate",seeds="[123,42,256]")
submit.regist(sol, ["python","test/windows/syn_pop.py"] )
result = submit.run()

print(result)



