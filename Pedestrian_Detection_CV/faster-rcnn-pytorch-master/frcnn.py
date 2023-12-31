import colorsys
import os
import time

import numpy as np
import torch
import torch.nn as nn
from PIL import Image, ImageDraw, ImageFont

from nets.frcnn import FasterRCNN
from utils.utils import (cvtColor, get_classes, get_new_img_size, resize_image,
                         preprocess_input, show_config)
from utils.utils_bbox import DecodeBox



class FRCNN(object):
    _defaults = {
        
        "model_path"    : 'model_data/voc_weights_resnet.pth',
        "classes_path"  : 'model_data/voc_classes.txt', 
        "backbone"      : "resnet50",
        "confidence"    : 0.5,
        "nms_iou"       : 0.3,
        'anchors_size'  : [8, 16, 32],
        "cuda"          : False,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    
    
    
    #Initialize faster-rcnn
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        print(' Model has loaded.')
           
        for name, value in kwargs.items():
            setattr(self, name, value)
        
        #Get the classed and numbers
        self.class_names, self.num_classes  = get_classes(self.classes_path)

        self.std    = torch.Tensor([0.1, 0.1, 0.2, 0.2]).repeat(self.num_classes + 1)[None]
        if self.cuda:
            self.std    = self.std.cuda()
        self.bbox_util  = DecodeBox(self.std, self.num_classes)

        
        #set different colors to the frame
        hsv_tuples = [(x / self.num_classes, 1., 1.) for x in range(self.num_classes)]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), self.colors))
        self.generate()

    
    #load the model
    def generate(self):
        self.net    = FasterRCNN(self.num_classes, "predict", anchor_scales = self.anchors_size, backbone = self.backbone)
        device      = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.net.load_state_dict(torch.load(self.model_path, map_location=device))
        self.net    = self.net.eval()
        
        
        
        if self.cuda:
            self.net = nn.DataParallel(self.net)
            self.net = self.net.cuda()
    
    
    #detect the image and draw the frame
    def detect_image(self, image, crop = False, count = False):
        
        #calculate the size of the image
        image_shape = np.array(np.shape(image)[0:2])
        
        #resize
        input_shape = get_new_img_size(image_shape[0], image_shape[1])
        
        #change the image to RGB format
        image       = cvtColor(image)
       
        #resize
        image_data  = resize_image(image, [input_shape[1], input_shape[0]])
        image_data  = np.expand_dims(np.transpose(preprocess_input(np.array(image_data, dtype='float32')), (2, 0, 1)), 0)

        with torch.no_grad():
            images = torch.from_numpy(image_data)
            if self.cuda:
                images = images.cuda()
            
           
            roi_cls_locs, roi_scores, rois, _ = self.net(images)
            results = self.bbox_util.forward(roi_cls_locs, roi_scores, rois, image_shape, input_shape, 
                                                    nms_iou = self.nms_iou, confidence = self.confidence)
                    
            if len(results[0]) <= 0:
                return image
                
            top_label   = np.array(results[0][:, 5], dtype = 'int32')
            top_conf    = results[0][:, 4]
            top_boxes   = results[0][:, :4]
        
        
        #format the font and frame
        font        = ImageFont.truetype(font='model_data/simhei.ttf', size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness   = int(max((image.size[0] + image.size[1]) // np.mean(input_shape), 1))
        
        
        #draw the image
        for i, c in list(enumerate(top_label)):
            predicted_class = self.class_names[int(c)]
            
            #only detect the person
            if predicted_class == 'person':
                
                box             = top_boxes[i]
                score           = top_conf[i]

                top, left, bottom, right = box

                top     = max(0, np.floor(top).astype('int32'))
                left    = max(0, np.floor(left).astype('int32'))
                bottom  = min(image.size[1], np.floor(bottom).astype('int32'))
                right   = min(image.size[0], np.floor(right).astype('int32'))

                label = '{} {:.2f}'.format(predicted_class, score)
                draw = ImageDraw.Draw(image)
                label_size = draw.textsize(label, font)
                label = label.encode('utf-8')
                # print(label, top, left, bottom, right)

                if top - label_size[1] >= 0:
                    text_origin = np.array([left, top - label_size[1]])
                else:
                    text_origin = np.array([left, top + 1])

                for i in range(thickness):
                    draw.rectangle([left + i, top + i, right - i, bottom - i], outline=self.colors[c])
                draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=self.colors[c])
                draw.text(text_origin, str(label,'UTF-8'), fill=(0, 0, 0), font=font)
                del draw

        return image



    