from .model_action import ModelAction


class RoofRValue(ModelAction):
    # this shows the ip to si conversion rate
    # if unit is 'ip', then multiply this rate.
    # for window it is the U-value
    # convert U-value IP to SI
    CONVERSION_RATE = 5.678

    def __init__(self, unit="si"):
        ModelAction.__init__(self, 'roof_rvalue', unit)

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        if ModelAction.unit(self) == 'ip':
            for i in range(len(datalist)):
                datalist[i] = datalist[i] / RoofRValue.CONVERSION_RATE
        ModelAction.set_datalist(self, datalist)
