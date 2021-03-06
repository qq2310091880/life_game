import unittest
from HTMLTestRunner import HTMLTestRunner

from life_game import Mapping, Game
from life_game.basic_units import Cell
from life_game.config import Config, ConfigAttribute
from life_game import Control


class TestCell(unittest.TestCase):

    def test_init(self):
        cell = Cell(True, 4, 5)
        self.assertEqual(cell.lived, True)
        self.assertEqual(cell.next, False)
        self.assertEqual(cell.x, 4)
        self.assertEqual(cell.y, 5)
        self.assertTrue(isinstance(cell, Cell))
        self.assertIsNone(cell.shape_obj)

    def test_attr(self):
        cell = Cell(False, 5, 6)
        cell.x = 7
        cell.y = 8
        cell.next = True
        cell.lived = False
        self.assertEqual(cell.x, 7)
        self.assertEqual(cell.y, 8)
        self.assertEqual(cell.next, True)
        self.assertEqual(cell.lived, False)

    def test_look_up(self):
        mapping = Mapping(5, 5, dot_map=[[0, 1], [1, 0], [1, 2],
                                         [1, 4], [3, 1], [4, 4]])
        game_map = mapping.game_map
        for row in game_map:
            for cell in row:
                cell.look_up(mapping)
                if (cell.x == 0 and cell.y == 1 or
                    cell.x == 1 and cell.y == 1 or
                        cell.x == 2 and cell.y == 1):
                    self.assertEqual(cell.next, True)
                else:
                    self.assertEqual(cell.next, False)


class TestMapping(unittest.TestCase):

    def test_init(self):
        mapping = Mapping(3, 4)
        self.assertEqual(mapping.map_x, 3)
        self.assertEqual(mapping.map_y, 4)
        self.assertEqual(mapping.debug, False)
        self.assertTrue(isinstance(mapping, Mapping))

    def test_init_game_map(self):
        mapping = Mapping(3, 6)
        mapping.init_game_map(5, 4)
        self.assertEqual(mapping.map_x, 5)
        self.assertEqual(mapping.map_y, 4)
        self.assertEqual(len(mapping.game_map), 6)
        for row in mapping.game_map:
            self.assertEqual(len(row), 5)
            for cell in row:
                self.assertTrue(isinstance(cell, Cell))

    def test_init_cells(self):
        mapping = Mapping(3, 4, dot_map=[[0, 1]])
        mapping.init_cells([[0, 1], [2, 3], [1, 0]])
        game_map = mapping.game_map
        for row in game_map:
            for cell in row:
                if (cell.x == 0 and cell.y == 1 or
                    cell.x == 2 and cell.y == 3 or
                        cell.x == 1 and cell.y == 0):
                    self.assertEqual(cell.lived, True)
                else:
                    self.assertEqual(cell.lived, False)

    def test_generate_next(self):
        mapping = Mapping(5, 5, dot_map=[[0, 1], [1, 0], [1, 2],
                                         [1, 4], [3, 1], [4, 4]])
        mapping.generate_next()
        game_map = mapping.game_map
        for row in game_map:
            for cell in row:
                cell.look_up(mapping)
                if (cell.x == 0 and cell.y == 1 or
                    cell.x == 1 and cell.y == 1 or
                        cell.x == 2 and cell.y == 1):
                    self.assertEqual(cell.lived, True)
                else:
                    self.assertEqual(cell.lived, False)


class Env(object):
    test = ConfigAttribute('TEST')
    config = {'TEST': 'value'}


class TestConfig(unittest.TestCase):

    def test_init(self):
        config = Config({'a': 1, 'b': 'test'})
        self.assertEqual(config['a'], 1)
        self.assertEqual(config['b'], 'test')
        self.assertTrue(isinstance(config, Config))

    def test_key(self):
        config = Config()
        config['key'] = 'value'
        self.assertTrue('key' in config)

    def test_keyerror(self):
        config = Config()
        with self.assertRaises(KeyError):
            value = config['empty']

    def test_from_object(self):
        config = Config()
        env = Env()
        setattr(env, 'DEBUG', True)
        config.from_object(env)
        self.assertEqual(config['DEBUG'], True)


class TestConfigAttribute(unittest.TestCase):

    def test_init(self):
        ca = ConfigAttribute('test')
        self.assertEqual(ca.__name__, 'test')

    def test_get(self):
        env = Env()
        self.assertEqual(env.test, 'value')

    def test_set(self):
        env = Env()
        setattr(env, 'test', ConfigAttribute('TEST'))
        setattr(env, 'config', {})
        env.test = 'value'
        self.assertEqual(env.test, 'value')


