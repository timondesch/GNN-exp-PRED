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
            return self.label[0]

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
        def __init__(self, description="any task", name=None, namespace=None, label=None, **kargs):
            self.description = description
            super().__init__(name, namespace, **kargs)
            self.label = label
            self.description = description
        
        def describe(self):
            return self.description

    # Subclass Tasks
    # class Node_C_R(Task): pass

    # class Edge_C_R(Task): pass

    # class Edge_Prediction(Task): pass

    # class Graph_C_R(Task): pass

    # class Community_Detection(Task): pass

    # class Graph_Clustering(Task): pass

    # class Graph_Generation(Task): pass



    class Explanation_Format(ow2.Thing):
        def __init__(self, description="any format", name=None, namespace=None, label=None, **kargs):
            super().__init__(name, namespace, **kargs)
            self.label = label
            self.description = description

        def describe(self):
            return self.description

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

base_format = Explanation_Format(description="any explanation format", label="Explanation_Format")
base_task = Task(description="any task", label="Task")

# formats
subgraph = Explanation_Format(name="subgraph", description="a subgraph", label="subgraph")
walk = Explanation_Format(name="walk", description="a graph walk", label="walk")
typical_graph = Explanation_Format(name="typical_graph", description="a typical graph", label="typical_graph")
soft_mask_edge = Soft_Mask(name="soft_mask_edge", description="a soft mask on edges", label="soft_mask_edge", applies_on=[Edge])
soft_mask_node = Soft_Mask(name="soft_mask_node", description="a soft mask on nodes", label="soft_mask_node", applies_on=[Node])
hard_mask_edge = Hard_Mask(name="hard_mask_edge", description="a hard mask on edges", label="hard_mask_edge", applies_on=[Edge])
hard_mask_node = Hard_Mask(name="hard_mask_node", description="a hard mask on nodes", label="hard_mask_node", applies_on=[Node])
bayesian_network = PGM(name="bayesian_network", description="a Bayesian network", label="bayesian_network")

# tasks
node_classification_regression = Task(name="node_classification_regression", description="node classification and/or regression", label="node_classification_regression", focuses_on=[Node])
edge_classification_regression = Task(name="edge_classification_regression", description="edge classification and/or regression", label="edge_classification_regression", focuses_on=[Edge])
edge_prediction = Task(name="edge_prediction", label="edge_prediction", description="edge prediction", focuses_on=[Edge])
graph_classification_regression = Task(name="graph_classification_regression", description="graph classification and/or regression", label="graph_classification_regression", focuses_on=[Graph])
community_detection = Task(name="community_detection", description="community detection", label="community_detection")
graph_clustering = Task(name="graph_clustering", description="graph clustering", label="graph_clustering", focuses_on=[Graph])
graph_matching = Task(name="graph_matching", description="graph matching", label="graph_matching", focuses_on=[Graph])

# methods
base_method = Explanation_Method(name="base_method")
subgraphx = Perturbations(name="subgraphx", label="subgraphx", explains_with=[subgraph],
    can_explain=[node_classification_regression, edge_prediction, graph_classification_regression])
gnnexplainer = Perturbations(name="gnnexplainer", label="gnnexplainer", explains_with=[soft_mask_edge, soft_mask_node],
    can_explain=[node_classification_regression, edge_classification_regression, edge_prediction, graph_classification_regression, community_detection, graph_clustering])
pgexplainer = Perturbations(name="pgexplainer", label="pgexplainer", explains_with=[hard_mask_edge],
    can_explain=[node_classification_regression, edge_classification_regression, edge_prediction, graph_classification_regression, community_detection, graph_clustering])
graphmask = Perturbations(name="graphmask", label="graphmask", explains_with=[hard_mask_edge],
    can_explain=[node_classification_regression, graph_classification_regression])
pgmexplainer = Surrogate(name="pgmexplainer", label="pgmexplainer", explains_with=[bayesian_network],
    can_explain=[node_classification_regression, edge_classification_regression, edge_prediction, graph_classification_regression, community_detection, graph_clustering])
gnnlrp = Decomposition(name="gnnlrp", label="gnnlrp", explains_with=[walk],
    can_explain=[node_classification_regression, graph_classification_regression])
xgnn = Generation(name="xgnn", label="xgnn", explains_with=[typical_graph],
    can_explain=[graph_classification_regression])

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

def label_query(label):
    query = f'''
        SELECT DISTINCT ?x 
        {{
            ?x rdfs:label "{label}" .
        }}
        '''
    
    values = list(ow2.default_world.sparql(query))
    return values[0][0]

if __name__ == '__main__':
    for method in sparql_query("Hard_Mask", "Task"):
        print(label_query("subgraph"))