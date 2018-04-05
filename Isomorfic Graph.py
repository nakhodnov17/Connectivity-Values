from networkx import *
import numpy as np

def Calc_CV(G):
    c_values = np.zeros(G.number_of_nodes(), dtype=np.int)
    c_values_new = np.zeros(G.number_of_nodes(), dtype=np.int)

    for idx in range(c_values.shape[0]):
        c_values[idx] = G.degree(idx)

    unique_prev = len(set(c_values))
    unique_new = G.number_of_nodes()

    while unique_new > unique_prev:

        for idx in range(c_values.shape[0]):
            c_values_new[idx] = np.sum(np.take(c_values, list(G.neighbors(idx))))

        c_values = c_values_new
        unique_prev = unique_new
        unique_new = len(set(c_values_new))
    return np.unique(c_values)

def Calc_DG(G):
    degrees = np.zeros(G.number_of_nodes(), dtype=np.int)

    for idx in range(degrees.shape[0]):
        degrees[idx] = G.degree(idx)
    return np.sort(degrees)

n=15 # number of nodes
m=5 # number of edges

f_p = [0, 0, 0]
f_n = [0, 0, 0]
t_p = [0, 0, 0]
t_n = [0, 0, 0]

graph_size = 100

graphs = list()
for i in range(graph_size):
    graphs.append(gnm_random_graph(n,m))

# equality rate
lim = 0.90

for i in range(graph_size):
    for j in range(graph_size):
        if i < j:
            cv_i = Calc_CV(graphs[i])
            cv_j = Calc_CV(graphs[j])
            deg_i = Calc_DG(graphs[i])
            deg_j = Calc_DG(graphs[j])
            equality_cv = np.sum(cv_i == cv_j) / cv_i.shape[0] > lim
            equality_deg = np.sum(deg_i == deg_j) / deg_i.shape[0] > lim
            equality_rnd = np.random.binomial(1, 0.5, 1)[0]
            real_isom = is_isomorphic(graphs[i], graphs[j])
            if equality_cv and real_isom:
                t_p[0] += 1
            if not equality_cv and real_isom:
                f_n[0] += 1
            if equality_cv and not real_isom:
                f_p[0] += 1
            if not equality_cv and not real_isom:
                t_n[0] += 1

            if equality_deg and real_isom:
                t_p[1] += 1
            if not equality_deg and real_isom:
                f_n[1] += 1
            if equality_deg and not real_isom:
                f_p[1] += 1
            if not equality_deg and not real_isom:
                t_n[1] += 1

            if equality_rnd and real_isom:
                t_p[2] += 1
            if not equality_rnd and real_isom:
                f_n[2] += 1
            if equality_rnd and not real_isom:
                f_p[2] += 1
            if not equality_rnd and not real_isom:
                t_n[2] += 1

print("CV")
print(t_p[0], t_n[0], f_p[0], f_n[0])
print((t_p[0] + t_n[0]) / (t_p[0] + t_n[0] + f_p[0] + f_n[0]))

print("Deg")
print(t_p[1], t_n[1], f_p[1], f_n[1])
print((t_p[1] + t_n[1]) / (t_p[1] + t_n[1] + f_p[1] + f_n[1]))

print("Rand")
print(t_p[2], t_n[2], f_p[2], f_n[2])
print((t_p[2] + t_n[2]) / (t_p[2] + t_n[2] + f_p[2] + f_n[2]))

