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
        def __init__(self, description="An explanation method", image=None, link=None, name=None, namespace=None, label=None, **kargs):
            super().__init__(name, namespace, **kargs)
            self.label = label
            self.description = description
            self.link = link
            self.image = image

        def get_link(self):
            return self.link

        def get_image(self):
            return self.image

        def get_label(self):
            return self.label
        
        def get_name(self):
            return self.name

        def get_description(self):
            return self.description

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
subgraphx = Perturbations(name="Subgraphx", description="Subgraphx is a novel method utilizing Monte Carlo Tree Search to extract relevant subgraphs as explanations.",
    label="subgraphx", explains_with=[subgraph], link="https://arxiv.org/pdf/2102.05152.pdf", image="format/subgraph.png",
    can_explain=[node_classification_regression, edge_prediction, graph_classification_regression])

gnnexplainer = Perturbations(name="GNNExplainer", description="GNNExplainer is one of the first GNN explainability methods, and stood the test of time due to it's wide range of applicability and good performances.",
    label="gnnexplainer", explains_with=[soft_mask_edge, soft_mask_node], link="https://proceedings.neurips.cc/paper/2019/file/d80b7040b773199015de6d3b4293c8ff-Paper.pdf", image="format/mask.png",
    can_explain=[node_classification_regression, edge_classification_regression, edge_prediction, graph_classification_regression, community_detection])

pgexplainer = Perturbations(name="PGExplainer", description="PGExplainer is a learning-based parametrized explainer which exhibits good results, especially on generalization.",
    label="pgexplainer", explains_with=[hard_mask_edge], link="https://arxiv.org/pdf/2011.04573.pdf", image="format/mask.png",
    can_explain=[node_classification_regression, edge_classification_regression, edge_prediction, graph_classification_regression, community_detection])

graphmask = Perturbations(name="GraphMask", description="GraphMask is a very effective graph explainability method originally developped for Natural Language Processing purposes.",
    label="graphmask", explains_with=[hard_mask_edge], link="https://arxiv.org/pdf/2010.00577.pdf", image="format/mask.png",
    can_explain=[node_classification_regression, graph_classification_regression, community_detection])

pgmexplainer = Surrogate(name="PGM-Explainer", description="PGM-Explainer is a surrogate-based method which proposes to explain GNNs using a white box probabilistic graphical model (Bayesian network).",
    label="pgmexplainer", explains_with=[bayesian_network], link="https://arxiv.org/pdf/2010.05788.pdf", image="format/bn.png",
    can_explain=[node_classification_regression, edge_prediction, graph_classification_regression, community_detection])

gnnlrp = Decomposition(name="GNN-LRP", description='GNN-LRP is a method exploiting a "natural" explanation present in GNNs by using layer-wise relevance propagation.',
    label="gnnlrp", explains_with=[walk], link="https://arxiv.org/pdf/2006.03589.pdf", image="format/walk.png",
    can_explain=[node_classification_regression, graph_classification_regression])

xgnn = Generation(name="XGNN", description="XGNN is a mode-level explanation method, meaning that it aims to explain an entire GNN model rather than a single input/output pair.",
    label="xgnn", explains_with=[typical_graph], link="https://arxiv.org/pdf/2006.02587.pdf", image="format/typical_graph.png",
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