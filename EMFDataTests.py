"""
Encounter Mapper Freeform is a node-based encounter map creator for tabletop
RPGs. Copyright 2020 Eric Symmank

This file is part of Encounter Mapper Freeform.

Encounter Mapper Freeform is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

Encounter Mapper Freeform is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Encounter Mapper Freeform.
If not, see <https://www.gnu.org/licenses/>.
"""
import unittest

from EMFNodes import EMFNodeHelper, EMFNode, EMFLine, EMFShape, NodeLayer


"""
EMFNodeTests tests the builtin functions of EMFNodes. A bit redundant,
but pretty straightforward.
"""


class EMFNodeTests(unittest.TestCase):
    # Test EMFNode Creation and node.jsonObj
    def test_nodeToJSON(self):
        node = EMFNode(0, 0)
        self.assertEqual(node.jsonObj({}),
                         {'X': 0, 'Y': 0, 'DIProperties': {}})

    # Test EMFNode Creation from a jsonObj
    def test_JSONToNode(self):
        nodeJSON = {'X': 0, 'Y': 0, 'DIProperties': {}}
        node = EMFNode.createFromJSON(nodeJSON, {})
        self.assertEqual(node.jsonObj({}), nodeJSON)

    # Test EMFHelper method for creating a median from a pair of nodes
    def test_nodeMedianPair(self):
        nodePairList = [
            (EMFNode(0, 0), EMFNode(0, 100)),
            (EMFNode(0, 0), EMFNode(100, 0)),
            (EMFNode(0, 0), EMFNode(-100, 0)),
            (EMFNode(0, 0), EMFNode(0, -100)),
            (EMFNode(0, 0), EMFNode(0, 0)),
            (EMFNode(30, 60), EMFNode(45, 45)),
        ]
        medianPointList = [
            (0, 50),
            (50, 0),
            (-50, 0),
            (0, -50),
            (0, 0),
            (38, 53),
        ]

        for i in range(len(nodePairList)):
            with self.subTest(i=i):
                median = EMFNodeHelper.medianNode(nodePairList[i])
                self.assertEqual(median.x(), medianPointList[i][0])
                self.assertEqual(median.y(), medianPointList[i][1])

    # Test calculating the angles from a pair of nodes
    def test_nodeAngles(self):
        nodePairList = [
            (EMFNode(0, 0), EMFNode(0, 100)),
            (EMFNode(0, 0), EMFNode(100, 0)),
            (EMFNode(0, 0), EMFNode(-100, 0)),
            (EMFNode(0, 0), EMFNode(0, -100)),
            (EMFNode(0, 0), EMFNode(0, 0)),
            (EMFNode(30, 30), EMFNode(60, 90)),
            (EMFNode(30, 30), EMFNode(0, 90)),
            (EMFNode(30, 30), EMFNode(60, -30)),
            (EMFNode(30, 30), EMFNode(0, -30)),
        ]
        nodeDistanceList = [
            180,
            90,
            270,
            0,
            0,
            153.43494882292202,
            206.56505117707798,
            26.565051177077983,
            333.434948822922
        ]

        for i in range(len(nodePairList)):
            with self.subTest(i=i):
                self.assertEqual(EMFNodeHelper.nodeAngles(
                    nodePairList[i][0], nodePairList[i][1]),
                    nodeDistanceList[i])

    # test calculating the distance between a pair of nodes
    def test_nodeDistanceSqr(self):
        nodePairList = [
            (EMFNode(0, 0), EMFNode(0, 100)),
            (EMFNode(0, 0), EMFNode(100, 0)),
            (EMFNode(0, 0), EMFNode(-100, 0)),
            (EMFNode(0, 0), EMFNode(0, -100)),
            (EMFNode(0, 0), EMFNode(0, 0)),
            (EMFNode(30, 60), EMFNode(45, 45)),
        ]
        nodeDistanceList = [
            10000,
            10000,
            10000,
            10000,
            0,
            450
        ]

        for i in range(len(nodePairList)):
            with self.subTest(i=i):
                self.assertEqual(EMFNodeHelper.nodeDistanceSqr(
                    nodePairList[i][0], nodePairList[i][1]),
                    nodeDistanceList[i])

    # test the EMFNodeHelper.nodeComparison() method and return values
    def test_nodeComparison(self):
        nodePairList = [
            (EMFNode(0, 0), EMFNode(0, 100)),
            (EMFNode(0, 0), EMFNode(100, 0)),
            (EMFNode(0, 0), EMFNode(-100, 0)),
            (EMFNode(0, 0), EMFNode(0, -100)),
            (EMFNode(0, 0), EMFNode(0, 0)),
            (EMFNode(30, 60), EMFNode(45, 45)),
        ]
        nodeCompList = [
            (180, 10000),
            (90, 10000),
            (270, 10000),
            (0, 10000),
            (0, 0),
            (45, 450)
        ]

        for i in range(len(nodePairList)):
            with self.subTest(i=i):
                np = nodePairList[i]
                comp = EMFNodeHelper.nodeComparison(np[0], np[1])
                self.assertEqual(comp[0], np[0])
                self.assertEqual(comp[1], np[1])
                self.assertEqual(comp[2], nodeCompList[i][0])
                self.assertEqual(comp[3], nodeCompList[i][1])

    # test the EMFNodeHelper.nodeComparison() method and return values
    # when needSquareRoot = True
    def test_nodeComparisonSqrt(self):
        nodePairList = [
            (EMFNode(0, 0), EMFNode(0, 100)),
            (EMFNode(0, 0), EMFNode(100, 0)),
            (EMFNode(0, 0), EMFNode(-100, 0)),
            (EMFNode(0, 0), EMFNode(0, -100)),
            (EMFNode(0, 0), EMFNode(0, 0)),
            (EMFNode(30, 60), EMFNode(45, 45)),
        ]
        nodeCompList = [
            (180, 100),
            (90, 100),
            (270, 100),
            (0, 100),
            (0, 0),
            (45, 21.213203435596427)
        ]

        for i in range(len(nodePairList)):
            with self.subTest(i=i):
                np = nodePairList[i]
                comp = EMFNodeHelper.nodeComparison(np[0], np[1], True)
                self.assertEqual(comp[0], np[0])
                self.assertEqual(comp[1], np[1])
                self.assertEqual(comp[2], nodeCompList[i][0])
                self.assertEqual(comp[3], nodeCompList[i][1])

    # test the range for clicking the node
    def test_nodeInSelectRange(self):
        node = EMFNode(10, 10)

        clickingPoints = [
            (EMFNode(10, 10), True),
            (EMFNode(0, 10), True),
            (EMFNode(20, 10), True),
            (EMFNode(10, 0), True),
            (EMFNode(10, 20), True),
            (EMFNode(0, 0), False),
            (EMFNode(10, 21), False),
        ]

        for i in range(len(clickingPoints)):
            with self.subTest(i=i):
                self.assertEqual(
                    node.inSelectRange(
                        clickingPoints[i][0]), clickingPoints[i][1])

    # test the application of the grab transformation
    def test_nodeGrabTransform(self):
        # node = EMFNode(10, 10)

        grabTransforms = [
            (EMFNode(10, 10), (10, 10)),
            (EMFNode(10, 10), (-10, -10)),
            (EMFNode(0, 0), (10, 10)),
            (EMFNode(0, 0), (-10, -10)),
            (EMFNode(0, 0), (0, 0))
        ]

        finalPoints = [
            (20, 20),
            (0, 0),
            (20, 20),
            (0, 0),
            (10, 10)

        ]

        for i in range(len(grabTransforms)):
            with self.subTest(i=i):
                testNode = EMFNode(10, 10)

                # Handle the transform
                testNode.beginTransform(grabTransforms[i][0])
                testNode.grab(grabTransforms[i][1])
                testNode.applyTransform()

                self.assertEqual(
                    testNode.x(), finalPoints[i][0])
                self.assertEqual(
                    testNode.y(), finalPoints[i][1])

    # test the cancelling of grab transformations
    def test_nodeGrabCancelTransform(self):
        # node = EMFNode(10, 10)

        grabTransforms = [
            (EMFNode(10, 10), (10, 10)),
            (EMFNode(10, 10), (-10, -10)),
            (EMFNode(0, 0), (10, 10)),
            (EMFNode(0, 0), (-10, -10)),
        ]

        for i in range(len(grabTransforms)):
            with self.subTest(i=i):
                testNode = EMFNode(10, 10)

                # Handle the transform
                testNode.beginTransform(grabTransforms[i][0])
                testNode.grab(grabTransforms[i][1])
                testNode.cancelTransform()

                self.assertEqual(
                    testNode.x(), 10)
                self.assertEqual(
                    testNode.y(), 10)

    # test the application of the rotate transformation
    def test_nodeRotateTransform(self):
        # node = EMFNode(10, 10)

        rotateTransforms = [
            (EMFNode(10, 10), 0),
            (EMFNode(10, 10), 90),
            (EMFNode(10, 10), 180),
            (EMFNode(10, 10), 270),
            (EMFNode(20, 10), 0),
            (EMFNode(20, 10), 90),
            (EMFNode(20, 10), 180),
            (EMFNode(20, 10), 270),
        ]

        finalPoints = [
            (10, 10),
            (10, 10),
            (10, 10),
            (10, 10),
            (20, 0),
            (30, 10),
            (20, 20),
            (10, 10),
        ]

        for i in range(len(rotateTransforms)):
            with self.subTest(i=i):
                testNode = EMFNode(10, 10)

                # Handle the transform
                testNode.beginTransform(rotateTransforms[i][0])
                testNode.rotate(rotateTransforms[i][1])
                testNode.applyTransform()

                self.assertEqual(
                    testNode.x(), finalPoints[i][0])
                self.assertEqual(
                    testNode.y(), finalPoints[i][1])

    # test the cancelling of rotate transformations
    def test_nodeRotateCancelTransform(self):
        # node = EMFNode(10, 10)

        rotateTransforms = [
            (EMFNode(10, 10), 0),
            (EMFNode(10, 10), 90),
            (EMFNode(10, 10), 180),
            (EMFNode(10, 10), 270),
            (EMFNode(20, 10), 0),
            (EMFNode(20, 10), 90),
            (EMFNode(20, 10), 180),
            (EMFNode(20, 10), 270),
        ]

        for i in range(len(rotateTransforms)):
            with self.subTest(i=i):
                testNode = EMFNode(10, 10)

                # Handle the transform
                testNode.beginTransform(rotateTransforms[i][0])
                testNode.rotate(rotateTransforms[i][1])
                testNode.cancelTransform()

                self.assertEqual(
                    testNode.x(), 10)
                self.assertEqual(
                    testNode.y(), 10)

    # test the application of the scale transformation
    def test_nodeScaleTransform(self):
        # node = EMFNode(10, 10)

        rotateTransforms = [
            (EMFNode(10, 10), 0),
            (EMFNode(10, 10), 0.5),
            (EMFNode(10, 10), 1),
            (EMFNode(10, 10), 2),
            (EMFNode(20, 10), 0),
            (EMFNode(20, 10), 0.5),
            (EMFNode(20, 10), 1),
            (EMFNode(20, 10), 2),
            (EMFNode(10, 0), 0),
            (EMFNode(10, 0), 0.5),
            (EMFNode(10, 0), 1),
            (EMFNode(10, 0), 2),

        ]

        finalPoints = [
            (10, 10),
            (10, 10),
            (10, 10),
            (10, 10),
            (20, 10),
            (15, 10),
            (10, 10),
            (0, 10),
            (10, 0),
            (10, 5),
            (10, 10),
            (10, 20),

        ]

        for i in range(len(rotateTransforms)):
            with self.subTest(i=i):
                testNode = EMFNode(10, 10)

                # Handle the transform
                testNode.beginTransform(rotateTransforms[i][0])
                testNode.scale(rotateTransforms[i][1])
                testNode.applyTransform()

                self.assertEqual(
                    testNode.x(), finalPoints[i][0])
                self.assertEqual(
                    testNode.y(), finalPoints[i][1])

    # test the cancelling of scale transformations
    def test_nodeScaleCancelTransform(self):
        # node = EMFNode(10, 10)

        rotateTransforms = [
            (EMFNode(10, 10), 0),
            (EMFNode(10, 10), 90),
            (EMFNode(10, 10), 180),
            (EMFNode(10, 10), 270),
            (EMFNode(20, 10), 0),
            (EMFNode(20, 10), 90),
            (EMFNode(20, 10), 180),
            (EMFNode(20, 10), 270),
        ]

        for i in range(len(rotateTransforms)):
            with self.subTest(i=i):
                testNode = EMFNode(10, 10)

                # Handle the transform
                testNode.beginTransform(rotateTransforms[i][0])
                testNode.scale(rotateTransforms[i][1])
                testNode.cancelTransform()

                self.assertEqual(
                    testNode.x(), 10)
                self.assertEqual(
                    testNode.y(), 10)


