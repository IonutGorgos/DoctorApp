from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS, Literal
from rdflib.namespace import XSD
import json
import logging
import re

OPENDATA = Namespace("http://opendata.cs.pub.ro/resource/")
OPENDATA_PROPERTY = Namespace("http://opendata.cs.pub.ro/property/")
DBPEDIA_PROPERTY = Namespace("http://dbpedia.org/property/")

logging.basicConfig()

def parseJson(json, graph):
	for entry in output_json:
		nume = entry["nume"].replace("dr", '').replace("Dr", '').replace("DR", '').replace(".", '')
		contact = entry["contact"]
		judet = re.sub(r'\s', '', contact[contact.find("(")+1:contact.rfind(")")])
		localitate = re.sub(r'\s', '', contact[:contact.rfind("(")]).replace("\\", '')
		if len(contact.split(',')) > 1:
			telefon = ''.join(re.findall('\d+', re.sub(r'\s', '', contact.split(',')[1])))
		else:
			telefon = ""
		loc_munca = entry["loc_munca"]
		if loc_munca is not None:
			loc_munca = loc_munca.replace('"', '').replace("'", '').replace('|', '').replace(" ", "_")
		specialitate = entry["specialitate"]
		doctor = URIRef(OPENDATA[re.sub(r'\s', '', nume)])

		graph.add((doctor, RDF.type,  URIRef("http://dbpedia.org/ontology/Person")))
		graph.add((doctor, RDFS.label, Literal(nume, datatype=XSD.string)))
		graph.add((doctor, OPENDATA_PROPERTY["specializare"], Literal(specialitate, datatype=XSD.string)))
		graph.add((doctor, OPENDATA_PROPERTY["loc_munca"], URIRef(OPENDATA[loc_munca])))
		graph.add((doctor, OPENDATA_PROPERTY["loc_munca_judet"], URIRef(OPENDATA[judet + "_Judet"])))
		graph.add((doctor, OPENDATA_PROPERTY["loc_munca_localitate"], URIRef(OPENDATA[localitate + "_judet_" + judet])))
		graph.add((doctor, DBPEDIA_PROPERTY["telefon"], Literal(telefon, datatype=XSD.string)))

graph = Graph()

with open('docs_info.json') as json_data:
	output_json = json.load(json_data)
	parseJson(output_json, graph)
with open('docplanner.json') as json_data:
	output_json = json.load(json_data)
	parseJson(output_json, graph)

graph.serialize("output.rdf", format='xml', encoding='utf-8')

