import os
from scripting import *

WS_OUTPUT_SCENE = 'scenes/wizard_scene.cej'

ce = CE()


def main():    
    create_new_scene(WS_OUTPUT_SCENE)
    terrain = create_terrain()
    streets = create_streets(terrain)
    apply_rules(streets)
    ce.saveFile(WS_OUTPUT_SCENE)
    
    views = ce.getObjectsFrom(ce.get3DViews())
    views[0].frame()
    
    ce.generateModels(ce.getObjectsFrom(streets, ce.isShape), False)


def create_new_scene(ws_new_scene):
    ce.closeFile(ws_new_scene)
    fs_output_scene = ce.toFSPath(ws_new_scene)
    if os.path.exists(fs_output_scene):
        os.remove(fs_output_scene)
    ce.refreshFolder('scenes')
    return ce.newFile(ws_new_scene)
    

def create_terrain():
    terrain = ce.addAttributeLayer('terrain', 'maps/zurich_texture_10x10km.png', 'maps/zurich_heightmap_10x10km.png', True)
    ce.setAttributeLayerExtents(terrain, [-5000, -5000, 10000, 10000]) # anchor point is "north west"
    ce.setLayerAttributes(terrain, "attr elevation = map_01(brightness, 260, 870.0)")
    return terrain


def create_streets(terrain):    
    street_obstacles_layer = ce.addAttributeLayer('street_obstacles', 'maps/zurich_obstacle_10x10km.png')
    ce.setElevationOffset(street_obstacles_layer, -100)
    ce.setAttributeLayerExtents(street_obstacles_layer, [0, 0, 10000, 10000]) # quirk: anchor point is center
    ce.setLayerAttributes(street_obstacles_layer, "attr obstacle = brightness < 0.5")

    grow_street_settings = GrowStreetsSettings()
    grow_street_settings.setEnvironmentSettingsHeightmapLayer(terrain)
    grow_street_settings.setEnvironmentSettingsObstaclemapLayer(street_obstacles_layer)
    grow_street_settings.setBasicSettingsNumberOfStreets(2000)

    streets = ce.addGraphLayer('streets')
    ce.growStreets(streets, grow_street_settings)

    return streets


def apply_rules(streets):
    shapes = ce.getObjectsFrom(streets, ce.isShape)

    building_shapes = []
    street_shapes = []
    for s in shapes:
        start_rule = ce.getAttribute(s, '/ce/rule/startRule')
        if start_rule in ['Street', 'Sidewalk', 'Crossing']:
            street_shapes.append(s)
        elif start_rule in ['Lot', 'LotInner']:
            building_shapes.append(s)
    
    ce.setRuleFile(street_shapes, '/ESRI.lib/rules/Streets/Street_Modern_Standard.cga')

    ce.setRuleFile(building_shapes, '/ESRI.lib/rules/Buildings/Building_From_Footprint.cga')
    ce.setStartRule(building_shapes, 'Generate')

    
if __name__ == '__main__':
    main()