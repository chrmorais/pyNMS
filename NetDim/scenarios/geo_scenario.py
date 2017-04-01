from .base_scenario import BaseScenario
from map.map import Map

def overrider(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider

class GeoScenario(BaseScenario):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # map 
        self.world_map = Map(self, viewportx=500, viewporty=250)
        self.world_map.change_projection('mercator')
        self.world_map.load_map(self.world_map.create_meridians())
        self.world_map.centerCarta([[7, 49]])
        
        # for the shapefile not to be automatically reloaded when NetDim 
        # is closed and reopened
        self.ms.update()
        
    def adapt_coordinates(function):
        def wrapper(self, event, *others):
            event.x, event.y = self.cvs.canvasx(event.x), self.cvs.canvasy(event.y)
            function(self, event, *others)
        return wrapper
            
    def switch_binding(self): 
        super(GeoScenario, self).switch_binding()
        
        # if self._mode == 'motion':
            # self.cvs.tag_bind('water', '<ButtonPress-1>', self.move_sphere, add='+')
            # self.cvs.tag_bind('Area', '<ButtonPress-1>', self.move_sphere, add='+')
            
    # set the map object at the bottom of the stack
    def lower_map(self):
        for map_obj in self.world_map.map_ids:
            self.cvs.tag_lower(map_obj)
        if self.world_map.is_spherical():
            self.cvs.tag_lower(self.world_map.oval_id)
        
    @adapt_coordinates
    def move_sphere(self, event):
        coords = self.world_map.from_points((event.x, event.y), dosphere=1)
        if coords and self.world_map.is_spherical():
            self.world_map.map_temp['centerof'] = coords
            self.world_map.change_projection(self.world_map.mode)
                        
    @adapt_coordinates
    @overrider(BaseScenario)
    def create_node_on_binding(self, event):
        node = self.ntw.nf(node_type=self._creation_mode, x=event.x, y=event.y)
        # update logical and geographical coordinates
        lon, lat = self.world_map.get_geographical_coordinates(node.x, node.y)
        node.longitude, node.latitude = lon, lat
        node.logical_x, node.logical_y = node.x, node.y
        self.create_node(node)
      
    @overrider(BaseScenario)
    def create_node(self, node, layer=1):
        super(GeoScenario, self).create_node(node, layer)
        # if the node wasn't created from the binding (e.g import or graph
        # generation), its canvas coordinates are initialized at (0, 0). 
        # we update them based on their geographical coordinates
        if not node.x and not node.y:
            node.x, node.y = self.world_map.to_points([[node.longitude, node.latitude]], 1)
        
    @overrider(BaseScenario)
    def create_link(self, new_link):
        # create the link
        super(GeoScenario, self).create_link(new_link)
        # the link is now at the bottom of the stack after calling tag_lower
        # if the map is activated, we need to lower all map objects to be 
        # able to see the link
        self.lower_map()
            
    ## Map Menu
    
    def update_geographical_coordinates(self, *nodes):
        for node in nodes:
            node.longitude, node.latitude = self.world_map.get_geographical_coordinates(node.x, node.y)
            
    def update_logical_coordinates(self, *nodes):
        for node in nodes:
            node.logical_x, node.logical_y = node.x, node.y 
            
    def move_to_geographical_coordinates(self, *nodes):
        for node in nodes:
            node.x, node.y = self.world_map.to_points([[node.longitude, node.latitude]], 1)
        self.move_nodes(nodes)
        
    def move_to_logical_coordinates(self, *nodes):
        for node in nodes:
            node.x, node.y = node.logical_x, node.logical_y
        self.move_nodes(nodes)
        
    ## Geographical projection menu
    
    def change_projection(self, mode):
        self.world_map.change_projection(mode)
        self.lower_map()
    
    @adapt_coordinates
    @overrider(BaseScenario)
    def zoomer(self, event):
        ''' Zoom for window '''
        self._cancel()
        factor = 1.1 if event.delta > 0 else 0.9
        self.diff_y *= factor
        self.node_size *= factor
        self.world_map.scale_map(ratio=factor)
        self.update_nodes_coordinates(factor)