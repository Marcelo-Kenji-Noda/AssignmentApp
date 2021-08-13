import numpy as np
from ortools.linear_solver import pywraplp
from teamsandtasks.models import Pessoa, Tarefa, Categoria, Nota

def get_list_with_cost(pearson):
    costs_for_pearson = [x.value for x in Nota.objects.filter(pearson__name=pearson).values()]
    return costs_for_pearson

def calculate_all(individual_resource):
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    Pessoas = Pessoa.objects.all()
    Tarefas = Tarefa.objects.filter(tem_resp=False)
    Notas = Nota.objects.all()

    num_workers = len(Pessoas)
    num_tasks = len(Tarefas)

    a = [x.tempo_estimado for x in Tarefas]
    b = int(individual_resource)

    #Variable defying
    C = np.zeros((num_workers, num_tasks))

    for idx ,i in enumerate(Pessoas):
        for jdx ,j in enumerate(Tarefas):
            categorias_tarefa_j = j.categoria.all()
            Nota_individuo = Nota.objects.filter(pessoa = i, categoria__in = categorias_tarefa_j).values_list('value',flat= True)
            nota_final = -sum(Nota_individuo)
            try:
                coef = 1/len(categorias_tarefa_j)
            except:
                coef = 0
            C[idx-1][jdx-1] = nota_final*coef

    #Optimization Model
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = solver.IntVar(0, 1, '')
    
    # Each worker is assigned to at most 1 task.
    for i in range(num_workers):
        solver.Add(solver.Sum([a[j]*x[i, j] for j in range(num_tasks)]) <= b)

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1)

    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(C[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        data = []
        result['ObjectiveValue'] = solver.Objective().Value()
        for idx ,i in enumerate(Pessoas):
            aux = {}
            aux["pessoa"] = i.nome
            aux["tasks"] = []
            support_hours = 0
            for jdx ,j in enumerate(Tarefas):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[idx, jdx].solution_value() > 0.5:
                    aux["tasks"].append(dict(tarefa =  j.nome,custo =  C[idx][jdx]))
                    support_hours = support_hours + j.tempo_estimado
            aux['tempo_gasto'] = support_hours
            data.append(aux)
        result['assignments'] = data
    else:
        result['tempo_gasto'] = 0
        result['ObjectiveValue'] = 0
        result['assignments'] = None
        

    return result