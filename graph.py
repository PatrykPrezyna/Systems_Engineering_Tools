# CREATE
#   (Drill:Object {name: 'Drill'}),
#   (Motor:Person {name: 'Motor'}),
#   (Drill)-[:Touches]->(Motor),
#   (Motherboard:Person {name: 'Motherboard'}),
#   (Motor)-[:ToucheElectrics]->(Motherboard),

import csv
# from py2neo import Graph

def csv_to_cypher(csv_path):
    # Read CSV matrix
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Generate node creation queries
    cypher = []
    # Generate all objects
    for row in rows:
        object_name = row[0].replace(" ", "_")
        cypher.append(f'CREATE ({object_name}:Object {{name: "{object_name}"}})')

    # Generate relationship queries
    relationships = []
    for i, row in enumerate(rows):
        source = row[0].replace(" ", "_")
        for idx, value in enumerate(row[1:]):
            target = rows[idx][0].replace(" ", "_")
            if i > idx:
                if value[0] == '1':
                    if source == 'power_cable' or source == 'Power_Button' or source == 'motors': 
                        relationships.append(f'CREATE ({source})-[:electrical]->({target})')
                        print('source, electrical', source)
                    else:
                        relationships.append(f'CREATE ({source})-[:info]->({target})')
                        print('source, info', source)
                if value == '2':
                    relationships.append(f'CREATE ({source})-[:info]->({target})')
                    relationships.append(f'CREATE ({source})-[:electrical]->({target})')
                if value.split(".")[-1] == '5' and value != '5':
                    relationships.append(f'CREATE ({source})-[:physical]->({target})')
            else:
                pass

    query = cypher
    for rel in relationships:
        query.append(rel)

    with open("graph.txt", 'w') as f:
        f.write("\n".join(query))

    # Execute in single transaction
    # tx = graph.begin()
    # tx.run("\n".join(cypher))
    # for rel in relationships:
    #     tx.run(rel)
    # graph.commit(tx)

# Usage
# graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
csv_to_cypher("graph.csv")