"""
The `Model` class is used to instantiate a central namespace for a SysML model by subsuming elements into mode elements or model relationships.

---------

Model elements and relationships are the building blocks that make up the 9 SysML diagrams
"""
from sysml.elements import *
import uuid

# developer notes: to use hidden vs unhidden attributes

class Model(object):
    """This class defines a SysML model for subsuming elements into model elements or relationships.
    """

    # Dictionary of valid model elements. key: element [string], value: element [class]
    _validElements = {
        "block":Block,
        "requirement":Requirement,
        "constraint":ConstraintBlock,
        "package":Package
    }

    # Dictionary of valid model relationships. key: element [string], value: valid element nodes [list of classes]
    _validRelationships = {
        "containment":{
            "source":[Block],
            "target":[Block]},
        "inheritance":{
            "source":[Block],
            "target":[Block]},
        "association":{
            "source":[Block],
            "target":[Block]},
        "generalization":{
            "source":[Block],
            "target":[Block]},
        "partProperty":{
            "source":[Block],
            "target":[Block]},
        "valueProperty":{
            "source":[Block],
            "target":[Block]},
        "referenceProperty":{
            "source":[Block],
            "target":[Block]},
        "flowProperty":{
            "source":[Block],
            "target":[Block]}
    }

    def __init__(self, label=None, elements={}, relationships={}):
        # Model label
        self._label = label
        # All model elements stored as a dictionary of key-value pairs
        self._elements = elements

    def __setitem__(self, key, element):
        "Sets/overwrites element-valid model element or relationship into model"
        if self._isValidElementKey(key):
            self._setElement(key, element)
        elif self._isValidRelationshipKey(key):
            self._setRelationship(key, element)
        else:
            raise ValueError(repr(key) + " is not a valid key. Keys should be a string containing a dash-separated element and integer, e.g., 'partProperty-42' ")

    def __getitem__(self, key):
        "Returns data for key-specified model element or relationship"
        if key in self._elements.keys():
            return self._elements[key]
        elif key in self._relationships.keys():
            return self._relationships[key]
        else:
            raise ValueError(repr(key) + " is not a valid key. Keys should be a string containing a dash-separated element and integer, e.g., 'partProperty-42' ")

    @property
    def elements(self):
        "Returns dictionary of model elements"
        return self._elements

    @property
    def relationships(self):
        "Returns dictionary of relationships"
        return self._relationships

    @elements.setter
    def elements(self, elements):
        """Sets/rewrites model elements for entire model by passing model elements as key-value pairs.

        Note: model elements must be valid elements.
        """
        if type(elements) is not dict:
            raise TypeError(repr(elements) + " must be a dictionary.")
        else:
            for key in elements.keys():
                self._setElements(key, elements[key])

    @relationships.setter
    def relationships(self, relationships):
        """Sets relationships to user-defined dictionary.

        Note: model relationships must be valid elements.
        """
        if type(relationships) is not dict:
            raise TypeError(repr(relationships) + " must be a dictionary.")
        for key in relationships.keys():
            elementName, id_no = key.split('-')
            if not self._isValidRelationshipKey(key):
                raise ValueError(key + " is not a valid key. Keys should be a string containing a dash-separated element and integer, e.g., 'partProperty-42' ")
            else:
                self._setRelationship(key, relationships[key])

    def add_elements(self, *elementv):
        "Sets/overwrites element-valid model element or relationship into model"
        for element in elementv:
            key = self._generateKey(element, len(self._elements)+1)
            self._setElement(key, element)

    def add_relationships(self, *relationshipv):
        "Sets/overwrites element-valid model element or relationship into model"
        for relationship in relationshipv:
            key = self._generateKey(relationship, len(self._relationships)+1)
            self._setRelationship(key, relationship)

    def add_package(self, label=None):
        """Creates a package element in model"""
        if type(label) is str:
            self._setElement(label, Package(label))
        else:
            raise TypeError(label + " must be a string")

    ## Structural Diagrams
    def bdd(self):
        """Generates a BlockDefinitionDiagram

        A block definition diagram describes the system hierarchy and system/component classifications.
        """
        pass

    def pkg(self):
        """Generates a package diagram

        The package diagram is used to organize the model.
        """
        pass

    ## Behavioral Diagrams
    def uc(self):
        """Generates a use case diagram

        A use-case diagram provides a high-level description of functionality that is achieved through interaction among systems or system parts.
        """
        pass

    ## Requirement Diagrams
    def req(self):
        """Generates a requirement diagram

        The requirements diagram captures requirements hierarchies and requirements derivation, and the satisfy and verify relationships allow a modeler to relate a requirement to a model element that satisfies or verifies the requirements.
        """
        pass

    def _generateKey(self, element, maxId_no):
        if self._isValidElement(element):
            for validElement in self._validElements.keys():
                if isinstance(element, self._validElements[validElement]):
                    for id_no in range(1, maxId_no+1):
                        newKey = validElement + "-" + str(id_no)
                        if newKey not in self._elements.keys():
                            return newKey
        elif self._isValidRelationship(element):
            for validRelationship in self._validRelationships.keys():
                if element["relationshipType"] is validRelationship:
                    for id_no in range(1, maxId_no+1):
                        newKey = validRelationship + "-" + str(id_no)
                        if newKey not in self._relationships.keys():
                            return newKey
        else:
            raise TypeError(element + " is not a valid element.")

    def _setElement(self, key, element):
        if key is None:
            key = self._generateKey(element)
        if not self._isValidElement(element):
            raise TypeError(repr(element) + " is not a valid model element.")
        else:
            self._elements[key] = element
            self._elements[key].uuid = str(uuid.uuid1())

    def _setRelationship(self, key, relationship):
        if relationship["source"] not in self._elements.keys():
            raise TypeError(relationships[key]["source"] + " does not exist in model.")
        if relationship["target"] not in self._elements.keys():
            raise TypeError(relationship["target"] + " does not exist in model.")
        if not self._isValidRelationship(relationship):
            raise TypeError(relationship["source"] + " and " + relationships["target"] + " are not a valid source-target pair for " + elementName)
        else:
            self._relationships[key] = relationship
            # if not hasattr(self._relationships[key], 'uuid'):
            #     self._relationships[key].uuid = str(uuid.uuid1())

    def _isValidRelationship(self, relationship):
        source = self._elements[relationship["source"]]
        target = self._elements[relationship["target"]]
        relationshipType = relationship["relationshipType"]
        return type(source) in self._validRelationships[relationshipType]['source'] and type(target) in self._validRelationships[relationshipType]['target']

    @classmethod
    def _isValidElementKey(cls, key):
        elementName, id_no = key.split('-')
        return elementName in cls._validElements.keys() and isinstance(int(id_no),int)

    @classmethod
    def _isValidElement(cls, element):
        return type(element) in cls._validElements.values()

    @classmethod
    def _isValidRelationshipKey(cls, key):
        relationship, id_no = key.split('-')
        return relationship in cls._validRelationships.keys() and isinstance(int(id_no),int)

    # @classmethod
    # def _isValidSource(cls, relationship, source):
    #     return source in cls._validRelationships[relationship]['source']
    #
    # @classmethod
    # def _isValidTarget(cls, relationship, target):
    #     return target in cls._validRelationships[relationship]['target']
