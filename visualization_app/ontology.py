import owlready2 as ow2

onto = ow2.get_ontology("http://test.org/onto.owl")

with onto:
    '''
    Populate the ontology
    '''

    # Entities Definition

    class Explanation_Method(ow2.Thing): pass

    # Sublass Explanation Methods

    # class GNNExplainer(Explanation_Method): pass

    # class PGExplainer(Explanation_Method): pass

    # class PGM_Explainer(Explanation_Method): pass

    # class GraphMASK(Explanation_Method): pass

    # class GNN_LRP(Explanation_Method): pass

    # class SubgraphX(Explanation_Method): pass

    # class XGNN(Explanation_Method): pass


    class Task(ow2.Thing): pass

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

    # class Mask(Explanation_Format): pass
    # class Soft_Mask(Mask): pass
    # class Hard_Mask(Mask): pass

    # class Walk(Explanation_Format): pass

    # class Subgraph(Explanation_Format): pass

    # class PGM(Explanation_Format): pass

    # class Typical_Graph(Explanation_Format): pass


    class Dataset(ow2.Thing): pass



    class explains_with(ow2.ObjectProperty):
        domain = [Explanation_Method]
        region = [Explanation_Format]

print(list(onto.classes()))