"""
EMFLineTests tests the builtin functions of EMFLines as well as their
interactions with EMFNodes.
"""


class EMFLineTests(unittest.TestCase):

    # test creating a JSON object from an EMFLine for the sake of saving
    def test_lineToJSON(self):
        nodes = [EMFNode(0, 0), EMFNode(10, 10)]
        nodeList = {nodes[0]: 0, nodes[1]: 1}
        line = EMFLine(nodes[0], nodes[1])
        self.assertEqual(line.jsonObj(nodeList, {}),
                         {'DIProperties': {}, 'nodes': [0, 1]})

    # test the functionaility of loading an EMFLine from a JSON object
    def test_JSONToLine(self):
        nodes = [EMFNode(0, 0), EMFNode(10, 10)]
        nodeList = {nodes[0]: 0, nodes[1]: 1}
        lineJSON = {'DIProperties': {}, 'nodes': [0, 1]}

        line = EMFLine.createFromJSON(lineJSON, nodes, [])
        self.assertEqual(line.jsonObj(nodeList, {}), lineJSON)


"""
EMFSapeTests tests the builtin functions of EMFShapes, as well as the
relationship between shapes, lines, and nodes
"""


class EMFShapeTests(unittest.TestCase):
    # test creating a JSON object from an EMFShape for the sake of saving
    def test_shapeToJSON(self):
        nodes = [EMFNode(0, 0), EMFNode(10, 10), EMFNode(0, 10)]
        nodeList = {nodes[0]: 0, nodes[1]: 1, nodes[2]: 2}
        shape = EMFShape(nodes)
        self.assertEqual(shape.jsonObj(nodeList, {}),
                         {'DIProperties': {}, 'nodes': [1, 2, 0]})

    # test the functionaility of loading an EMFShape from a JSON object
    def test_JSONToShape(self):
        nodes = [EMFNode(0, 0), EMFNode(10, 10), EMFNode(0, 10)]
        nodeList = {nodes[0]: 0, nodes[1]: 1, nodes[2]: 2}
        shapeJSON = {'DIProperties': {}, 'nodes': [1, 2, 0]}

        shape = EMFShape.createFromJSON(shapeJSON, nodes, [])
        self.assertEqual(shape.jsonObj(nodeList, {}), shapeJSON)


