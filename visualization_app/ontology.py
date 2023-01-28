import owlready2 as ow2

onto = ow2.get_ontology("http://test.org/onto.owl")

with onto:
    '''
    Populate the ontology
    '''

    # Entities Definition

    class Item(ow2.Thing): pass
    class Node(Item): pass
    class Edge(Item): pass
    class Graph(Item): pass

    class Explanation_Method(ow2.Thing):
        def details(self):
            print(self.label[0])

    class Instance_level_explanation(Explanation_Method): pass
    class Gradient_features(Instance_level_explanation): pass
    class Perturbations(Instance_level_explanation): pass
    class Decomposition(Instance_level_explanation): pass
    class Surrogate(Instance_level_explanation): pass
    class Model_level_explanation(Explanation_Method): pass
    class Generation(Model_level_explanation): pass

    # Sublass Explanation Methods

    # class GNNExplainer(Explanation_Method): pass

    # class PGExplainer(Explanation_Method): pass

    # class PGM_Explainer(Explanation_Method): pass

    # class GraphMASK(Explanation_Method): pass

    # class GNN_LRP(Explanation_Method): pass

    # class SubgraphX(Explanation_Method): pass

    # class XGNN(Explanation_Method): pass


    class Task(ow2.Thing):
        def __init__(self, name=None, namespace=None, **kargs):
            super().__init__(name, namespace, **kargs)
        

    # Subclass Tasks
    # class Node_C_R(Task): pass

    # class Edge_C_R(Task): pass

    # class Edge_Prediction(Task): pass

    # class Graph_C_R(Task): pass

    # class Community_Detection(Task): pass

    # class Graph_Clustering(Task): pass

    # class Graph_Generation(Task): pass



    class Explanation_Format(ow2.Thing): pass

    # Subclass Explanation Formats

    class Mask(Explanation_Format): pass
    class Soft_Mask(Mask): pass
    class Hard_Mask(Mask): pass

    # class Walk(Explanation_Format): pass

    # class Subgraph(Explanation_Format): pass

    class PGM(Explanation_Format): pass

    # class Typical_Graph(Explanation_Format): pass


    class Dataset(ow2.Thing): pass



    # class explains_with(ow2.ObjectProperty):
    #     domain = [Explanation_Method]
    #     region = [Explanation_Format]
    

    class explains_with(Explanation_Method >> Explanation_Format, ow2.ObjectProperty): pass
    class can_explain(Explanation_Method >> Task, ow2.ObjectProperty): pass
    class applies_on(Mask >> Item, ow2.ObjectProperty): pass
    class focuses_on(Task >> Item, ow2.ObjectProperty): pass

base_format = Explanation_Format("base_format")

# formats
subgraph = Explanation_Format("subgraph", label="subgraph")
walk = Explanation_Format("walk", label="walk")
typical_graph = Explanation_Format("typical_graph", label="typical_graph")
soft_mask_edge = Soft_Mask("soft_mask_edge", label="soft_mask_edge", applies_on=[Edge])
soft_mask_node = Soft_Mask("soft_mask_node", label="soft_mask_node", applies_on=[Node])
hard_mask_edge = Hard_Mask("hard_mask_edge", label="hard_mask_edge", applies_on=[Edge])
hard_mask_node = Hard_Mask("hard_mask_node", label="hard_mask_node", applies_on=[Node])
bayesian_network = PGM("bayesian_network", label="bayesian_network")

# tasks
node_classification_regression = Task("node_classification_regression", label="node_classification_regression", focuses_on=[Node])
edge_classification_regression = Task("edge_classification_regression", label="edge_classification_regression", focuses_on=[Edge])
edge_prediction = Task("edge_prediction", label="edge_prediction", focuses_on=[Edge])
graph_classification_regression = Task("graph_classification_regression", label="graph_classification_regression", focuses_on=[Graph])
community_detection = Task("community_detection", label="community_detection")
graph_clustering = Task("graph_clustering", label="graph_clustering", focuses_on=[Graph])
graph_generation = Task("graph_generation", label="graph_generation", focuses_on=[Graph])

# methods
base_method = Explanation_Method("base_method")
subgraphx = Perturbations("subgraphx", label="subgraphx", explains_with=[subgraph],
    can_explain=[node_classification_regression, edge_prediction, graph_classification_regression])
gnnexplainer = Perturbations("gnnexplainer", label="gnnexplainer", explains_with=[soft_mask_edge, soft_mask_node],
    can_explain=[node_classification_regression, edge_classification_regression, edge_prediction, graph_classification_regression, community_detection, graph_clustering])
graphmask = Perturbations("graphmask", label="graphmask", explains_with=[hard_mask_edge],
    can_explain=[node_classification_regression, graph_classification_regression])
pgmexplainer = Surrogate("pgmexplainer", label="pgmexplainer", explains_with=[bayesian_network],
    can_explain=[node_classification_regression, edge_classification_regression, edge_prediction, graph_classification_regression, community_detection, graph_clustering])
gnnlrp = Decomposition("gnnlrp", label="gnnlrp", explains_with=[walk],
    can_explain=[node_classification_regression, graph_classification_regression])
xgnn = Generation("xgnn", label="xgnn", explains_with=[typical_graph],
    can_explain=[graph_classification_regression])


# print(list(ow2.default_world.sparql("""
    # SELECT (COUNT(?x) AS ?nb)
    # {?x a onto:Explanation_Format .}
# """)))
# 
# print(list(ow2.default_world.sparql("""
    # SELECT (COUNT(?x) AS ?nb)
    # {?x a onto:Explanation_Method .
    # ?x onto:explains_with ?s .
    # ?s rdfs:label "subgraph" . }
# """)))

# print(list(ow2.default_world.sparql("""
#     SELECT ?x WHERE
#     {
#         ?x a ?c .
#         ?c rdfs:subClassOf* onto:Explanation_Method .
        
#         ?x onto:explains_with ?m .
#         ?m rdfs:subClassOf* onto:Explanation_Format .
#     }""")))

# print(list(ow2.default_world.sparql(f'''
#     SELECT ?x WHERE
#     {{
#         ?x a ?c .
#         ?c rdfs:subClassOf* onto:Explanation_Method .
        
#         ?x onto:explains_with  ?d .
#         ?d rdfs:subClassOf* onto:{subgraph.label[0]} .
#         ?x onto:can_explain onto:{node_classification_regression.label[0]} .
#     }}''')))


def sparql_query(format, task):
    form_query = f'''
            ?x onto:explains_with ?d .
            {{
                ?d a ?f .
                ?f rdfs:subClassOf* ?g .
                ?g rdfs:subClassOf* onto:{format} .
            }}
            UNION
            {{
                ?d a ?e .
                ?e rdfs:subClassOf* onto:{format} .
            }}
            UNION
            {{
                ?d rdfs:subClassOf* onto:{format}
            }}
            '''

    task_query = f'''
            ?x onto:can_explain ?y .
            {{
                ?y rdfs:subClassOf* onto:{task} .
            }}
            UNION
            {{
                ?y a ?z .
                ?z rdfs:subClassOf* onto:{task} .
            }}
        '''

    query = f'''
        SELECT DISTINCT ?x WHERE
        {{
            ?x a ?c .
            ?c rdfs:subClassOf* onto:Explanation_Method .
            
            {form_query}
            {task_query}

        }}'''
    
    values = list(ow2.default_world.sparql(query))
    
    return values

if __name__ == '__main__':
    for method in sparql_query("Hard_Mask", "Task"):
        print(method[0].details())