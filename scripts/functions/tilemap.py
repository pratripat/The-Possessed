import pygame, json, sys
from .funcs import *

class Tilemap:
    RES = 45

    def __init__(self, filename):
        self.filename = filename
        self.entities = []
        self.load()

    #Loads the json file
    def load(self):
        data = json.load(open(self.filename, 'r'))
        for position in data:
            pos, layer = position.split(':')
            id, filepath, index, scale = data[position]
            layer = int(layer)

            x, y = pos.split(';')
            pos = [int(float(x))*self.RES, int(float(y))*self.RES]

            try:
                image = load_images_from_spritesheet('data/graphics/spritesheet/'+filepath+'.png')[index]
            except:
                image = pygame.image.load('data/graphics/spritesheet/'+filepath+'.png').convert()

            image = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))
            image.set_colorkey((0,0,0))

            dimensions = image.get_size()

            offset = self.load_offset(id, index)
            offset[0] *= scale
            offset[1] *= scale

            self.entities.append({
                'position': pos,
                'offset': offset,
                'layer': layer,
                'id': id,
                'filepath': filepath,
                'image': image,
                'index': index,
                'scale': scale,
                'dimensions': dimensions
            })

        def get_layer(elem):
            return int(elem['layer'])

        self.entities.sort(key=get_layer)

        horizontal_positions = [entity['position'][0] for entity in self.entities]
        vertical_positions = [entity['position'][1] for entity in self.entities]
        self.left = min(horizontal_positions)
        self.right = max(horizontal_positions)
        self.top = min(vertical_positions)
        self.bottom = max(vertical_positions)

    #Loads offset with id and index
    def load_offset(self, id, index):
        try:
            offset_data = json.load(open(f'data/configs/offsets/{id}_offset.json', 'r'))
            offset = offset_data[str(index)]
            return offset
        except:
            return [0,0]

    #Returns entities that are colliding with the given rect
    def get_colliding_entities(self, ids, rect):
        entities = []
        colliding_rects = []

        for id in ids:
            entities.extend(self.get_rects_with_id(id))

        for entity_rect in entities:
            if entity_rect.colliderect(rect):
                colliding_rects.append(entity_rect)

        return colliding_rects

    def get_tiles_with_position(self, id, position, layer=None):
        entities = []
        for entity in self.entities:
            if entity['id'] == id:
                if entity['position'] == position:
                    if layer != None and entity['layer'] != layer:
                        continue
                    entities.append(entity)
        return entities

    #Returns entities with the same id and layer
    def get_tiles_with_id(self, id, layer=None):
        entities = []
        for entity in self.entities:
            if entity['id'] == id:
                if layer != None and entity['layer'] != layer:
                    continue
                entities.append(entity)
        return entities

    def get_rects_with_id(self, id, layer=None):
        rects = []
        for entity in self.entities:
            if entity['id'] == id:
                rect = pygame.Rect(entity['position'][0]+entity['offset'][0], entity['position'][1]+entity['offset'][1], *entity['dimensions'])
                if layer != None and entity['layer'] != layer:
                    continue
                rects.append(rect)
        return rects

    #Removes a entity from given position and layer
    def remove_entity(self, pos, layer=None):
        for entity in self.entities[:]:
            if entity['position'] == pos:
                if layer != None and entity['layer'] != layer:
                    continue
                self.entities.remove(entity)