"""
EMFNodeLayerTests tests the builtin functionality of interacting with nodes,
lines, and shapes through the NodeLayer
"""


class EMFNodeLayerTests(unittest.TestCase):

    # Helper method to create a nodeLayer given a series of inputs
    def createNodeLayer(self, nl, lis, sis, ns=True):
        lines = []
        for li in lis:
            lines.append(EMFLine(nl[li[0]], nl[li[1]]))
        shapes = []
        for si in sis:
            sNodes = []
            for i in si:
                sNodes.append(nl[i])
            shapes.append(EMFShape(sNodes, ns))
        return NodeLayer(100, 100, nl, lines, shapes)

    # test creating a JSON object from a NodeLayer for the sake of saving
    def test_nodeLayerToJSON(self):
        nl = self.createNodeLayer(
            [EMFNode(0, 0), EMFNode(10, 0), EMFNode(10, 10), EMFNode(0, 10)],
            [(3, 0), (0, 1), (1, 2), (2, 3)],
            [(0, 1, 2, 3)])

        self.assertEqual(nl.jsonObj({}),
                         {'DIProperties': {},
                          'Lines': [{'DIProperties': {}, 'nodes': [3, 0]},
                                    {'DIProperties': {}, 'nodes': [0, 1]},
                                    {'DIProperties': {}, 'nodes': [1, 2]},
                                    {'DIProperties': {}, 'nodes': [2, 3]}],
                          'Nodes': [{'DIProperties': {}, 'X': 0, 'Y': 0},
                                    {'DIProperties': {}, 'X': 10, 'Y': 0},
                                    {'DIProperties': {}, 'X': 10, 'Y': 10},
                                    {'DIProperties': {}, 'X': 0, 'Y': 10}],
                          'Shapes': [{'DIProperties': {}, 'nodes': [1, 2, 3, 0]
                                      }]})

    # test the functionaility of loading a NodeLayer from a JSON object
    def test_JSONToNodeLayer(self):
        nlJSON = {'DIProperties': {},
                  'Lines': [{'DIProperties': {}, 'nodes': [3, 0]},
                            {'DIProperties': {}, 'nodes': [0, 1]},
                            {'DIProperties': {}, 'nodes': [1, 2]},
                            {'DIProperties': {}, 'nodes': [2, 3]}],
                  'Nodes': [{'DIProperties': {}, 'X': 0, 'Y': 0},
                            {'DIProperties': {}, 'X': 10, 'Y': 0},
                            {'DIProperties': {}, 'X': 10, 'Y': 10},
                            {'DIProperties': {}, 'X': 0, 'Y': 10}],
                  'Shapes': [{'DIProperties': {}, 'nodes': [1, 2, 3, 0]}]}
        nl = NodeLayer.createFromJSON(nlJSON, {}, 100, 100)
        self.assertEqual(nl.jsonObj({}), nlJSON)


if __name__ == '__main__':
    unittest.main()
