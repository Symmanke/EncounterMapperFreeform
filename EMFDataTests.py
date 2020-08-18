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

from EMFNodes import EMFNodeHelper, EMFNode


"""
EMFNodeTests is used for tests specifically with nodes, no properties.
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


if __name__ == '__main__':
    unittest.main()