class TestGame(unittest.TestCase):

    def test_init(self):
        game = Game()
        self.assertTrue(isinstance(game.config, Config))
        self.assertEqual(game.debug, False)
        self.assertEqual(game.window_width, 800)
        self.assertEqual(game.window_height, 600)
        self.assertEqual(game.row_nums, 50)
        self.assertEqual(game.column_nums, 50)
        self.assertEqual(game.margin_top, 200)
        self.assertEqual(game.margin_left, 500)
        self.assertEqual(game.sleep_time, 500)
        self.assertEqual(game.window_change, False)
        self.assertEqual(game.init_cells, None)
        self.assertEqual(game.cell_size, 10)
        self.assertEqual(game.canvas_margin_top, 50)
        self.assertEqual(game.canvas_margin_left, 135)

    def test_init_mapping(self):
        game=Game()
        game.column_nums=5
        game.row_nums=5
        game.init_cells=[[0, 1], [1, 0], [1, 2],
                         [1, 4], [3, 1], [4, 4]]
        game.init_canvas()
        game.init_mapping()

        game_map=game.mapping.game_map
        for row in game_map:
            for cell in row:
                # lived cells' shape_obj are not None
                if cell.lived:
                    self.assertIsNotNone(cell.shape_obj)


    def test_paint(self):
        game=Game()
        game.column_nums=5
        game.row_nums=5
        game.init_cells=[[0, 1], [1, 0], [1, 2],
                         [1, 4], [3, 1], [4, 4]]
        game.init_canvas()
        game.init_mapping()
        # these cells are lived in init stage.
        self.assertIsNotNone(game.mapping.game_map[0][1].shape_obj)
        self.assertIsNotNone(game.mapping.game_map[1][0].shape_obj)
        self.assertIsNotNone(game.mapping.game_map[1][2].shape_obj)
        self.assertIsNotNone(game.mapping.game_map[1][4].shape_obj)
        self.assertIsNotNone(game.mapping.game_map[3][1].shape_obj)
        self.assertIsNotNone(game.mapping.game_map[4][4].shape_obj)
        # generate the next generation
        game.mapping.generate_next()
        # repaint
        game.paint()
        # The following cells in initialization is alive and dies in the the next generation.
        self.assertIsNone(game.mapping.game_map[1][0].shape_obj)
        self.assertIsNone(game.mapping.game_map[1][2].shape_obj)
        self.assertIsNone(game.mapping.game_map[1][4].shape_obj)
        self.assertIsNone(game.mapping.game_map[3][1].shape_obj)
        self.assertIsNone(game.mapping.game_map[4][4].shape_obj)
        # The following cells in initialization is alive and will remain alive in the next generation.
        self.assertIsNotNone(game.mapping.game_map[0][1].shape_obj)
        # The following cells in initialization is dead, resurrected in the next generation.
        self.assertIsNotNone(game.mapping.game_map[1][1].shape_obj)
        self.assertIsNotNone(game.mapping.game_map[2][1].shape_obj)
    
    """
        Timer,Unit test not yet implemented.
    """
    def test_loop_paint(self):
        pass
    
    def test_start(self):
        pass
        
class TestControl(unittest.TestCase):
    def test_init(self):
        control=Control()
        self.assertTrue(control.update_cells)
        self.assertEqual(control.paint_nums,0)
        self.assertEqual(control.loop_nums,0)
        self.assertIsInstance(control,Control)
    
    def test_mapping(self):
        control=Control()
        # init mapping is None
        control.init_canvas()
        control.init_mapping()
        self.assertEqual(control.mapping,control.mapping)
    
    def test_map_x(self):
        control=Control()
        control.init_canvas()
        control.init_mapping()
        self.assertEqual(control.mapping.map_x,control.map_x)
    
    def test_map_y(self):
        control=Control()
        control.init_canvas()
        control.init_mapping()
        self.assertEqual(control.mapping.map_y,control.map_y)

    def test_root(self):
        control=Control()
        self.assertEqual(control.root,control.root)
    
    def test_config(self):
        control=Control()
        self.assertEqual(control.config,control.config)
    
    def test_cv(self):
        control=Control()
        control.init_canvas()
        self.assertEqual(control.canvas, control.canvas)

    def test_get_cell_position(self):
        control=Control()
        # a simple test example
        control.init_cells=[[0, 1], [1, 0]]
        control.init_canvas()
        control.init_mapping()

        traget_tuple_1= (0*control.cell_size+control.canvas_margin_left,
                        1*control.cell_size+control.canvas_margin_top,
                        (0+1)*control.cell_size+control.canvas_margin_left,
                        (1+1)*control.cell_size+control.canvas_margin_top)

        for index,value in enumerate(control.get_cell_position(0,1)):
               self.assertEqual(traget_tuple_1[index],value)

        traget_tuple_2= (1*control.cell_size+control.canvas_margin_left,
                        0*control.cell_size+control.canvas_margin_top,
                        (1+1)*control.cell_size+control.canvas_margin_left,
                        (0+1)*control.cell_size+control.canvas_margin_top)
        
        for index,value in enumerate(control.get_cell_position(1,0)):
               self.assertEqual(traget_tuple_2[index],value)
    
    def test_before_control(self):
        control=Control()
        # before loop_nums
        loop_nums_pre=control.loop_nums
        control.before_control()
        # after loop_nums
        loop_nums_next=control.loop_nums
        self.assertEqual(loop_nums_pre+1,loop_nums_next)
    
    def test_after_paint(self):
        control=Control()
        # before paint_nums
        paint_nums_pre=control.paint_nums
        control.after_paint()
        # after paint_nums
        paint_nums_next=control.paint_nums
        self.assertEqual(paint_nums_pre+1,paint_nums_next)

    def test_start(self):
        pass

    def test_after_control(self):
        pass


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMapping))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCell))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConfig))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConfigAttribute))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGame))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestControl))

    with open('HTMLReport.html', 'wb+') as f:
        runner = HTMLTestRunner(stream=f,
                                title='Life game test report',
                                description='life game.',
                                verbosity=2
                                )
        runner.run(suite)
